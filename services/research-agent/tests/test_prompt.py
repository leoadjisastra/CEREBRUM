from research_agent.prompt_loader import load_prompt


def test_load_research_prompt():
    prompt = load_prompt("research")
    assert "Research Agent" in prompt
    assert len(prompt) > 0
