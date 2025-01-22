import os
from app import run_app

app = run_app()

if __name__ == '__main__':
    host = os.getenv('DISCLOSURE_IP', 'localhost')
    port = os.getenv('DISCLOSURE_PORT', '8081')

    app.run(host=host, port=port, debug=True)
    #완료 20150101/20240120

"""
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
from yp_fin_utils.parsers.parsers import extract_value_from_xml
from yp_fin_utils.utils.utils import is_number, formatted_date
from app.fetchers.kr_disclosure_fetcher import KRDisclosureFetcher
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from yp_fin_utils.models import MarketModelFactory
from app.fetchers.fetcher_factory import FetcherFactory
from app.celery_app.worker import celery


def parse_amount(amount: str):
    if not amount:
        return 0
    if is_number(amount):
        return float(amount.replace(',',''))
    for match in re.findall(r"\d[\d,]*", amount):
        value = float(match.replace(',',''))
        if value > 1000:
            return value
    return 0

def extract_dividend_info(document_xml):
    return {
            'dividend_type': extract_value_from_xml(cleaned_xml, "배당구분"),
            'dividend_method': extract_value_from_xml(cleaned_xml, "배당종류"),
            'asset_details': extract_value_from_xml(cleaned_xml, "상세내역"),
            'total_dividend_amount': parse_amount(extract_value_from_xml(cleaned_xml, "배당금총액")),
            'record_date': extract_value_from_xml(cleaned_xml, "배당기준일"),
            'payment_date': extract_value_from_xml(cleaned_xml, "배당금지급 예정일자"),
    }

dart_api = '541a296fd06cf0a27eacea908da44f24949f2cd0'
dart_fss.set_api_key(dart_api)

disclosure_model = MarketModelFactory.get_model('DISCLOSURE', 'kr')

cursor = disclosure_model.objects.raw({'dividend_type': None})

for c in cursor:
    print(c.recept_dt, c.recept_no, c.recept_nm)
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            full_path = dart_fss.api.filings.download_document(tmpdir, rcept_no=c.recept_no)
            zip_path = full_path
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_name in zip_ref.namelist():
                    with zip_ref.open(file_name) as file:
                        html_text = file.read()
                        encoding_info = chardet.detect(html_text)
                        decoded_html = html_text.decode(encoding_info['encoding'])
                        unescaped_html = html.unescape(decoded_html)
                        cleaned_xml = re.sub(r'<meta[^>]*>|<br[^>]*>', '', unescaped_html)
                        dividend_info = extract_dividend_info(cleaned_xml)
                        print('dividend_info', dividend_info)
                        c.dividend_type = dividend_info['dividend_type']
                        c.dividend_method = dividend_info['dividend_method']
                        c.asset_details = dividend_info['asset_details']
                        c.total_dividend_amount = dividend_info['total_dividend_amount']
                        c.record_date = dividend_info['record_date']
                        c.payment_date = dividend_info['payment_date']
                        c.save()
        except Exception as e:
            print('error', e)



"""
