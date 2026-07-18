from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class ResearchResult:
    topic: str
    summary: str
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
