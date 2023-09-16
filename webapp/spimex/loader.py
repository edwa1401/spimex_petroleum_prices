
from datetime import datetime, date

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from webapp.domain import Petroleum
from webapp.prices import get_petroleums_from_products, get_products_from_db
from webapp.spimex.db import db_session, engine
from webapp.spimex.models import ContractDB, PetroleumDB, SectionDB, TradeDayDB
from webapp.spimex.schemas import Contract, TradeDay
from webapp.spimex.spimex_parser import (convert_date, create_trade_day,
                                         delete_all_emty_values_from_raw_data,
                                         download_file_from_spimex,
                                         get_all_cell_values_from_sheet,
                                         get_date, get_url_to_spimex_data,
                                         read_spimex_file)


def save_trade_day(trade_day: TradeDay) -> TradeDayDB:
    trade_day_db = TradeDayDB(day=trade_day.day)
    db_session.add(trade_day_db)
    db_session.commit()
    return trade_day_db


def save_contract(contract: Contract) -> ContractDB:
    return ContractDB(
        code=contract.code,
        name=contract.code,
        base=contract.base,
        volume=contract.volume,
        amount=contract.amount,
        price_change_amount=contract.price_change_amount,
        price_change_ratio=contract.price_change_ratio,
        price_min=contract.price_min,
        price_avg=contract.price_avg,
        price_max=contract.price_max,
        price_market=contract.price_market,
        price_best_bid=contract.price_best_bid,
        price_best_call=contract.price_best_call,
        num_of_lots=contract.num_of_lots
    )


def save_spimex_trade_day(trade_day: TradeDay) -> TradeDayDB:

    trade_day_db = TradeDayDB(day=trade_day.day)
    sections_db = []
    for section in trade_day.sections:
        contracts_db = []
        section_db = SectionDB(name=section.name, metric=section.metric)

        for contract in section.contracts:
            contract_db = save_contract(contract)
            contracts_db.append(contract_db)

        section_db.contracts = contracts_db
        sections_db.append(section_db)

    trade_day_db.sections = sections_db

    db_session.add(trade_day_db)
    try:
        db_session.commit()
    except SQLAlchemyError:
        db_session.rollback()
        raise

    return trade_day_db


def save_trade_day_to_db(raw_day: str) -> None:

    day = get_date(raw_day)
    converted_day = convert_date(day)
    url = get_url_to_spimex_data(date=converted_day)
    content = download_file_from_spimex(url)
    sheet = read_spimex_file(content)
    raw_data = get_all_cell_values_from_sheet(sheet)
    all_values = delete_all_emty_values_from_raw_data(raw_data)
    trade_day = create_trade_day(all_values)

    try:
        save_spimex_trade_day(trade_day)
    except (TypeError, ValueError) as e:
        f'Incorrect data format {e}'
    except SQLAlchemyError as e:
        f'Data integrity error {e}'

    # TODO сделать красивей обработку ошибок


def get_trade_day_from_db(day: date) -> TradeDayDB:
    trade_day_from_db = select(TradeDayDB).where(TradeDayDB.day == day)
    session = Session(engine)
    return session.scalars(trade_day_from_db).one()


def delete_trade_day_from_db(raw_day: str) -> None:
    day = get_date(raw_day)
    trade_day_to_delete = db_session.query(TradeDayDB).filter_by(day=day).first()
    db_session.delete(trade_day_to_delete)
    db_session.commit()


def save_peroleumDB(petroleum: Petroleum) -> PetroleumDB:
    return PetroleumDB(
        product_key=petroleum.product_key.name,
        base=petroleum.product_key.base,
        base_name=petroleum.product_key.base_name,
        volume=petroleum.volume,
        amount=petroleum.amount,
        metric=petroleum.metric,
        day=petroleum.day,
        sort=petroleum.sort.value,
        density=petroleum.density,
        price=petroleum.price,
        retail_price=petroleum.retail_price
    )


def save_petroleums_to_db(raw_day: str) -> None:
    day = get_date(raw_day)
    trade_day_extracted_from_db = get_trade_day_from_db(day)
    products = get_products_from_db(trade_day_extracted_from_db)
    petroleums = get_petroleums_from_products(products)
    petroleumsDB = [save_peroleumDB(petroleum) for petroleum in petroleums]
    db_session.add_all(petroleumsDB)
    db_session.commit()


def get_petroleum_from_db(days: list[date], base_name: str, sort: str) -> list[PetroleumDB]:

    petroleums = select(PetroleumDB).where(
        PetroleumDB.day.in_(days), PetroleumDB.base_name == base_name, PetroleumDB.sort == sort
    )
    session = Session(engine)
    return [petroleum for petroleum in session.scalars(petroleums)]


def get_days(days: list[str]) -> list[date]:
    return [datetime.date(datetime.strptime(day, '%Y-%m-%d')) for day in days]
