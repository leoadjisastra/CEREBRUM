# CEREBRUM — AI Agent Context

## ⚠️ Security Rules (READ FIRST)

Never hardcode:
- API Keys
- Wallet Private Keys
- Mnemonic phrases
- Secrets of any kind

Always use `.env` files (never commit them — see .gitignore).

Never execute a real blockchain transaction unless explicitly requested by Leo in that exact session.

Default environment for all trading/wallet code: **Testnet** and **Paper Trading**.
Mainnet is off-limits until Leo explicitly says otherwise, per docs/adr/005-testnet-first.md.

Never deploy automatically. Never run `docker compose up -d` on production-like configs without confirmation.

## Project Mission

CEREBRUM is Leo's long-term AI Engineering workspace — a foundation for
multi-agent systems, quant trading research, blockchain/agentic wallet
experiments, and automation, built to last years, not weeks.

## Environment

- OS: Ubuntu 24.04 (HP ProOne 400 G1 AIO, RAM 12GB (8+4), SSD 256GB + HDD 1TB)
- Secondary device: Xiaomi Redmi Note 9 Pro (8/128) — used for remote access, Telegram bot control, monitoring
- Docker (docker-ce, compose plugin)
- Python 3.12
- Node.js (via NVM)
- Ollama (local LLM)
- Claude Code, Gemini CLI

## Hardware Constraints

Development machine: HP ProOne 400 G1, RAM 12GB, limited CPU.

Avoid:
- Kubernetes
- Huge Vector DB
- Giant Local LLM (stick to 1.5B–3B class models)
- Excessive Docker containers running simultaneously

Prefer lightweight solutions. Always consider RAM footprint before suggesting
a new service or container.

## Preferred Stack

Backend:
- Python

Automation:
- Python
- n8n

CLI:
- Python
- Bash

Web:
- FastAPI
- React (later)

AI:
- Ollama
- OpenAI-compatible APIs
- Gemini
- Claude

Database:
- SQLite (prototype)
- PostgreSQL (later)

Container:
- Docker Compose

Do not introduce a new language, framework, or database outside this list
without proposing an ADR first.

## Architecture

See docs/architecture/ARCHITECTURE.md and docs/adr/ for reasoning behind
every major structural decision. Do not restructure folders without
proposing an ADR first.

## Repository Principle

One repository.
Many independent projects.
Loose coupling.
High cohesion.

CEREBRUM is not one application — it is a workspace.

## Folder Responsibilities

- `projects/ai-agents/` — general-purpose agent experiments
- `projects/quant-engine/` — trading pipeline (Analyst → Research → Risk → Trader)
- `projects/agentic-wallet/` — wallet automation (testnet-only until further notice)
- `projects/blockchain/` — on-chain interaction code
- `projects/mcp/` — MCP servers/clients
- `projects/sandbox/` — throwaway experiments, not part of any pipeline
- `docker/compose/` — docker-compose files per service
- `docker/dockerfiles/` — custom images
- `storage/` — gitignored data/model/log storage, folder tracked via .gitkeep

## Coding Philosophy

Build software that can still be understood two years from now.

Prefer:
- readability
- modularity
- explicitness

Avoid:
- premature optimization
- over-engineering
- unnecessary abstractions

## Coding Standards

- Python: type hints where practical, docstrings on public functions
- Commit messages: imperative mood, e.g. "Add risk manager module"
- One concern per commit where reasonable

## Agent Behavior

Before writing code:
1. Read existing files.
2. Understand architecture.
3. Reuse existing modules.
4. Avoid duplicate logic.
5. Explain changes before large edits.

## AI Decision Rules

When uncertain:
- Ask before making architectural changes.
- Prefer modifying existing code over creating new files.
- Avoid duplicate implementations.
- Prefer simple solutions over clever ones.
- Explain tradeoffs before major refactors.

## Development Workflow

- Build one pipeline node end-to-end before adding the next.
- No "monster stack" changes — small, testable increments.
- Document decisions in docs/notes/DEVLOG.md as you go, not after.

## Git Rules

- Never commit .env, secrets/, wallets/, private_keys/, models/, datasets/
- Never force-push to main

## ADR Rules

Major decisions require an ADR. Examples:
- New language
- New database
- New architecture
- New messaging system
- Production deployment

## Docker Rules

- Prefer named volumes over bind mounts for stateful services
- Set memory limits on containers (host has 12GB RAM total)

## Testing Rules

- Trading logic must be testable against historical/paper data before
  any live execution path is added

## Long-term Goals

Phase 3–9 roadmap: Sandbox → Quant Engine → AI Analyst → Risk Manager →
Paper Trading → Backtesting → Testnet → Agentic Wallet → Mainnet.
Mainnet is the final phase and requires explicit human sign-off per ADR 005.