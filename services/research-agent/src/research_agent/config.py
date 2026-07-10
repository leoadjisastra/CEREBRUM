import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_DEFAULT_DB = Path(__file__).resolve().parents[3] / "storage" / "research_agent.db"


@dataclass(frozen=True)
class Settings:
    llm_provider: str
    api_key: str
    model: str
    db_provider: str
    db_path: Path

    @staticmethod
    def load() -> "Settings":
        return Settings(
            llm_provider=os.getenv("LLM_PROVIDER", "anthropic"),
            api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            model=os.getenv("MODEL_NAME", "claude-sonnet-4-6"),
            db_provider=os.getenv("DB_PROVIDER", "sqlite"),
            db_path=Path(os.getenv("DB_PATH", str(_DEFAULT_DB))),
        )
