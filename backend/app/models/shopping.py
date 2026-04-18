from pydantic import BaseModel, Field
from .credit_card import CreditCardInput
from .store_rewards import StoreRewardsProgram
from .product import Store


class ShoppingItem(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    quantity: int = Field(ge=1, le=99, default=1)
    unit: str | None = None


class ComparisonRequest(BaseModel):
    items: list[ShoppingItem] = Field(min_length=1, max_length=50)
    zip_code: str = Field(pattern=r"^\d{5}$")
    credit_cards: list[CreditCardInput] = []
    store_rewards_programs: list[StoreRewardsProgram] = []
    demo_mode: bool = False


class LocationResult(BaseModel):
    store: Store
    store_id: str
    name: str
    address: str
    distance_miles: float | None = None
