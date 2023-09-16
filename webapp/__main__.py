import logging

import uvicorn
from fastapi import FastAPI

from webapp.prices import (get_petroleums_filtered_by_basis_sort,
                           get_petroleums_from_products, get_products_from_db)
from webapp.spimex.loader import (delete_trade_day_from_db, get_days,
                                  get_petroleum_from_db, get_trade_day_from_db,
                                  save_petroleums_to_db, save_trade_day_to_db)
from webapp.spimex.spimex_parser import get_date, get_rail_tariff_from_spimex

logger = logging.getLogger(__name__)

app = FastAPI()


def get_tariff() -> None:
    logging.basicConfig(level=logging.INFO)
    tariff = get_rail_tariff_from_spimex(station_from='223108', station_to='198103', cargo='21105')
    logger.info(tariff)


def save_data_to_db() -> None:
    logging.basicConfig(level=logging.INFO)

    day = '2023-09-04'
    save_trade_day_to_db(day)
    save_petroleums_to_db(day)
    delete_trade_day_from_db(day)


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    logger.info('db started')

    days = ['2023-08-17', '2023-08-18']

    base_name = 'ст. Новоярославская'
    sort = 'AI95'

    dates = get_days(days)
    extracted_petroleums = get_petroleum_from_db(days=dates, base_name=base_name, sort=sort)

    logger.info(extracted_petroleums)


@app.get('/spimex_prices')
def get_spimex_trade_day(date: str, basis_name: str, sort: str) -> dict:
    logging.basicConfig(level=logging.INFO)

    logger.info('app started')

    day = get_date(date=date)
    trade_day_extracted_from_db = get_trade_day_from_db(day)
    products = get_products_from_db(trade_day_extracted_from_db)

    petroleums = get_petroleums_from_products(products)
    petroleum_filtered = get_petroleums_filtered_by_basis_sort(petroleums, basis_name=basis_name, sort=sort)

    logger.info(petroleum_filtered)

    return {
        'Trading results on commodity exchange SPIMEX for ': petroleum_filtered[0].day,
        'Results of trade on basis :': basis_name,

        'Product ': petroleum_filtered[0].sort,
        'Volumes sold': petroleum_filtered[0].volume,
        'metric ': petroleum_filtered[0].metric,
        'price, rub/tn': petroleum_filtered[0].price,
        'or ret. price, rub/l': petroleum_filtered[0].retail_price,
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)
    get_tariff()
