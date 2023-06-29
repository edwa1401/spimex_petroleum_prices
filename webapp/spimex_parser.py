import requests
from typing import BinaryIO, Any
import xlrd
from dataclasses import dataclass


@dataclass
class Spimex_data:
    code_instr: str
    name_instr: str
    basis: str
    volume_tn: int
    volume_rub: int


def download_file_from_spimex() -> BinaryIO:

    url = 'https://spimex.com/upload/reports/oil_xls/oil_xls_20230628162000.xls'
    response = requests.get(url)
    with open('.data/spimex.xls', 'wb') as output:
        output.write(response.content)


def read_spimex_file() -> Any:
    workbook = xlrd.open_workbook('.data/spimex.xls')
    sheet = workbook.sheet_by_index(0)
    for row in range(sheet.nrows):
        print(sheet.row(row))
