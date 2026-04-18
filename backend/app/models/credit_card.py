from enum import Enum
from pydantic import BaseModel


class RewardType(str, Enum):
    cashback = "cashback"
    points = "points"


class CreditCardInput(BaseModel):
    id: str
    name: str
    reward_type: RewardType = RewardType.cashback
    earn_rates: dict[str, float] = {}
    cents_per_point: float = 1.0
    is_active: bool = True
