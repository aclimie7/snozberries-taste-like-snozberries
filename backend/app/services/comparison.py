import asyncio
import logging

from ..config import settings
from ..models.product import (
    ComparisonResult,
    ComparisonSummary,
    ItemComparison,
    NormalizedProduct,
    Recommendation,
    SplitRecommendation,
    Store,
)
from ..models.shopping import ComparisonRequest, ShoppingItem
from ..models.credit_card import CreditCardInput
from ..models.store_rewards import StoreRewardsProgram
from .rewards import find_program
from .kroger import mock as kroger_mock, normalizer as kroger_norm
from .kroger.client import KrogerClient
from .walmart import mock as walmart_mock, normalizer as walmart_norm
from .walmart.client import WalmartClient

_kroger_client: KrogerClient | None = None
_walmart_client: WalmartClient | None = None


def _get_kroger_client() -> KrogerClient:
    global _kroger_client
    if _kroger_client is None:
        _kroger_client = KrogerClient(settings.kroger_client_id, settings.kroger_client_secret)
    return _kroger_client


def _get_walmart_client() -> WalmartClient:
    global _walmart_client
    if _walmart_client is None:
        _walmart_client = WalmartClient(settings.walmart_api_key)
    return _walmart_client

logger = logging.getLogger(__name__)


def _recommend(
    kroger_products: list[NormalizedProduct],
    walmart_products: list[NormalizedProduct],
    quantity: int,
) -> Recommendation | None:
    k_best = kroger_products[0] if kroger_products else None
    w_best = walmart_products[0] if walmart_products else None

    if k_best is None and w_best is None:
        return None
    if k_best is None:
        return Recommendation(store=Store.walmart, product=w_best, reason="Only Walmart has this item")
    if w_best is None:
        return Recommendation(store=Store.kroger, product=k_best, reason="Only Kroger has this item")

    k_cost = k_best.price.final_price * quantity
    w_cost = w_best.price.final_price * quantity
    savings = abs(k_cost - w_cost)
    savings_str = f"saves ${savings:.2f}"

    if k_cost < w_cost:
        parts = [f"Kroger is cheaper after all rewards ({savings_str})"]
        if k_best.on_sale:
            parts.append("on sale")
        if k_best.price.cc_reward_detail:
            parts.append(k_best.price.cc_reward_detail)
        return Recommendation(store=Store.kroger, product=k_best, reason=" · ".join(parts))
    else:
        parts = [f"Walmart is cheaper after all rewards ({savings_str})"]
        if w_best.on_sale:
            parts.append("on sale")
        if w_best.price.cc_reward_detail:
            parts.append(w_best.price.cc_reward_detail)
        return Recommendation(store=Store.walmart, product=w_best, reason=" · ".join(parts))


def _build_split_recommendation(
    comparisons: list[ItemComparison],
    threshold: float,
) -> SplitRecommendation | None:
    kroger_items: list[str] = []
    walmart_items: list[str] = []
    split_total = 0.0
    single_best_total = 0.0

    for item in comparisons:
        k_best = item.kroger[0] if item.kroger else None
        w_best = item.walmart[0] if item.walmart else None
        qty = item.quantity

        if k_best is None and w_best is None:
            continue

        k_cost = k_best.price.final_price * qty if k_best else float("inf")
        w_cost = w_best.price.final_price * qty if w_best else float("inf")
        best_single = min(k_cost, w_cost)
        single_best_total += best_single

        if k_cost <= w_cost:
            kroger_items.append(item.query)
            split_total += k_cost
        else:
            walmart_items.append(item.query)
            split_total += w_cost

    if not (kroger_items and walmart_items):
        return None

    split_savings = round(single_best_total - split_total, 2)
    if split_savings < threshold:
        return None

    return SplitRecommendation(
        kroger_items=kroger_items,
        walmart_items=walmart_items,
        split_savings=split_savings,
    )


