from abc import ABC, abstractmethod

from ..models import ResearchResult


class ResearchRepository(ABC):
    """Interface penyimpanan hasil riset (SQLite, Postgres, dll)."""

    @abstractmethod
    def save(self, result: ResearchResult) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_history(self, limit: int = 10) -> list[ResearchResult]:
        raise NotImplementedError
