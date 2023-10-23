import datetime
from pydantic import BaseModel, validator


class Price(BaseModel):
    """
    Price is a pydantic BaseModel that defines the type for a price.
    """

    date: datetime
    price: float
    price_change: float
    bid: float
    ask: float
    currency: str
    symbol: str

    @validator("symbol")
    def validate_symbol(self, value):
        """
        validate_symbol validates that the symbol is non-empty
        """
        if len(value) == 0:
            raise ValueError("Symbol must be non-empty")
        return value

    @validator("date")
    def validate_date(self, value):
        """
        validate_date validates that the date is non-empty
        """
        if len(value) == 0:
            raise ValueError("Date must be non-empty")
        return value
