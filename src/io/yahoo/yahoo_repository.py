from app.entities.options import Option
from app.entities.ticker import Ticker
from app.repositories.finance_repository import FinanceRepository
from io.yahoo.yahoo_client import YahooHttpInterface
from typing import Union, List, Dict, Literal
from app.utils.pick import pick
from pydantic import BaseModel


class YahooFinanceOptions(BaseModel):
    ticker: str
    expiration_dates: List[str]
    calls: List[Option]
    puts: List[Option]


class YahooFinanceRepository(FinanceRepository):
    """
    YahooFinanceRepository is a class that implements the FinanceRepository interface.
    """

    def __init__(self, client: YahooHttpInterface):
        self.client = client
        super().__init__()

    async def get_by_ticker(
        self, ticker: Ticker, data_type: Literal["options"]
    ) -> Option:
        """
        get_by_ticker returns a price by ticker
        """
        options_data = self.client.get_by_ticker(ticker, data_type)

        if isinstance(options_data, dict):
            return self._process_options_data(options_data)

        return None

    async def get_expiration_dates(self, ticker: Ticker) -> List[str, None]:
        """
        get_expiration_dates returns a price by ticker
        """
        options_data = self.client.get_expiration_dates(ticker)
        options_chain = options_data["optionChain"]["result"]

        if isinstance(options_data, dict):
            expiration_dates = options_chain[0]["expirationDates"]
            return expiration_dates

        return None

    async def _process_options_data(
        self, options_data: dict
    ) -> Union[YahooFinanceOptions, None]:
        """
        Private method _process_options_data processes options data
        """
        options_chain = options_data["optionChain"]
        result = options_chain["result"]

        if (
            len(result) == 0
            or result[0].get("quote", None) is None
            or result[0].get("options", None) is None
        ):
            return None

        quote = pick(
            result[0]["quote"],
            ["regularMarketPrice", "regularMarketTime", "bid", "ask"],
        )

        short_quote = {
            "price": self._getRawValue(quote, "regularMarketPrice"),
            "time": self._getRawValue(quote, "regularMarketTime"),
            "bid": self._getRawValue(quote, "bid"),
            "ask": self._getRawValue(quote, "ask"),
        }

        options_chain = result[0]["options"]

        if (
            len(options_chain) == 0
            or options_chain[0].get("calls", None) is None
            or options_chain[0].get("puts", None) is None
        ):
            return None

        return YahooFinanceOptions(
            ticker=self._getRawValue(quote, "symbol"),
            expiration_dates=options_chain[0]["expirationDates"],
            calls=list(
                map(
                    lambda call: self.create_option(**call, **short_quote),
                    options_chain[0]["calls"],
                )
            ),
            puts=list(
                map(
                    lambda put: self.create_option(**put, **short_quote),
                    options_chain[0]["puts"],
                )
            ),
        )

    def _getRawValue(self, data: Dict, key: str) -> Union[str, None]:
        """
        Accesses a value in a dictionary by key and returns it.
        """
        if key in data:
            return data[key]["raw"]

        return None

    def create_option(self, ticker: str, option_data: Dict) -> Option:
        """
        Instantiates an Option object from a dictionary.
        """
        return Option(
            at=self._getRawValue(option_data, "time"),
            contractSymbol=self._getRawValue(option_data, "contractSymbol"),
            symbol=ticker,
            type=self._getRawValue(option_data, "type"),
            lastTradeDate=self._getRawValue(option_data, "lastTradeDate"),
            expiration=self._getRawValue(option_data, "expiration"),
            strike=self._getRawValue(option_data, "strike"),
            percentChange=self._getRawValue(option_data, "percentChange"),
            openInterest=self._getRawValue(option_data, "openInterest"),
            change=self._getRawValue(option_data, "change"),
            inTheMoney=self._getRawValue(option_data, "inTheMoney"),
            impliedVolatility=self._getRawValue(option_data, "impliedVolatility"),
            volume=self._getRawValue(option_data, "volume"),
            ask=self._getRawValue(option_data, "ask"),
            contractSize=self._getRawValue(option_data, "contractSize"),
            currency=self._getRawValue(option_data, "currency"),
            bid=self._getRawValue(option_data, "bid"),
            lastPrice=self._getRawValue(option_data, "lastPrice"),
            regular_market_price=self._getRawValue(option_data, "price"),
        )
