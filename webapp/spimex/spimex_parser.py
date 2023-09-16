import logging
from datetime import date, datetime
from typing import Any

import requests
import xlrd
from bs4 import BeautifulSoup
from fastapi import HTTPException
from xlrd import sheet

import webapp.config as config
from webapp.spimex.schemas import Contract, Section, TradeDay
import re

logger = logging.getLogger(__name__)


def get_date(date: str) -> date:
    return datetime.date(datetime.strptime(date, '%Y-%m-%d'))


def convert_date(date: date) -> str:
    if date.weekday() == 5 or date.weekday() == 6:
        return 'No tradings in holidays'
    if len(str(date.day)) == 1:
        day = '0' + str(date.day)
    else:
        day = str(date.day)
    if len(str(date.month)) == 1:
        month = '0' + str(date.month)
    else:
        month = str(date.month)
    return str(date.year) + month + day


def get_url_to_spimex_data(date: str) -> str:
    url = 'https://spimex.com/upload/reports/oil_xls/oil_xls_' + date + '162000.xls'
    return url


def get_sessid(sess: requests.Session) -> str:
    url_rzd = 'https://spimex.com/markets/oil_products/rzd/'
    resp = sess.get(url_rzd)
    soup = BeautifulSoup(resp.text, 'html.parser')
    raw_scripts = soup.head.find_all('script')
    for script in raw_scripts:
        if 'bitrix_sessid' in script.text:
            result = script.text
    sess_id_re = re.compile("^.*'bitrix_sessid':'(\w*)'.*$")
    match = sess_id_re.match(result)
    if match:
        sessid = match.groups()[0]

    return sessid


def get_rail_tariff_from_spimex(station_from: str, station_to: str, cargo: str) -> Any:

    sess = requests.Session()

    sessid = get_sessid(sess)

    url = 'https://spimex.com/local/components/spimex/calculator.rzd/templates/.default/ajax.php'

    payload = {
        'action': 'getCalculation',
        'sessid': sessid,
        'type': '43',
        'st1': station_from,
        'st2': station_to,
        'kgr': cargo,
        'ves': '52',
        'gp': '66',
        'nv': '1',
        'nvohr': '1',
        'nprov': '0',
        'osi': '4',
        'sv': '2'
    }
    response = sess.post(url=url, data=payload)
    response.raise_for_status()

    return response.json()


def download_file_from_spimex(url: str) -> bytes:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPException:
        raise HTTPException(
            status_code=500,
            detail='Ошибка сайта СПБМТСБ'
        )
    return response.content

# TODO добавить нормальную обработку ошибок


def read_spimex_file(content: bytes) -> sheet.Sheet:
    workbook = xlrd.open_workbook(file_contents=content)
    return workbook.sheet_by_index(0)


def get_all_cell_values_from_sheet(sheet: sheet.Sheet) -> list[str]:
    all_raw_data = []
    for row in range(sheet.nrows):
        for column in range(sheet.ncols):
            all_raw_data.append(sheet.cell_value(row, column))
    return all_raw_data


def delete_all_emty_values_from_raw_data(raw_data: list[str]) -> list[str]:
    return [value for value in raw_data if value != '']


def get_indexes_for_search_value(all_values: list[str], search_value: str) -> list[int]:
    return [value for value in range(len(all_values)) if all_values[value].startswith(search_value)]


def extract_value_from_string(raw_string: str, prefix: str) -> str:
    if prefix in raw_string:
        return raw_string[len(prefix):len(raw_string)]
    else:
        return raw_string


def make_strings_from_all_values(all_values: list[str], search_value: str, prefix: str) -> list[str]:
    indexes = get_indexes_for_search_value(all_values, search_value)
    return [extract_value_from_string(all_values[index], prefix) for index in indexes if extract_value_from_string(all_values[index], prefix)]


def get_day(all_values: list[str]) -> date:
    days_str = make_strings_from_all_values(all_values, search_value='Дата торгов: ', prefix='Дата торгов: ')
    days = [datetime.strptime(day_str, '%d.%m.%Y') for day_str in days_str]
    return datetime.date(days[0])


def convert_empty_strings(string: str) -> Any:
    return None if string == '-' else string


def convert_empty_values_to_zero(string: str) -> Any:
    return '0' if string == '-' else string


def get_sections_indexes(all_values: list[str]) -> list[list[int]]:
    start_section_indexes = get_indexes_for_search_value(all_values, search_value='Лучший\nспрос')
    end_section_indexes = get_indexes_for_search_value(all_values, search_value='Итого:')
    sections_indexes = []
    for sections_index in range(len(start_section_indexes)):
        sections_indexes.append([start_section_indexes[sections_index] + 1, end_section_indexes[sections_index]])
    return sections_indexes


def get_raw_sections(all_values: list[str], sections_indexes: list[list[int]]) -> list[list[str]]:
    return [all_values[section_indexes[0]:section_indexes[1]] for section_indexes in sections_indexes]


def get_contracts_from_section(section: list[str]) -> list[Contract]:
    start_index = 0
    end_index = config.NUM_COLUMNS_IN_SECTION
    num_of_contracts_in_section = len(section) // config.NUM_COLUMNS_IN_SECTION
    contracts = []
    for _ in range(num_of_contracts_in_section):
        contract = section[start_index:end_index]
        start_index = end_index
        end_index = end_index + config.NUM_COLUMNS_IN_SECTION
        contracts.append(convert_contract(contract))
    return contracts


def convert_contract(contract: list[str]) -> Contract:
    return Contract(
        code=convert_empty_strings(contract[-14]),
        name=convert_empty_strings(contract[-13]),
        base=convert_empty_strings(contract[-12]),
        volume=convert_empty_values_to_zero(contract[-11]),
        amount=convert_empty_values_to_zero(contract[-10]),
        price_change_amount=convert_empty_strings(contract[-9]),
        price_change_ratio=convert_empty_strings(contract[-8]),
        price_min=convert_empty_strings(contract[-7]),
        price_avg=convert_empty_strings(contract[-6]),
        price_max=convert_empty_strings(contract[-5]),
        price_market=convert_empty_strings(contract[-4]),
        price_best_bid=convert_empty_strings(contract[-3]),
        price_best_call=convert_empty_strings(contract[-2]),
        num_of_lots=convert_empty_strings(contract[-1])
    )


def create_sections(all_values: list[str], sections: list[list[str]]) -> list[Section]:
    all_sections = []
    names = make_strings_from_all_values(all_values, search_value='Секция Биржи: ', prefix='Секция Биржи: ')
    metrixes = make_strings_from_all_values(all_values, search_value='Единица измерения: ', prefix='Единица измерения: ')
    section_index = 0
    for section in sections:
        all_sections.append(
            Section(
                name=names[section_index],
                metric=metrixes[section_index],
                contracts=get_contracts_from_section(section)
            )
        )
        section_index += 1
    return all_sections


def create_trade_day(all_values: list[str]) -> TradeDay:
    sections_indexes = get_sections_indexes(all_values)
    sections = get_raw_sections(all_values, sections_indexes)
    return TradeDay(
        day=get_day(all_values),
        sections=create_sections(all_values, sections)
    )
