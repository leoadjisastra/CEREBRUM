import tempfile
from pathlib import Path

from research_agent.models import ResearchResult
from research_agent.repository.sqlite import SQLiteRepository


def test_save_and_get_history():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        repo = SQLiteRepository(db_path)

        result = ResearchResult(topic="AI agents", summary="Ringkasan singkat.")
        repo.save(result)

        history = repo.get_history()
        assert len(history) == 1
        assert history[0].topic == "AI agents"
        assert history[0].summary == "Ringkasan singkat."
