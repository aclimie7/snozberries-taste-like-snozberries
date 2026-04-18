from ...models.product import NormalizedProduct, Store, ProductCategory, PriceBreakdown
from ...models.credit_card import CreditCardInput
from ...models.store_rewards import StoreRewardsProgram
from ..rewards import best_card_dollar_value, store_loyalty_savings


_GROCERY_CATEGORIES = {"dairy", "meat", "produce", "bakery", "deli", "seafood", "breakfast", "juice", "coffee"}


def _map_category(categories: list[str]) -> ProductCategory:
    for cat in categories:
        if any(g in cat.lower() for g in _GROCERY_CATEGORIES):
            return ProductCategory.grocery
    return ProductCategory.grocery


def _pick_image(images: list[dict]) -> str | None:
    for img in images:
        if img.get("perspective") == "front":
            sizes = img.get("sizes", [])
            for s in sizes:
                if s.get("size") in ("medium", "large"):
                    return s.get("url")
            if sizes:
                return sizes[0].get("url")
    return None


def normalize(
    raw: dict,
    quantity: int,
    cards: list[CreditCardInput],
    store_program: StoreRewardsProgram | None,
) -> NormalizedProduct:
    item = raw["items"][0]
    prices = item.get("price", {})
    base = float(prices.get("regular", 0.0))
    promo = prices.get("promo")
    sale_price = float(promo) if promo else None
    after_sale = min(base, sale_price) if sale_price else base

    category = _map_category(raw.get("categories", []))

    loyalty_savings, store_detail = store_loyalty_savings(store_program, after_sale, quantity)
    effective = round(after_sale - loyalty_savings, 4)

    spend = effective * quantity
    cc_val, cc_detail = best_card_dollar_value(cards, category.value, spend)
    final = round(effective - cc_val, 2)

    return NormalizedProduct(
        store=Store.kroger,
        product_id=raw["productId"],
        name=raw["description"],
        brand=raw.get("brand", ""),
        upc=raw.get("upc"),
        size=item.get("size", ""),
        image_url=_pick_image(raw.get("images", [])),
        category=category,
        price=PriceBreakdown(
            base_price=base,
            sale_price=sale_price,
            coupon_savings=0.0,
            store_rewards_savings=loyalty_savings,
            effective_price=effective,
            cc_reward_value=cc_val,
            final_price=final,
            cc_reward_detail=cc_detail,
            store_reward_detail=store_detail,
        ),
        on_sale=sale_price is not None,
        has_digital_coupon=False,
        in_stock=item.get("inventory", {}).get("status") != "TEMPORARILY_UNAVAILABLE",
        score=1.0,
    )
