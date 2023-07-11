from collections import defaultdict

from webapp.domain import Product, ProductKey
from webapp.spimex.schemas import Contract, TradeDay


def get_product_key(contract: Contract) -> ProductKey:
    return ProductKey(
        name=contract.code[:4],
        base=contract.code[4:7],
    )


def get_contracts_volumes_sum(contracts: list[Contract]) -> dict[ProductKey, float]:
    products_volumes: dict[ProductKey, float] = defaultdict(float)

    for contract in contracts:
        products_key = get_product_key(contract)

        products_volumes[products_key] += float(contract.volume)

    return products_volumes


def get_contracts_amount_sum(contracts: list[Contract]) -> dict[ProductKey, float]:
    products_amounts: dict[ProductKey, float] = defaultdict(float)

    for contract in contracts:
        products_key = get_product_key(contract)

        products_amounts[products_key] += float(contract.amount)

    return products_amounts


def get_products_from_trade_day(trade_day: TradeDay) -> list[Product]:
    products = []
    for section in trade_day.sections:
        amounts = get_contracts_amount_sum(section.contracts)
        volumes = get_contracts_volumes_sum(section.contracts)
        for contract in section.contracts:
            product_key = get_product_key(contract)
            product = Product(
                product_key=product_key,
                volume=volumes[product_key],
                amount=amounts[product_key],
                day=trade_day.day,
                metric=section.metric
            )
            products.append(product)
    return products
