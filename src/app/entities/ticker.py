from pydantic import BaseModel, validator


class Ticker(BaseModel):
    """
    TickerType is a pydantic BaseModel that defines the type for a ticker.
    """

    symbol: str
    name: str
    price: float
    changes_percentage: float
    change: float
    day_low: float
    day_high: float
    year_high: float
    year_low: float

    @validator("symbol")
    def validate_symbol(self, value):
        """
        validate_symbol validates that the symbol is non-empty
        """
        if len(value) == 0:
            raise ValueError("Symbol must be non-empty")
        return value

    @validator("price")
    def validate_price(self, value):
        """
        validate_price validates that the price is non-negative
        """
        if value < 0:
            raise ValueError("Price must be non-negative")
        return value

    @validator("change")
    def validate_change(self, value):
        """
        validate_change validates that the change is non-negative
        """
        if value < 0:
            raise ValueError("Change must be non-negative")
        return value
