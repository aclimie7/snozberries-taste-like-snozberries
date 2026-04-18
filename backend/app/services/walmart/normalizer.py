from ...models.product import NormalizedProduct, Store, ProductCategory, PriceBreakdown
from ...models.credit_card import CreditCardInput
from ...models.store_rewards import StoreRewardsProgram
from ..rewards import best_card_dollar_value, store_loyalty_savings


_GROCERY_PATH_KEYWORDS = {"dairy", "eggs", "produce", "fresh", "frozen", "bakery", "deli", "seafood", "breakfast", "juice", "coffee", "meat", "beef", "chicken", "pork"}


def _map_category(category_path: str) -> ProductCategory:
    path_lower = category_path.lower()
    if any(kw in path_lower for kw in _GROCERY_PATH_KEYWORDS):
        return ProductCategory.grocery
    return ProductCategory.general_merchandise


def normalize(
    raw: dict,
    quantity: int,
    cards: list[CreditCardInput],
    store_program: StoreRewardsProgram | None,
) -> NormalizedProduct:
    sale_price_raw = float(raw.get("salePrice", 0.0))
    msrp_raw = float(raw.get("msrp") or sale_price_raw)

    base = msrp_raw
    sale_price = sale_price_raw if sale_price_raw < msrp_raw else None
    after_sale = sale_price_raw

    category = _map_category(raw.get("categoryPath", ""))

    loyalty_savings, store_detail = store_loyalty_savings(store_program, after_sale, quantity)
    effective = round(after_sale - loyalty_savings, 4)

    spend = effective * quantity
    cc_val, cc_detail = best_card_dollar_value(cards, category.value, spend)
    final = round(effective - cc_val, 2)

    stock = raw.get("stock", "Available")
    in_stock = stock not in ("Out of Stock",)

    return NormalizedProduct(
        store=Store.walmart,
        product_id=str(raw["itemId"]),
        name=raw["name"],
        brand=raw.get("brandName", ""),
        upc=raw.get("upc"),
        size=raw.get("size", ""),
        image_url=raw.get("largeImage") or raw.get("thumbnailImage"),
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
        in_stock=in_stock,
        score=1.0,
    )