async def _compare_one_item(
    item: ShoppingItem,
    kroger_location_id: str,
    zip_code: str,
    cards: list[CreditCardInput],
    kroger_program: StoreRewardsProgram | None,
    walmart_program: StoreRewardsProgram | None,
    use_kroger_mock: bool,
    use_walmart_mock: bool,
    warnings: list[str],
) -> ItemComparison:
    kroger_task = (
        kroger_mock.search_products(item.name, kroger_location_id)
        if use_kroger_mock
        else _kroger_live_search(item.name, kroger_location_id)
    )
    walmart_task = (
        walmart_mock.search_products(item.name, zip_code)
        if use_walmart_mock
        else _walmart_live_search(item.name, zip_code)
    )

    k_raw, w_raw = await asyncio.gather(kroger_task, walmart_task, return_exceptions=True)

    kroger_products: list[NormalizedProduct] = []
    walmart_products: list[NormalizedProduct] = []

    if isinstance(k_raw, Exception):
        logger.warning("Kroger fetch failed for '%s': %s", item.name, k_raw)
        if "Kroger data unavailable for some items" not in warnings:
            warnings.append("Kroger data unavailable for some items")
    else:
        for r in list(k_raw)[:3]:
            try:
                kroger_products.append(
                    kroger_norm.normalize(r, item.quantity, cards, kroger_program)
                )
            except Exception as e:
                logger.warning("Kroger normalize error: %s", e)

    if isinstance(w_raw, Exception):
        logger.warning("Walmart fetch failed for '%s': %s", item.name, w_raw)
        if "Walmart data unavailable for some items" not in warnings:
            warnings.append("Walmart data unavailable for some items")
    else:
        for r in list(w_raw)[:3]:
            try:
                walmart_products.append(
                    walmart_norm.normalize(r, item.quantity, cards, walmart_program)
                )
            except Exception as e:
                logger.warning("Walmart normalize error: %s", e)

    recommendation = _recommend(kroger_products, walmart_products, item.quantity)

    return ItemComparison(
        query=item.name,
        quantity=item.quantity,
        kroger=kroger_products,
        walmart=walmart_products,
        recommended=recommendation,
    )


async def _kroger_live_search(query: str, location_id: str) -> list[dict]:
    return await _get_kroger_client().search_products(query, location_id)


async def _walmart_live_search(query: str, zip_code: str) -> list[dict]:
    return await _get_walmart_client().search_products(query, zip_code)


async def run_comparison(request: ComparisonRequest) -> ComparisonResult:
    use_kroger_mock = settings.use_kroger_mock or request.demo_mode
    use_walmart_mock = settings.use_walmart_mock or request.demo_mode
    demo_active = use_kroger_mock or use_walmart_mock

    kroger_location_id = "70300168"
    kroger_program = find_program(request.store_rewards_programs, Store.kroger)
    walmart_program = find_program(request.store_rewards_programs, Store.walmart)

    warnings: list[str] = []
    tasks = [
        _compare_one_item(
            item=item,
            kroger_location_id=kroger_location_id,
            zip_code=request.zip_code,
            cards=request.credit_cards,
            kroger_program=kroger_program,
            walmart_program=walmart_program,
            use_kroger_mock=use_kroger_mock,
            use_walmart_mock=use_walmart_mock,
            warnings=warnings,
        )
        for item in request.items
    ]
    comparisons = list(await asyncio.gather(*tasks))

    kroger_total = 0.0
    walmart_total = 0.0
    rewards_applied = 0.0

    for comp in comparisons:
        if comp.kroger:
            kroger_total += comp.kroger[0].price.effective_price * comp.quantity
            rewards_applied += comp.kroger[0].price.cc_reward_value
        if comp.walmart:
            walmart_total += comp.walmart[0].price.effective_price * comp.quantity
            rewards_applied += comp.walmart[0].price.cc_reward_value

    kroger_total = round(kroger_total, 2)
    walmart_total = round(walmart_total, 2)
    rewards_applied = round(rewards_applied, 2)

    best_store = Store.kroger if kroger_total <= walmart_total else Store.walmart
    best_total = min(kroger_total, walmart_total)
    worst_total = max(kroger_total, walmart_total)
    total_savings = round(worst_total - best_total, 2)

    split = _build_split_recommendation(comparisons, settings.split_savings_threshold)

    summary = ComparisonSummary(
        kroger_total=kroger_total,
        walmart_total=walmart_total,
        best_store=best_store,
        total_savings=total_savings,
        rewards_applied=rewards_applied,
        split_recommendation=split,
    )

    return ComparisonResult(
        items=comparisons,
        summary=summary,
        demo_mode=demo_active,
        warnings=warnings,
    )
