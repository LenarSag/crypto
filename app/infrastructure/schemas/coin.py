from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CoinCreate(BaseModel):
    ticker: str
    name: str
    description: str


class CoinResponse(CoinCreate):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class CoinPriceResponse(CoinResponse):
    price: float
