from dataclasses import dataclass
from datetime import datetime

@dataclass
class ShoppingDTO:
    food_id: int
    total: int
    single_price: float
    food_name: str
    img: str
    added_time: datetime