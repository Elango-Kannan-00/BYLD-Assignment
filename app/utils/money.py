from decimal import Decimal, ROUND_HALF_UP

MONEY_QUANTUM = Decimal("0.0001")


def to_money(value: Decimal | int | str) -> Decimal:
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    return value.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def money_mul(quantity: int, price: Decimal) -> Decimal:
    return to_money(Decimal(quantity) * price)
