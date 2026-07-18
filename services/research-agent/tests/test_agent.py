from unittest.mock import Mock

from research_agent.agent import ResearchAgent
from research_agent.models import ResearchResult


def test_agent_run_generates_and_saves_result():
    provider = Mock()
    provider.generate.return_value = "Ringkasan hasil riset"
    repository = Mock()

    agent = ResearchAgent(provider=provider, repository=repository)
    result = agent.run("AI trading")

    assert isinstance(result, ResearchResult)
    assert result.topic == "AI trading"
    assert result.summary == "Ringkasan hasil riset"
    provider.generate.assert_called_once()
    repository.save.assert_called_once_with(result)


def test_agent_run_passes_correct_prompts_to_provider():
    provider = Mock()
    provider.generate.return_value = "summary apapun"
    repository = Mock()

    agent = ResearchAgent(provider=provider, repository=repository)
    agent.run("Bitcoin halving")

    system_prompt, user_prompt = provider.generate.call_args[0]
    assert "Bitcoin halving" in user_prompt
    assert system_prompt == agent.system_prompt
