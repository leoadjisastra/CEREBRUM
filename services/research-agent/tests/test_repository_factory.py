import pytest

from research_agent.config import Settings
from research_agent.exceptions import RepositoryError
from research_agent.repository.factory import get_repository
from research_agent.repository.sqlite import SQLiteRepository


def test_get_repository_returns_sqlite():
    settings = Settings(
        llm_provider="anthropic",
        api_key="fake-key",
        model="claude-sonnet-4-6",
        db_provider="sqlite",
        db_path="unused.db",
    )
    repository = get_repository(settings)
    assert isinstance(repository, SQLiteRepository)


def test_get_repository_unknown_raises():
    settings = Settings(
        llm_provider="anthropic",
        api_key="fake-key",
        model="claude-sonnet-4-6",
        db_provider="unknown-db",
        db_path="unused.db",
    )
    with pytest.raises(RepositoryError):
        get_repository(settings)
