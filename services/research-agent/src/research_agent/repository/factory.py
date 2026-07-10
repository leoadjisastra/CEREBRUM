from ..config import Settings
from ..exceptions import RepositoryError
from .base import ResearchRepository
from .sqlite import SQLiteRepository

REPOSITORIES = {
    "sqlite": SQLiteRepository,
    # "postgres": PostgresRepository,   # belum diimplementasi
}


def get_repository(settings: Settings) -> ResearchRepository:
    repo_cls = REPOSITORIES.get(settings.db_provider)
    if repo_cls is None:
        raise RepositoryError(f"Unknown DB provider: {settings.db_provider}")

    return repo_cls(db_path=settings.db_path)
