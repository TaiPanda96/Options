from pydantic import BaseModel, validator
from datetime import datetime


class Option(BaseModel):
    """
    Option is a pydantic BaseModel that defines the type for an option.
    You can use this base class to define a call option or a put option.
    """

    contractSymbol: str
    symbol: str
    type: str
    lastTradeDate: datetime
    expiration: datetime
    strike: float
    percentChange: float
    openInterest: float
    change: float
    inTheMoney: bool
    impliedVolatility: float
    volume: float
    ask: float
    contractSize: str
    currency: str
    bid: float
    lastPrice: float
    regular_market_price: float
    at: datetime

    @validator("symbol")
    def validate_symbol(self, value):
        """
        validate_symbol validates that the symbol is non-empty
        """
        if len(value) == 0:
            raise ValueError("Symbol must be non-empty")
        return value

    @validator("strike")
    def validate_strike(self, value):
        """
        validate_strike validates that the strike is non-negative
        """
        if value < 0:
            raise ValueError("Strike must be non-negative")
        return value
