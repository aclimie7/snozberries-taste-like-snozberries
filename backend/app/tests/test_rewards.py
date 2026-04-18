import pytest
from ..models.credit_card import CreditCardInput, RewardType
from ..models.store_rewards import StoreRewardsProgram
from ..models.product import Store
from ..services.rewards import (
    card_dollar_value,
    best_card_dollar_value,
    store_loyalty_savings,
    find_program,
)


def cashback_card(grocery=0.06, general=0.01, default=0.01) -> CreditCardInput:
    return CreditCardInput(
        id="c1", name="Test Cash", reward_type=RewardType.cashback,
        earn_rates={"grocery": grocery, "general_merchandise": general, "default": default},
        cents_per_point=1.0, is_active=True,
    )


def points_card(grocery=3.0, default=1.0, cpp=1.5) -> CreditCardInput:
    return CreditCardInput(
        id="c2", name="Test Points", reward_type=RewardType.points,
        earn_rates={"grocery": grocery, "default": default},
        cents_per_point=cpp, is_active=True,
    )


class TestCardDollarValue:
    def test_cashback_grocery(self):
        card = cashback_card(grocery=0.06)
        val = card_dollar_value(card, "grocery", 10.0)
        assert round(val, 4) == 0.6

    def test_cashback_uses_default_for_unknown_category(self):
        card = cashback_card(default=0.015)
        val = card_dollar_value(card, "unknown_cat", 100.0)
        assert round(val, 2) == 1.5

    def test_points_grocery(self):
        card = points_card(grocery=3.0, cpp=1.5)
        val = card_dollar_value(card, "grocery", 10.0)
        assert round(val, 4) == round(10.0 * 3.0 * (1.5 / 100), 4)

    def test_inactive_card_not_used(self):
        card = cashback_card(grocery=0.10)
        card.is_active = False
        val, detail = best_card_dollar_value([card], "grocery", 100.0)
        assert val == 0.0
        assert detail == ""


class TestBestCardDollarValue:
    def test_picks_higher_of_cashback_vs_points(self):
        cash = cashback_card(grocery=0.04)
        pts = points_card(grocery=3.0, cpp=2.0)
        val, detail = best_card_dollar_value([cash, pts], "grocery", 10.0)
        cash_val = 10.0 * 0.04
        pts_val = 10.0 * 3.0 * (2.0 / 100)
        assert val == round(max(cash_val, pts_val), 2)

    def test_empty_cards_returns_zero(self):
        val, detail = best_card_dollar_value([], "grocery", 50.0)
        assert val == 0.0

    def test_detail_string_cashback(self):
        card = cashback_card(grocery=0.05)
        val, detail = best_card_dollar_value([card], "grocery", 20.0)
        assert "5.0%" in detail
        assert "Test Cash" in detail

    def test_detail_string_points(self):
        card = points_card(grocery=3.0, cpp=1.5)
        _, detail = best_card_dollar_value([card], "grocery", 20.0)
        assert "3x" in detail
        assert "1.5" in detail


class TestStoreLoyaltySavings:
    def test_walmart_plus_1pct(self):
        prog = StoreRewardsProgram(
            store=Store.walmart, program_name="Walmart+",
            enrolled=True, store_cashback_rate=0.01, fuel_points_per_dollar=0,
        )
        savings, detail = store_loyalty_savings(prog, 10.0, 2)
        assert round(savings, 2) == 0.20
        assert "Walmart+" in detail

    def test_not_enrolled_returns_zero(self):
        prog = StoreRewardsProgram(
            store=Store.walmart, program_name="Walmart+",
            enrolled=False, store_cashback_rate=0.01, fuel_points_per_dollar=0,
        )
        savings, detail = store_loyalty_savings(prog, 10.0, 1)
        assert savings == 0.0
        assert detail == ""

    def test_kroger_plus_fuel_points_no_cash_savings(self):
        prog = StoreRewardsProgram(
            store=Store.kroger, program_name="Kroger Plus",
            enrolled=True, store_cashback_rate=0, fuel_points_per_dollar=1,
        )
        savings, detail = store_loyalty_savings(prog, 5.0, 2)
        assert savings == 0.0
        assert "fuel pts" in detail

    def test_none_program_returns_zero(self):
        savings, detail = store_loyalty_savings(None, 10.0, 1)
        assert savings == 0.0


class TestFindProgram:
    def test_finds_correct_store(self):
        programs = [
            StoreRewardsProgram(store=Store.kroger, program_name="K+", enrolled=True, store_cashback_rate=0, fuel_points_per_dollar=1),
            StoreRewardsProgram(store=Store.walmart, program_name="W+", enrolled=True, store_cashback_rate=0.01, fuel_points_per_dollar=0),
        ]
        result = find_program(programs, Store.walmart)
        assert result is not None
        assert result.store == Store.walmart

    def test_returns_none_when_not_found(self):
        result = find_program([], Store.kroger)
        assert result is None
