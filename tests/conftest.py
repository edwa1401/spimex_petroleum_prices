import datetime
import io
import random
from random import randint

import pytest
import requests
from faker import Faker


@pytest.fixture
def make_code():
    def inner(
            product: str | None = None,
            basis: str | None = None,
            lot_size: str | None = None,
            shipment: str | None = None
    ):
        product = product or 'A592'
        basis = basis or 'UFM'
        lot_size = lot_size or '060'
        shipment = shipment or 'F'
        return product + basis + lot_size + shipment
    return inner


@pytest.fixture
def make_petroleum_price():
    def inner():
        return str(randint(30000, 100000))
    return inner


@pytest.fixture
def make_contract_str(make_code, make_petroleum_price):
    def inner(
            code: str | None = None,
            name: str | None = None,
            base: str | None = None,
            volume: str | None = None,
            amount: str | None = None,
            price_change_amount: str | None = None,
            price_change_ration: str | None = None,
            price_min: str | None = None,
            price_avg: str | None = None,
            price_max: str | None = None,
            price_market: str | None = None,
            price_best_bid: str | None = None,
            price_best_call: str | None = None,
            num_of_lot: str | None = None
    ):
        code = code or make_code
        name = name or 'Продукт (марка бензина/сорт ДТ), ст. отправления'
        base = base or 'жд станция / пункт налива / нефтебаза'
        volume = volume or str(randint(60, 1000))
        amount = amount or str(randint(100, 100000000))
        price_change_amount = price_change_amount or str(randint(60, 1000))
        price_change_ration = price_change_ration or str(random.uniform(0.1, 100.0))
        price_min = price_min or make_petroleum_price
        price_avg = price_avg or make_petroleum_price
        price_max = price_max or make_petroleum_price
        price_market = price_market or make_petroleum_price
        price_best_bid = price_best_bid or make_petroleum_price
        price_best_call = price_best_call or make_petroleum_price
        num_of_lot = num_of_lot or str(randint(0, 50))
        return [
            code, name, base, volume, amount, price_change_amount,
            price_change_ration, price_min, price_avg, price_max,
            price_market, price_best_bid, price_best_call, num_of_lot
        ]
    return inner


@pytest.fixture
def create_contracts_str(make_contract):
    def inner(num_of_contracts: int | None = None):
        num_of_contracts = num_of_contracts or 10
        return [make_contract for _ in range(num_of_contracts)]
    return inner


@pytest.fixture
def make_date_str():
    def inner(day: str | None = None):
        fake = Faker()
        day = day or datetime.datetime.strftime(fake.date_object(), '%d.%m.%Y')
        return day
    return inner


@pytest.fixture
def make_section_str(create_contracts_str):
    def inner(
            name: str | None = None,
            metrix: str | None = None,
            contracts: list[list[str]] | None = None
    ):
        name = name or 'Нефтепродукты» АО «СПбМТСБ'
        metrix = metrix or 'Метрическая тонна'
        contracts = contracts or create_contracts_str
        return [name, metrix, contracts]
    return inner


@pytest.fixture
def create_sections_str(make_section_str):
    def inner(num_of_sections: int | None = None):
        num_of_sections = num_of_sections or 2
        return [make_section_str for _ in range(num_of_sections)]
    return inner


@pytest.fixture
def make_trade_day_str(create_sections_str, make_date_str):
    def inner(day: str | None = None,
              sections: list[list[list[str]]] | None = None
              ):
        day = day or make_date_str
        sections = sections or create_sections_str
        return [day, sections]
    return inner


@pytest.fixture
def create_all_values(create_contracts_str, make_date_str):
    def inner(
            first_row: str | None = None,
            prefix_day: str | None = None,
            section_name_str: str | None = None,
            metric_str: str | None = None,
            last_column_header: str | None = None,
            total_line_contracts: str | None = None
    ):
        first_row = first_row or 'Бюллетень'
        prefix_day = prefix_day or 'Дата торгов: '
        day = make_date_str
        section_name_str = section_name_str or 'Секция Биржи: «Нефтепродукты» АО «СПбМТСБ»'
        metric_str = metric_str or 'Единица измерения: Метрическая тонна'
        last_column_header = 'Лучший\nспрос'
        contracts = create_contracts_str
        total_line_contracts = 'Итого:'
        all_values = [
            first_row,
            prefix_day,
            day,
            section_name_str,
            metric_str,
            last_column_header,
            ''.join(contracts),
            total_line_contracts,
            last_column_header,
            ''.join(contracts),
            total_line_contracts
        ]
        return all_values
    return inner


@pytest.fixture
def convert_bytes_from_str():
    def inner(value: str | None):
        value = value or 'anything'
        return value.encode()
    return inner


@pytest.fixture
def make_request_response(convert_bytes_from_str):
    def inner(
            value: str | None = None
    ):
        response = requests.Response()
        response.status_code = 200
        response.raw = io.BytesIO(convert_bytes_from_str(value=value))
        return response
    return inner
