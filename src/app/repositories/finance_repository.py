from abc import ABC, abstractmethod
from typing import Dict, Literal


class FinanceRepository(ABC):
    """
    FinanceRepository is an abstract class that defines the interface for a finance repository.
     - get_by_ticker: returns a finance by ticker
     - get_by_where: returns a list of finances by where clause
    """

    @abstractmethod
    async def get_by_ticker(
        self, ticker: str, data_type: Literal["price", "option"]
    ) -> Dict:
        """
        get_by_id returns a database by id
        """
