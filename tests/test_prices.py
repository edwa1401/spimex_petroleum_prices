import pytest
from webapp.prices import get_product_key, get_contracts_volumes_sum, get_contracts_amount_sum, get_products_from_trade_day


def test__get_product_key__succes(create_contract, create_product_key):
    contract = create_contract(code='A592ABE010A', base='НБ Абзелиловская')

    expected = create_product_key(name='A592', base='ABE', base_name='НБ Абзелиловская')

    assert get_product_key(contract) == expected


def test__get_product_key__fail_return_error_for_different_values(create_contract, create_product_key):
    contract = create_contract(code='A592ABE010A', base='НБ Абзелиловская')

    expected = create_product_key(name='A595', base='ABE', base_name='НБ Абзелиловская')

    with pytest.raises(AssertionError):
        assert get_product_key(contract=contract) == expected


def test__get_contracts_volumes_sum__sucess(create_contract, create_product_key):
    contract_1 = create_contract(code='A592ABE010A', base='жд станция', volume='100')
    contract_2 = create_contract(code='A592ABE060F', base='жд станция', volume='200')
    contract_3 = create_contract(code='DSC5SAU065F', base='нефтебаза', volume='1000')
    contract_4 = create_contract(code='DSC5SAU065F', base='нефтебаза', volume='3000')

    contracts = [contract_1, contract_2, contract_3, contract_4]

    product_key_1 = create_product_key(name='A592', base='ABE', base_name='жд станция')
    product_key_2 = create_product_key(name='DSC5', base='SAU', base_name='нефтебаза')

    expected = {product_key_1: 300.0, product_key_2: 4000.00}

    assert get_contracts_volumes_sum(contracts) == expected


def test__get_contracts_volumes_sum__fail_diff_in_base_name(create_contract, create_product_key):
    contract_1 = create_contract(code='A592ABE010A', base='жд станция', volume='100')
    contract_2 = create_contract(code='A592ABE060F', base='нефтебаза', volume='200')

    contracts = [contract_1, contract_2]

    product_key_1 = create_product_key(name='A592', base='ABE', base_name='жд станция')

    expected = {product_key_1: 300.0}

    with pytest.raises(AssertionError):
        assert get_contracts_volumes_sum(contracts) == expected


def test__get_contracts_volumes_sum__fail_diff_in_code_name(create_contract, create_product_key):
    contract_1 = create_contract(code='A592ABE010A', base='жд станция', volume='100')
    contract_2 = create_contract(code='A595ABE060F', base='жд станция', volume='200')

    contracts = [contract_1, contract_2]

    product_key_1 = create_product_key(name='A592', base='ABE', base_name='жд станция')

    expected = {product_key_1: 300.0}

    with pytest.raises(AssertionError):
        assert get_contracts_volumes_sum(contracts) == expected


def test__get_contracts_amount_sum__sucess(create_contract, create_product_key):
    contract_1 = create_contract(code='A593BCD010A', base='станция', amount='300')
    contract_2 = create_contract(code='A593BCD060F', base='станция', amount='400')
    contract_3 = create_contract(code='DSZ5SAU065F', base='база', amount='200')
    contract_4 = create_contract(code='DSZ5SAU065F', base='база', amount='200')

    contracts = [contract_1, contract_2, contract_3, contract_4]

    product_key_1 = create_product_key(name='A593', base='BCD', base_name='станция')
    product_key_2 = create_product_key(name='DSZ5', base='SAU', base_name='база')

    expected = {product_key_1: 700.0, product_key_2: 400.00}

    assert get_contracts_amount_sum(contracts) == expected


def test__get_contracts_amount_sum__fail_diff_in_code_base(create_contract, create_product_key):
    contract_1 = create_contract(code='A593BCD060F', base='станция', amount='100')
    contract_2 = create_contract(code='A593BCE060F', base='станция', amount='200')

    contracts = [contract_1, contract_2]

    product_key_1 = create_product_key(name='A593', base='BCD', base_name='станция')

    expected = {product_key_1: 300.0}

    with pytest.raises(AssertionError):
        assert get_contracts_amount_sum(contracts) == expected


def test__get_products_from_trade_day__success(make_date_str, create_trade_day, create_contract, create_product, create_product_key):

    day = make_date_str('07.07.2023')

    section_names = ['«Нефтепродукты» АО «СПбМТСБ»', '«Нефтепродукты» АО «СПбМТСБ»']
    section_metrics = ['Килограмм', 'Метрическая тонна']

    contracts = [
        [
            create_contract(code='A592AASK01O', base='НБ Карасунская', volume='10000', amount='3000000.5'),
            create_contract(code='A592AAS060A', base='НБ Карасунская', volume='20000', amount='7000000.5')
        ],
        [
            create_contract(code='DTZ5ACH005A', base='Ачинский НПЗ', volume='100', amount='6230000'),
            create_contract(code='DTZ5ACH005A', base='Ачинский НПЗ', volume='200', amount='3770000.5')
        ]
    ]
    trade_day = create_trade_day(inp_day=day, section_names=section_names, section_metrics=section_metrics, contracts=contracts)

    product_key_1 = create_product_key(name='A592', base='AAS', base_name='НБ Карасунская')
    product_key_2 = create_product_key(name='DTZ5', base='ACH', base_name='Ачинский НПЗ')

    product_1 = create_product(product_key=product_key_1, volume=30000.00, amount=10000001.00, metric='Килограмм', inp_day=day)
    product_2 = create_product(product_key=product_key_2, volume=300.00, amount=10000000.5, metric='Метрическая тонна', inp_day=day)

    products = [product_1, product_2]

    assert get_products_from_trade_day(trade_day) == products
