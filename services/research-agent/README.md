# Research Agent

Service pertama CEREBRUM. Menerima topik dari CLI, mengirim prompt ke LLM
provider (Anthropic dulu, provider lain lewat interface yang sama), menyimpan
ringkasan lewat repository interface (SQLite dulu), menampilkan hasil di
terminal.

## ArchitectureResearchAgent
|
+-- LLMProvider (interface)
|       +-- AnthropicProvider  <- aktif
|       +-- GeminiProvider     <- belum
|       +-- OllamaProvider     <- belum
|
+-- ResearchRepository (interface)
+-- SQLiteRepository   <- aktif
+-- PostgresRepository <- belum## Usage

```bash
cp .env.example .env
# isi ANTHROPIC_API_KEY di .env

pip install -e .
python -m research_agent.main "topik yang mau diriset"
```

Tidak perlu `export` manual — `Settings.load()` otomatis baca `.env` lewat
python-dotenv.

## Testing

```bash
pip install -e ".[dev]"
pytest tests/
```

## Roadmap

| Version | Fitur | Status |
|---|---|---|
| v0.1 | CLI + single LLM call | ✅ |
| v0.2 | SQLite storage | ✅ |
| v0.3 | History command | ⬜ |
| v0.4 | Tools (web search) | ⬜ |
| v0.5 | Telegram output | ⬜ |
| v0.6 | TradingView-MCP | ⬜ |

## Status
v0.2 — Provider interface (Anthropic aktif), repository interface (SQLite
aktif), prompt as markdown file, custom exceptions.
