from typing import Any, BinaryIO
import logging
import requests
import xlrd


logger = logging.getLogger(__name__)


def download_file_from_spimex() -> BinaryIO:

    url = 'https://spimex.com/upload/reports/oil_xls/oil_xls_20230628162000.xls'
    response = requests.get(url)
    with open('.data/spimex.xls', 'wb') as output:
        output.write(response.content)


def read_spimex_file() -> Any:
    logging.basicConfig(level=logging.INFO)

    workbook = xlrd.open_workbook('.data/spimex.xls')
    sheet = workbook.sheet_by_index(0)
    for row in range(sheet.nrows):
        for column in range(sheet.ncols):
            logger.info(sheet.cell(row, column))
