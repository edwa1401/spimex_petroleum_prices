import enum
from dataclasses import dataclass
from datetime import date


class PetroleumSort(enum.Enum):
    AI100 = 'Бензин Аи-100'
    AI98 = 'Бензин Аи-98'
    AI95 = 'Бензин Аи-95'
    AI92 = 'Бензин Аи-92'
    DTL = 'Дизельное топливо Летнее'
    DTD = 'Дизельное топливо Демисезонное'
    DTZ = 'Дизельное топливо Зимнее'
    OTHER_PRODUCTS = 'Прочие продукты'


class Shipment(enum.Enum):
    FREE_ON_RAIL = 'Франко-вагон станция отправления'
    FREE_ON_RAIL_LWS = 'Франко-вагон станция отправления ОПТ'
    EX_WORKS_ON_RAIL = 'Самовывоз железнодорожным транспортом'
    FREE_IN_PIPE = 'Франко-труба'
    OTHER_SHIPMENT = 'Прочие'


class Metric(enum.Enum):
    KG = 'Килограмм'
    TN = 'Метрическая тонна'


@dataclass(frozen=True, kw_only=True, slots=True)
class Basis:
    code: str
    name: str
    full_name: str | None


@dataclass(frozen=True, kw_only=True, slots=True)
class ProductKey:
    name: str
    base: str
    base_name: str


@dataclass(frozen=True, kw_only=True, slots=True)
class Product:
    product_key: ProductKey
    volume: float
    amount: float
    metric: str
    day: date


@dataclass(frozen=True, kw_only=True, slots=True)
class Petroleum(Product):
    sort: PetroleumSort
    density: float

    @property
    def price(self) -> float | None:
        return round(self.amount / self.volume, 2) if self.amount and self.volume else None

    @property
    def retail_price(self) -> float | None:
        return round(self.price * self.density / 1000, 2) if self.price else None
