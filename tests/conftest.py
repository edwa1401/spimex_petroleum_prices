from random import randint
from typing import Any
import random


def make_code():
    def inner(
            product: str | None = None,
            basis: str | None = None,
            lot_size: str | None = None,
            shipment: str | None = None
    ):
        product = product or 'A592'
        basis = basis or 'UFM'
        lot_size = lot_size or '060'
        shipment = shipment or 'F'
        return product + basis + lot_size + shipment
    return inner


def make_petroleum_price():
    def inner():
        return str(randint(30000, 100000))
    return inner


def make_contract(make_code, make_petroleum_price):
    def inner(
            code: Any | None = None,
            name: str | None = None,
            base: str | None = None,
            volume: str | None = None,
            amount: str | None = None,
            price_change_amount: str | None = None,
            price_change_ration: str | None = None,
            price_min: str | None = None,
            price_avg: str | None = None,
            price_max: str | None = None,
            price_market: str | None = None,
            price_best_bid: str | None = None,
            price_best_call: str | None = None,
            num_of_lot: str | None = None
    ):
        code = code or make_code
        name = name or 'Продукт (марка бензина/сорт ДТ), ст. отправления'
        base = base or 'жд станция / пункт налива / нефтебаза'
        volume = volume or str(randint(60, 1000))
        amount = amount or str(randint(100, 100000000))
        price_change_amount = price_change_amount or str(randint(60, 1000))
        price_change_ration = price_change_ration or str(random.uniform(0.1, 100.0))
        price_min = price_min or make_petroleum_price
        price_avg = price_avg or make_petroleum_price
        price_max = price_max or make_petroleum_price
        price_market = price_market or make_petroleum_price
        price_best_bid = price_best_bid or make_petroleum_price
        price_best_call = price_best_call or make_petroleum_price
        num_of_lot = num_of_lot or str(randint(0, 50))
        return [
            code, name, base, volume, amount, price_change_amount,
            price_change_ration, price_min, price_avg, price_max,
            price_market, price_best_bid, price_best_call, num_of_lot
        ]
    return inner
