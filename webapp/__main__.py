import logging

import uvicorn
from fastapi import FastAPI

from webapp.spimex.spimex_parser import (create_trade_day,
                                         delete_all_emty_values_from_raw_data,
                                         download_file_from_spimex,
                                         get_all_cell_values_from_sheet,
                                         get_url_to_spimex_data,
                                         read_spimex_file)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/spimex prices')
def get_spimex_trade_day(date: str) -> dict:
    logging.basicConfig(level=logging.INFO)

    logger.info('app started')

    url = get_url_to_spimex_data(date=date)
    content = download_file_from_spimex(url)
    sheet = read_spimex_file(content)
    raw_data = get_all_cell_values_from_sheet(sheet)
    all_values = delete_all_emty_values_from_raw_data(raw_data)
    trade_day = create_trade_day(all_values)

    logger.info(trade_day)

    return {
        'Результаты торгов на СБМТСБ за ': trade_day.day,
        'в секции ': trade_day.sections[1].name,
        'единица измерений': trade_day.sections[1].metric,
        'число контрактов в секции': len(trade_day.sections[1].contracts)
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)
