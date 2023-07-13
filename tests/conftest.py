import datetime
import io
import random
from random import randint
from datetime import date
import pytest
import requests
from faker import Faker

from webapp.spimex.schemas import Contract, TradeDay, Section
from webapp.domain import ProductKey, Product

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
def create_contract():
    def inner(
            code: str | None = None,
            name: str | None = None,
            base: str | None = None,
            volume: str | None = None,
            amount: str | None = None,
            price_change_amount: str | None = None,
            price_change_ratio: str | None = None,
            price_min: str | None = None,
            price_avg: str | None = None,
            price_max: str | None = None,
            price_market: str | None = None,
            price_best_bid: str | None = None,
            price_best_call: str | None = None,
            num_of_lots: str | None = None
    ):
        return Contract(
            code=code or 'A592UFM060F',
            name=name or 'Продукт (марка бензина/сорт ДТ), ст. отправления',
            base=base or 'жд станция / пункт налива / нефтебаза',
            volume=volume or str(120),
            amount=amount or str(240000),
            price_change_amount=price_change_amount or str(500),
            price_change_ratio=price_change_ratio or str(0.50),
            price_min=price_min or str(50000),
            price_avg=price_avg or str(60000),
            price_max=price_max or str(70000),
            price_market=price_market or str(60000),
            price_best_bid=price_best_bid or str(61000),
            price_best_call=price_best_call or str(59000),
            num_of_lots=num_of_lots or str(10)
        )
    return inner


@pytest.fixture
def create_product_key(create_contract):
    def inner(name: str | None = None,
              base: str | None = None,
              base_name: str | None = None):

        name = name or 'A595'
        base = base or 'RZN'
        base_name = base_name or 'жд станция'

        code = name + base + '060F'
        contract = create_contract(code=code, base=base_name)

        return ProductKey(
            name=contract.code[0:4],
            base=contract.code[4:7],
            base_name=contract.base
        )
    return inner


@pytest.fixture
def create_contracts_str(make_contract_str):
    def inner(num_of_contracts: int | None = None):
        num_of_contracts = num_of_contracts or 10
        return [make_contract_str for _ in range(num_of_contracts)]
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
        total_line_contracts = 'Итого:'
        contracts = create_contracts_str
        all_values = [
            first_row,
            prefix_day,
            day,
            section_name_str,
            metric_str,
            last_column_header,
            ''.join([contract for contract in contracts]),
            total_line_contracts,
            last_column_header,
            ''.join([contract for contract in contracts]),
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

@pytest.fixture
def make_date_str():
    def inner(day: str | None = None):
        fake = Faker()
        day = day or datetime.datetime.strftime(fake.date_object(), '%d.%m.%Y')
        return day
    return inner


@pytest.fixture
def make_date():
    def inner(day: str | None = None):
        fake = Faker()
        day = day or datetime.datetime.strftime(fake.date_object(), '%d.%m.%Y')
        return datetime.datetime.strptime(day, '%d.%m.%Y')
    return inner


@pytest.fixture
def create_trade_day(create_contract, make_date):
    def inner(day: str | None = None,
              section_names: list[str] | None = None,
              section_metrics: list[str] | None = None,
              contracts: list[list[Contract], list[Contract]] | None = None,
              ):
        day = make_date(day) or make_date('07.07.2023')
        
        section_names = section_names or ['«Нефтепродукты» АО «СПбМТСБ»', '«Нефтепродукты» АО «СПбМТСБ»']
        section_metrics = section_metrics or ['Килограмм', 'Метрическая тонна']

        contracts = contracts or [
            [
                create_contract(code='A592AASK01O', base='НБ Карасунская', volume='10000', amount='3000000.5'),
                create_contract(code='A592AAS060A', base='НБ Карасунская', volume='20000', amount='7000000.5')
            ],
            [
                create_contract(code='A592ACH005A', base='Ачинский НПЗ', volume='100', amount='6330000'),
                create_contract(code='A592ACH005A', base='Ачинский НПЗ', volume='200', amount='3770000.5')
            ]
        ]
        return TradeDay(
            day=day,
            sections=[
                Section(
                    name=section_names[0],
                    metric=section_metrics[0],
                    contracts=contracts[0]
                ),
                Section(
                    name=section_names[1],
                    metric=section_metrics[1],
                    contracts=contracts[1]
                ),
            ]
        )
    return inner


@pytest.fixture
def create_product(create_product_key, make_date):
    def inner(
            product_key: ProductKey | None = None,
            volume: float | None = None,
            amount: float | None = None,
            metric: str | None = None,
            day: str | None = None
    ):
        product_key = product_key or create_product_key(name='A592', base='ACH', base_name='НПЗ')
        volume = volume or 100.05
        amount = amount or 5000000.95
        metric = metric or 'Метрическая тонна'
        day = make_date(day) or make_date('07.07.2023')

        return Product(
            product_key=product_key,
            volume=volume,
            amount=amount,
            metric=metric,
            day=day
        )
    return inner
