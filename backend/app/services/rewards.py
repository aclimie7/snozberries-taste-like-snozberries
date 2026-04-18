from ..models.credit_card import CreditCardInput, RewardType
from ..models.store_rewards import StoreRewardsProgram
from ..models.product import Store


def card_dollar_value(card: CreditCardInput, category: str, spend: float) -> float:
    rate = card.earn_rates.get(category, card.earn_rates.get("default", 0.0))
    if card.reward_type == RewardType.cashback:
        return round(spend * rate, 4)
    else:
        points_earned = spend * rate
        return round(points_earned * (card.cents_per_point / 100), 4)


def best_card_dollar_value(
    cards: list[CreditCardInput], category: str, spend: float
) -> tuple[float, str]:
    best_val = 0.0
    best_detail = ""
    for card in cards:
        if not card.is_active:
            continue
        val = card_dollar_value(card, category, spend)
        if val > best_val:
            best_val = val
            if card.reward_type == RewardType.cashback:
                rate = card.earn_rates.get(category, card.earn_rates.get("default", 0.0))
                best_detail = f"{card.name}: {rate * 100:.1f}% cashback = ${val:.2f}"
            else:
                rate = card.earn_rates.get(category, card.earn_rates.get("default", 0.0))
                best_detail = (
                    f"{card.name}: {rate:.0f}x pts × ${spend:.2f} "
                    f"@ {card.cents_per_point:.1f}¢/pt = ${val:.2f} value"
                )
    return round(best_val, 2), best_detail


def store_loyalty_savings(
    program: StoreRewardsProgram | None,
    pre_loyalty_price: float,
    qty: int,
) -> tuple[float, str]:
    if not program or not program.enrolled:
        return 0.0, ""

    subtotal = pre_loyalty_price * qty

    if program.store == Store.walmart:
        savings = round(program.store_cashback_rate * subtotal, 2)
        return savings, f"Walmart+ {program.store_cashback_rate * 100:.0f}% = ${savings:.2f}"

    if program.store == Store.kroger:
        pts = int(subtotal * program.fuel_points_per_dollar)
        return 0.0, f"Kroger Plus: member price + {pts} fuel pts"

    return 0.0, ""


def find_program(
    programs: list[StoreRewardsProgram], store: Store
) -> StoreRewardsProgram | None:
    for p in programs:
        if p.store == store:
            return p
    return None
