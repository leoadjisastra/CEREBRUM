from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ResearchResult:
    topic: str
    summary: str
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
