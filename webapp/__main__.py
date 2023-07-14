import logging

import uvicorn
from fastapi import FastAPI

from webapp.prices import (get_products_from_trade_day, set_density_map,
                           get_petroleum_map, transform_products_to_petroleums, get_products_filtered_by_basis)
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
    petrol_map = get_petroleum_map()
    density_map = set_density_map()
    petroleums = transform_products_to_petroleums(trade_day_products, petrol_map, density_map)
    basis_name = 'ст. Стенькино II'
    ryazan = get_products_filtered_by_basis(petroleums, basis_name=basis_name)
    logger.info(ryazan)

    return {
        'Результаты торгов на СБМТСБ за ': ryazan[3].day,
        'Результат продаж на базисе ': basis_name,

        'Автобензин ': ryazan[2].sort,
        'Проданный объем ': ryazan[2].volume,
        'ед. измерений ': ryazan[2].metric,
        'по цене, руб/т ': ryazan[2].price,
        'что эквивалентно розничной цене, руб/л ': ryazan[2].retail_price,

        'ДТ ': ryazan[3].sort,
        'на сумму ': ryazan[3].amount,
        'ед. изм ': ryazan[3].metric,
        'опт. цена, руб/т ': ryazan[3].price,
        'розничная цена, руб/т': ryazan[3].retail_price
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)
