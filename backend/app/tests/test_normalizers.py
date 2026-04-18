import pytest
from ..models.credit_card import CreditCardInput, RewardType
from ..services.kroger.normalizer import normalize as kroger_normalize
from ..services.walmart.normalizer import normalize as walmart_normalize


RAW_KROGER = {
    "productId": "0001111041700",
    "description": "Organic Whole Milk",
    "brand": "Simple Truth",
    "upc": "0001111041700",
    "categories": ["Dairy"],
    "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "http://example.com/milk.jpg"}]}],
    "items": [{"size": "1 gal", "price": {"regular": 5.49, "promo": 4.79}, "inventory": {"status": "AVAILABLE"}}],
}

RAW_WALMART = {
    "itemId": 10452064,
    "name": "Great Value Whole Milk",
    "brandName": "Great Value",
    "upc": "0078742365169",
    "size": "1 gal",
    "salePrice": 3.48,
    "msrp": 3.48,
    "categoryPath": "Food/Dairy & Eggs/Milk",
    "largeImage": "http://example.com/milk.jpg",
    "stock": "Available",
}

NO_CARDS: list[CreditCardInput] = []


class TestKrogerNormalizer:
    def test_basic_fields(self):
        product = kroger_normalize(RAW_KROGER, 1, NO_CARDS, None)
        assert product.store.value == "kroger"
        assert product.name == "Organic Whole Milk"
        assert product.brand == "Simple Truth"
        assert product.size == "1 gal"
        assert product.in_stock is True

    def test_sale_price_detection(self):
        product = kroger_normalize(RAW_KROGER, 1, NO_CARDS, None)
        assert product.on_sale is True
        assert product.price.sale_price == 4.79
        assert product.price.base_price == 5.49
        assert product.price.effective_price == 4.79

    def test_no_cards_zero_reward(self):
        product = kroger_normalize(RAW_KROGER, 1, NO_CARDS, None)
        assert product.price.cc_reward_value == 0.0
        assert product.price.final_price == product.price.effective_price

    def test_cashback_card_reduces_final_price(self):
        card = CreditCardInput(
            id="c1", name="Test", reward_type=RewardType.cashback,
            earn_rates={"grocery": 0.06, "default": 0.01}, cents_per_point=1.0, is_active=True,
        )
        product = kroger_normalize(RAW_KROGER, 1, [card], None)
        expected_reward = round(4.79 * 0.06, 2)
        assert product.price.cc_reward_value == expected_reward
        assert product.price.final_price < product.price.effective_price

    def test_quantity_multiplies_reward(self):
        card = CreditCardInput(
            id="c1", name="Test", reward_type=RewardType.cashback,
            earn_rates={"grocery": 0.05, "default": 0.01}, cents_per_point=1.0, is_active=True,
        )
        p1 = kroger_normalize(RAW_KROGER, 1, [card], None)
        p2 = kroger_normalize(RAW_KROGER, 3, [card], None)
        assert round(p2.price.cc_reward_value / p1.price.cc_reward_value, 1) == 3.0


class TestWalmartNormalizer:
    def test_basic_fields(self):
        product = walmart_normalize(RAW_WALMART, 1, NO_CARDS, None)
        assert product.store.value == "walmart"
        assert product.name == "Great Value Whole Milk"
        assert product.brand == "Great Value"
        assert product.in_stock is True

    def test_no_sale_when_msrp_equals_sale_price(self):
        product = walmart_normalize(RAW_WALMART, 1, NO_CARDS, None)
        assert product.on_sale is False
        assert product.price.sale_price is None

    def test_sale_detected_when_sale_lower_than_msrp(self):
        raw = {**RAW_WALMART, "salePrice": 2.98, "msrp": 3.48}
        product = walmart_normalize(raw, 1, NO_CARDS, None)
        assert product.on_sale is True
        assert product.price.sale_price == 2.98
        assert product.price.effective_price == 2.98

    def test_category_grocery_for_dairy(self):
        product = walmart_normalize(RAW_WALMART, 1, NO_CARDS, None)
        assert product.category.value == "grocery"

    def test_category_general_merchandise(self):
        raw = {**RAW_WALMART, "categoryPath": "Electronics/TVs"}
        product = walmart_normalize(raw, 1, NO_CARDS, None)
        assert product.category.value == "general_merchandise"

    def test_out_of_stock(self):
        raw = {**RAW_WALMART, "stock": "Out of Stock"}
        product = walmart_normalize(raw, 1, NO_CARDS, None)
        assert product.in_stock is False
