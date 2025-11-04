from datetime import datetime

from pydantic import BaseModel


class PriceResponse(BaseModel):
    price: float
    timestamp: datetime
