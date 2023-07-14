from collections import defaultdict

from webapp.domain import Product, ProductKey, Petroleum, PetroleumSort
from webapp.spimex.schemas import Contract, TradeDay


def get_product_key(contract: Contract) -> ProductKey:
    return ProductKey(
        name=contract.code[:4],
        base=contract.code[4:7],
        base_name=contract.base
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
    products: dict[ProductKey, Product] = {}
    for section in trade_day.sections:
        amounts = get_contracts_amount_sum(section.contracts)
        volumes = get_contracts_volumes_sum(section.contracts)
        for contract in section.contracts:
            product_key = get_product_key(contract)
            if product_key in products:
                continue

            product = Product(
                product_key=product_key,
                volume=volumes[product_key],
                amount=amounts[product_key],
                day=trade_day.day,
                metric=section.metric
            )
            products[product_key] = product
    return list(products.values())


def get_petroleum_map() -> dict[str, PetroleumSort]:
    petroleum_sorts = {
        PetroleumSort.AI100: ['A001', 'A100', 'A106', 'AI01', 'A10K'],
        PetroleumSort.AI92: ['A592', 'A926', 'DM07', 'A92K', 'AR92', 'A925', 'DM01'],
        PetroleumSort.AI95: ['A595', 'A956', 'AIE6', 'A95K', 'DM02', 'A953'],
        PetroleumSort.AI98: ['A598', 'A98K', 'A983'],
        PetroleumSort.DTL: [
            'DST5', 'DST5', 'DT5L', 'DTSO', 'DTYS', 'DEC3', 'DSC5', 'DM03', 'DM09', 'DS5D', 'DTC5',
            'DTSR', 'DTCC', 'DTSN'],
        PetroleumSort.DTD: [
            'DTE3', 'DE5E', 'DM16', 'DE5F', 'DT6M', 'DE18', 'DTE6', 'DTUU', 'DT20', 'DTFE', 'DWF5'],
        PetroleumSort.DTZ: [
            'DT26', 'DT62', 'DT32', 'DTWX', 'DTZ2', 'DW32', 'DW35', 'DT38', 'DE05', 'DE13', 'DE15',
            'DE23', 'DW25', 'DM17', 'DE35', 'DTP6', 'DWK2', 'DTZ6', 'DTZM']
    }
    return {
        key: petroleum_sort
        for petroleum_sort, product_keys in petroleum_sorts.items()
        for key in product_keys
    }


def set_density_map() -> dict[PetroleumSort, float]:
    return {
        PetroleumSort.AI100: 0.75,
        PetroleumSort.AI92: 0.75,
        PetroleumSort.AI95: 0.75,
        PetroleumSort.AI98: 0.75,
        PetroleumSort.DTL: 0.84,
        PetroleumSort.DTD: 0.84,
        PetroleumSort.DTZ: 0.84,
        PetroleumSort.OTHER_PRODUCTS: 0.00
    }


def convert_product_to_petroleum(
        product: Product, petroleum_map: dict[str, PetroleumSort], density_map: dict[PetroleumSort, float]
) -> Petroleum:
    petroleum_sort = petroleum_map.get(product.product_key.name, PetroleumSort.OTHER_PRODUCTS)
    return Petroleum(
        product_key=product.product_key,
        volume=product.volume,
        amount=product.amount,
        metric=product.metric,
        day=product.day,
        sort=petroleum_sort,
        density=density_map[petroleum_sort]
    )


def transform_products_to_petroleums(
        products: list[Product], petroleum_map: dict[str, PetroleumSort],
        density_map: dict[PetroleumSort, float]
) -> list[Petroleum]:

    return [convert_product_to_petroleum(product, petroleum_map, density_map) for product in products]


def get_products_filtered_by_basis(products: list[Petroleum], basis_name: str) -> list[Petroleum]:
    return [product for product in products if product.product_key.base_name == basis_name]
