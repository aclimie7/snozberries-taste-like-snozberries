from enum import Enum
from pydantic import BaseModel, Field


class Store(str, Enum):
    kroger = "kroger"
    walmart = "walmart"


class ProductCategory(str, Enum):
    grocery = "grocery"
    general_merchandise = "general_merchandise"


class PriceBreakdown(BaseModel):
    base_price: float
    sale_price: float | None = None
    coupon_savings: float = 0.0
    store_rewards_savings: float = 0.0
    effective_price: float
    cc_reward_value: float = 0.0
    final_price: float
    cc_reward_detail: str = ""
    store_reward_detail: str = ""


class NormalizedProduct(BaseModel):
    store: Store
    product_id: str
    name: str
    brand: str = ""
    upc: str | None = None
    size: str = ""
    image_url: str | None = None
    category: ProductCategory = ProductCategory.grocery
    price: PriceBreakdown
    on_sale: bool = False
    has_digital_coupon: bool = False
    in_stock: bool = True
    score: float = Field(ge=0.0, le=1.0, default=1.0)


class Recommendation(BaseModel):
    store: Store
    product: NormalizedProduct
    reason: str


class ItemComparison(BaseModel):
    query: str
    quantity: int
    kroger: list[NormalizedProduct] = []
    walmart: list[NormalizedProduct] = []
    recommended: Recommendation | None = None


class SplitRecommendation(BaseModel):
    kroger_items: list[str]
    walmart_items: list[str]
    split_savings: float


class ComparisonSummary(BaseModel):
    kroger_total: float
    walmart_total: float
    best_store: Store
    total_savings: float
    rewards_applied: float
    split_recommendation: SplitRecommendation | None = None


class ComparisonResult(BaseModel):
    items: list[ItemComparison]
    summary: ComparisonSummary
    demo_mode: bool = False
    warnings: list[str] = []
