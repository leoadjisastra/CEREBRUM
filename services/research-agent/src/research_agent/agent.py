from .models import ResearchResult
from .prompt_loader import load_prompt
from .providers.base import LLMProvider
from .repository.base import ResearchRepository


class ResearchAgent:
    def __init__(self, provider: LLMProvider, repository: ResearchRepository):
        self.provider = provider
        self.repository = repository
        self.system_prompt = load_prompt("research")

    def run(self, topic: str) -> ResearchResult:
        user_prompt = f"Riset dan ringkas topik berikut: {topic}"
        summary = self.provider.generate(self.system_prompt, user_prompt)
        result = ResearchResult(topic=topic, summary=summary)
        self.repository.save(result)
        return result
