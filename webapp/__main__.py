import logging

import uvicorn
from fastapi import FastAPI

from webapp.prices import get_products_from_trade_day
from webapp.spimex.spimex_parser import (create_trade_day,
                                         delete_all_emty_values_from_raw_data,
                                         download_file_from_spimex,
                                         get_all_cell_values_from_sheet,
                                         get_url_to_spimex_data,
                                         read_spimex_file)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/spimex_prices')
def get_spimex_trade_day(date: str) -> dict:
    logging.basicConfig(level=logging.INFO)

    logger.info('app started')

    url = get_url_to_spimex_data(date=date)
    content = download_file_from_spimex(url)
    sheet = read_spimex_file(content)
    raw_data = get_all_cell_values_from_sheet(sheet)
    all_values = delete_all_emty_values_from_raw_data(raw_data)
    trade_day = create_trade_day(all_values)
    trade_day_products = get_products_from_trade_day(trade_day)
    logger.info(trade_day_products)

    return {
        'Результаты торгов на СБМТСБ за ': trade_day.day,
        'Количество видов нефтепродуктов в разрезе базисов': len(trade_day_products),

        'Результат продаж по продукту': trade_day_products[100].product_key.name,
        'базис поставки': trade_day_products[300].product_key.base,
        'проданный объем': trade_day_products[300].volume,
        'ед. измерений': trade_day_products[300].metric,
        'на сумму, руб': trade_day_products[300].amount
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)
