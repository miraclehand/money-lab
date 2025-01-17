import logging
import dart_fss
from abc import abstractmethod
from datetime import datetime
from app.config.settings import CurrentConfig
from app.fetchers.disclosure_fetcher import DisclosureFetcher


logger = logging.getLogger(__name__)

class KRDisclosureFetcher(DisclosureFetcher):
    def __init__(self):
        self.COUNTRY = 'KR'
        self.REPORT_FIELDS = [
            "rcept_dt", "rcept_no", "report_nm",
            "stock_code", "corp_code", "corp_name",
            "corp_cls", "flr_nm", "rm"
        ]
        dart_fss.set_api_key(CurrentConfig.DART_API_KEY)

    @abstractmethod
    def sync_data(self, start_date: str = None, end_date: str = None):
        reports = self.fetch_reports_between_dates(start_date, end_date)
        return reports

    def fetch_reports_between_dates(self, start_date: [str, datetime], end_date: [str, datetime]):
        all_reports = []
        page_no = 1

        if isinstance(start_date, datetime):
            start_date_str = start_date.strftime('%Y%m%d'),
        else:
            start_date_str = start_date.replace('-','')

        if isinstance(end_date, datetime):
            end_date_str = end_date.strftime('%Y%m%d'),
        else:
            end_date_str = end_date.replace('-','')

        while True:
            try:
                reports = dart_fss.filings.search(
                    pblntf_ty='I',
                    bgn_de=start_date_str,
                    end_de=end_date_str,
                    page_no=page_no,
                    page_count=100,
                )
            except dart_fss.errors.NoDataReceived:
                logger.info(f'No data received between {start_date_str} and {end_date_str}')
                break

            if not reports:
                break

            logger.info(f'Fetch data {page_no}page of {reports.total_page}pages')

            all_reports.extend(reports)

            page_no += 1
            if page_no > reports.total_page:
                break

        return all_reports
