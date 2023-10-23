from abc import ABC, abstractmethod
from typing import List, Dict


class DatabaseRepository(ABC):
    """
    DatabaseRepository is an abstract class that defines the interface for a database repository.
    - get_all: returns a list of all databases
    - get_by_id: returns a database by id
    - get_by_name: returns a database by name
    - get_relations: returns a list of all relations for a database by id
    - get_relation: returns a relation by id
    """

    @abstractmethod
    def get_all(self) -> List[Dict]:
        """
        get_all returns a list of all databases
        """

    @abstractmethod
    def get_by_id(self) -> Dict:
        """
        get_by_id returns a database by id
        """

    @abstractmethod
    def get_tables(self, name: str) -> List[Dict]:
        """
        get_tables returns a list of all tables for a database by name
        """

    @abstractmethod
    def get_table(self, name: str, table_name: str) -> Dict:
        """
        get_table returns a table by name for a database by name
        """

    @abstractmethod
    def get_columns(self, name: str, table_name: str) -> List[Dict]:
        """
        get_columns returns a list of all columns for a table by name for a database by name
        """

    @abstractmethod
    def get_many_by_id(self, ids: List[str]) -> List[Dict]:
        """
        get_many_by_id returns a list of databases by id
        """

    @abstractmethod
    def get_by_where(self, where: Dict) -> List[Dict]:
        """
        get_by_where returns a list of databases by where clause
        """
