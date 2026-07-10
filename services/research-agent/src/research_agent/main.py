import argparse
import logging
import sys

from .agent import ResearchAgent
from .config import Settings
from .exceptions import ResearchAgentError
from .providers.factory import get_provider
from .repository.factory import get_repository

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [research_agent] %(message)s",
)
logger = logging.getLogger("research_agent")


def main():
    parser = argparse.ArgumentParser(description="CEREBRUM Research Agent")
    parser.add_argument("topic", type=str, help="Topik yang mau diriset")
    args = parser.parse_args()

    try:
        settings = Settings.load()
        provider = get_provider(settings)
        repository = get_repository(settings)
        agent = ResearchAgent(provider=provider, repository=repository)

        logger.info(f"Researching topic: {args.topic}")
        result = agent.run(args.topic)

        print("\n=== RESEARCH SUMMARY ===")
        print(f"Topic: {result.topic}")
        print(f"Time: {result.created_at}")
        print(f"\n{result.summary}\n")
        logger.info("Result saved.")
    except ResearchAgentError as e:
        logger.error(f"Research Agent failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
