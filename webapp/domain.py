import enum
from dataclasses import dataclass
from datetime import date

# TODO добавить группы Бензины и ДТ с основными октанами/ сортами
# аггрегацию продуктов по бензинам (октаны) и дт (сорта), присваивание плотности и
# суммирование amount и volume по признаку октан / базис


class Petroleums(enum.Enum):
    GASOLINE = 'Бензины'
    GASOIL = 'ДТ'
    OTHER_PRODUCT = 'Прочее'


class Shipment(enum.Enum):
    FREE_ON_RAIL = 'Франко-вагон станция отправления'
    FREE_ON_RAIL_LWS = 'Франко-вагон станция отправления ОПТ'
    EX_WORKS_ON_RAIL = 'Самовывоз железнодорожным транспортом'
    FREE_IN_PIPE = 'Франко-труба'
    OTHER_SHIPMENT = 'Прочие'


class Metrics(enum.Enum):
    KG = 'Килограмм'
    TN = 'Метрическая тонна'


@dataclass(frozen=True, kw_only=True, slots=True)
class Basis:
    code: str
    name: str
    full_name: str | None


@dataclass(frozen=True, kw_only=True, slots=True)
class Product:
    product_name: str
    basis: Basis
    lot_size: str
    shipment: str
    petroleum_type: Petroleums
    volume: int
    amount: int
    metrix: Metrics
    day: date
    density: float

    def calculate_price(self, amount: int, volume: int) -> float | None:
        price = amount / volume if amount and volume else None
        return price

    def calculate_retail_price(self, density: float, price: float) -> float | None:
        return price * density / 1000 if price else None
