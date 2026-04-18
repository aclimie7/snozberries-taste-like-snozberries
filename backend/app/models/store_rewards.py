from pydantic import BaseModel
from .product import Store


class StoreRewardsProgram(BaseModel):
    store: Store
    program_name: str
    enrolled: bool = False
    store_cashback_rate: float = 0.0
    fuel_points_per_dollar: float = 0.0
