class ResearchAgentError(Exception):
    """Base exception untuk Research Agent."""
    pass


class ProviderError(ResearchAgentError):
    """Error terkait LLM provider (auth, config, API call)."""
    pass


class RepositoryError(ResearchAgentError):
    """Error terkait penyimpanan hasil riset."""
    pass
