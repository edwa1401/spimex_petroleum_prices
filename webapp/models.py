from dataclasses import dataclass
import enum
from datetime import date


class Metrics(enum.Enum):
    kg = 'kg'
    tn = 'tn'


@dataclass
class TradeInstrument:
    code: str
    name: str
    base: str
    volume: int
    amount: int
    price_change: int
    price_min: int
    price_max: int
    price_market: int
    num_of_contracts: int


@dataclass
class Section:
    name: str
    metric: Metrics
    contracts: list[TradeInstrument]


@dataclass
class TradeDay:
    day: date
    sections: list[Section]
