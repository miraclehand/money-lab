import logging
import tempfile
import re
import zipfile
import chardet
import dart_fss
import html
from typing import Optional
from datetime import datetime, timedelta
from yp_fin_utils.models import MarketModelFactory
from yp_fin_utils.parsers.parsers import extract_value_from_html
from yp_fin_utils.utils.utils import is_number, formatted_date
from app.fetchers.kr_disclosure_fetcher import KRDisclosureFetcher


logger = logging.getLogger(__name__)

class KRDividendDisclosureFetcher(KRDisclosureFetcher):
    def __init__(self):
        super().__init__()
        self.disclosure_model = MarketModelFactory.get_model('DISCLOSURE', self.COUNTRY)

    def sync_data(self, start_date = None, end_date = None):
        start_date_str, end_date_str = self.calculate_date_range(start_date, end_date)
        logger.info(f'Sync start_date:{start_date_str} end_date:{end_date_str}')

        start_date = datetime.strptime(start_date_str, '%Y%m%d')
        end_date = datetime.strptime(end_date_str, '%Y%m%d')
        current_date = start_date

        while current_date <= end_date:
            next_date = min(current_date + timedelta(days=10), end_date)
            logger.info(f'Sync period starting between {current_date} and {next_date}')

            reports = super().sync_data(current_date, next_date)
            dividend_reports = [report for report in reports if '배당' in report.report_nm and '첨부정정' not in report.report_nm]

            for dividend_report in dividend_reports:
                logger.info(f'diviend_report rcept_dt:{dividend_report.rcept_dt}, corp_name:{dividend_report.corp_name}')
                self._process_dividend_report(dividend_report)

            current_date = next_date + timedelta(days=1)

        logger.info("Sync disclosure fetch completed.")

    def _process_dividend_report(self, report) -> None:
        report_data = {field: getattr(report, field, '').strip() for field in self.REPORT_FIELDS}

        stock  = MarketModelFactory.find_stock_by_ticker(self.COUNTRY,  report_data['stock_code'])
        candle = MarketModelFactory.find_candle_by_ticker(self.COUNTRY, report_data['stock_code'])

        if not stock or not candle:
            logger.error(f'{report_data["stock_code"]} {report_data["corp_name"]} {report_data["rm"]} does not found in the stock or candle model')
            return

        document_xml = self._fetch_document_html(report_data['rcept_no'])
        if not document_xml:
            logger.error(f'document_xml does not found. {report_data}')
            return

        dividend_info = self._extract_dividend_info(document_xml)
        if not dividend_info:
            logger.error(f'dividend_info does not found. {dividend_info}')
            return

        report_data.update(dividend_info)
        self._update_or_create_record(report_data, dividend_info, stock, candle)

    def _fetch_document_html(self, rcept_no: str) -> Optional[str]:
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                full_path = dart_fss.api.filings.download_document(tmpdir, rcept_no=rcept_no)
                return self._extract_html_from_zip(full_path)
            except Exception as e:
                logger.error(f"Error downloading document: {e} rcept_no: {rcept_no}")
                return None

    def _extract_html_from_zip(self, zip_path: str) -> str:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                with zip_ref.open(file_name) as file:
                    html_text = file.read()
                    encoding_info = chardet.detect(html_text)
                    decoded_html = html_text.decode(encoding_info['encoding'])
                    unescaped_html = html.unescape(decoded_html)
                    return re.sub(r'<meta[^>]*>|<br[^>]*>', '', unescaped_html)
        return None

    def _extract_dividend_info(self, cleaned_xml: str) -> dict:
        return {
            'dividend_type': extract_value_from_html(cleaned_xml, "배당구분"),
            'dividend_method': extract_value_from_html(cleaned_xml, "배당종류"),
            'asset_details': extract_value_from_html(cleaned_xml, "상세내역"),
            'total_dividend_amount': self._parse_amount(extract_value_from_html(cleaned_xml, "배당금총액")),
            'record_date': extract_value_from_html(cleaned_xml, "배당기준일") or extract_value_from_html(cleaned_xml, "기준일"),
            'payment_date': extract_value_from_html(cleaned_xml, "배당금지급 예정일자"),
        }

    def _parse_amount(self, amount: str):
        if not amount:
            return 0

        if is_number(amount):
            return float(amount.replace(',',''))

        for match in re.findall(r"\d[\d,]*", amount):
            value = float(match.replace(',',''))
            if value > 1000:
                return value
        return 0

    def _update_or_create_record(self, report_data, dividend_info, stock, candle):
        query = {
            'country': self.COUNTRY,
            'recept_dt': formatted_date(report_data['rcept_dt']),
            'recept_no': report_data['rcept_no'],
            'recept_nm': report_data['report_nm'],
        }

        cursor = self.disclosure_model.objects.raw(query)
        if cursor.count() > 0:
            existing_record = cursor.first()

            update_fields = {}
            for key, value in dividend_info.items():
                if getattr(existing_record, key, None) != value:
                    setattr(existing_record, key, value)
                    update_fields[key] = value

            for key, value in update_fields.items():
                logger.info(f'Update {key} record [{getattr(existing_record, key, None)}] -> [{value}]')
                setattr(existing_record, key, value)
                existing_record.updated_at = datetime.now()
                existing_record.save()
        else:
            self.disclosure_model(self.COUNTRY, stock._id, candle._id, report_data).save()
