# import random
# import string
# from random import randint

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

# def make_contract(make_code):
#     def inner(
#             code: str | None = None,
#             base: str | None = None,
#             volume: str | None = None,
#             amount: str | None = None,
#             price_change_amount: str | None = None,
#             price_change_ration: str | None = None,
#             price_min: str | None = None,
#             price_avg: str | None = None,
#             price_max: str | None = None,
#             price_market: str | None = None,
#             price_best_bid: str | None = None,
#             price_best_call: str | None = None,
#             num_of_lot: str | None = None
#             ):
#         code = code or make_code,

