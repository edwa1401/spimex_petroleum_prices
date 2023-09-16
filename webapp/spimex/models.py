
import logging

from sqlalchemy import Column, ForeignKey, Integer, Float, String, Date
from sqlalchemy.orm import relationship

from webapp.spimex.db import engine, Base

logger = logging.getLogger(__name__)


class TradeDayDB(Base):
    __tablename__ = 'trade_day'

    id = Column(Integer, primary_key=True)
    day = Column(Date, unique=True, nullable=False)
    sections = relationship('SectionDB', back_populates='trade_day', cascade='all, delete', passive_deletes=True)

    def __repr__(self) -> str:
        return f'TradeDayDB(id={self.id}, day={self.day}, sections={self.sections})'


class SectionDB(Base):
    __tablename__ = 'section'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    metric = Column(String, nullable=False)
    contracts = relationship('ContractDB', back_populates='section', cascade='all, delete', passive_deletes=True)
    trade_day_id = Column(Integer, ForeignKey('trade_day.id', ondelete='CASCADE'))
    trade_day = relationship('TradeDayDB', back_populates='sections')

    def __repr__(self) -> str:
        return f'Section_db(id={self.id}, name={self.name}, metric={self.metric}, contracts={self.contracts})'


class ContractDB(Base):
    __tablename__ = 'contract'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    base = Column(String, nullable=False)
    volume = Column(String, nullable=False)
    amount = Column(String, nullable=False)
    price_change_amount = Column(String)
    price_change_ratio = Column(String)
    price_min = Column(String)
    price_avg = Column(String)
    price_max = Column(String)
    price_market = Column(String)
    price_best_bid = Column(String)
    price_best_call = Column(String)
    num_of_lots = Column(String)

    section_id = Column(Integer, ForeignKey('section.id', ondelete='CASCADE'))
    section = relationship('SectionDB', back_populates='contracts')

    def __repr__(self) -> str:
        return f'ContractDB(id={self.id}, code={self.code}, name={self.name}, base={self.base}, \
            volume={self.volume}, amount={self.amount}), price_change_amount={self.price_change_amount}, \
            price_change_ratio={self.price_change_ratio}, price_min={self.price_min}, price_avg={self.price_avg}, \
            price_max={self.price_max}, price_market={self.price_market}, price_best_bid={self.price_best_bid}, \
            price_best_call={self.price_best_call}, num_of_lots={self.num_of_lots}'


class PetroleumDB(Base):
    __tablename__ = 'petroleum'

    id = Column(Integer, primary_key=True)
    product_key = Column(String(4), nullable=False)
    base = Column(String(3), nullable=False)
    base_name = Column(String, nullable=False)
    volume = Column(Float)
    amount = Column(Float)
    metric = Column(String, nullable=False)
    day = Column(Date, nullable=False)
    sort = Column(String, nullable=False)
    density = Column(Float)
    price = Column(Float)
    retail_price = Column(Float)

    def __repr__(self) -> str:
        return f'PetroleumDB(id={self.id}, product_key={self.product_key}, sort={self.sort}, base_name={self.base_name}, \
            metric={self.metric}, day={self.day}, volume={self.volume}, price={self.price}, retali_price={self.retail_price})'


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    logger.info('started')
    Base.metadata.create_all(bind=engine)
