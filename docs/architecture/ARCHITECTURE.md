Mantap, revisi lo semua make sense dan bikin ini jauh lebih matang. Gue gabungin semua ke `ARCHITECTURE.md` versi final — tinggal copy-paste:

```markdown
# CEREBRUM — Architecture

## 1. Overview
CEREBRUM adalah modular multi-agent AI engineering platform untuk riset,
automasi, dan trading crypto (CeFi + DeFi).

**Current reference deployment:**
- HP ProOne 400 G1 AIO
- Ubuntu 24.04 LTS
- 12 GB RAM
- 256 GB SSD + 1 TB HDD

**Target deployment (future):**
- Single server / Mini PC
- VPS
- Cloud
- Kubernetes (future)

Arsitektur ini didesain untuk bertahan lebih lama dari hardware yang menjalankannya.
Setiap keputusan dibuat agar bisa di-scale up tanpa menulis ulang platform.

## 2. Engineering Philosophy
CEREBRUM follows several engineering rules:

1. Every component must be replaceable.
2. Local-first whenever possible.
3. API-first when reasoning quality matters.
4. Scale only after bottlenecks are measured.
5. Every architectural decision must have an ADR.
6. Infrastructure follows project maturity, not hype.
7. Simplicity beats premature optimization.

## 3. System Diagram
```
                    CEREBRUM
            AI Engineering Platform
        +---------------------------+
        |       Human Operator      |
        +-------------+-------------+
                      |
                Claude / Gemini
                      |
        +-------------v-------------+
        |      MCP Server Layer     |
        +-------------+-------------+
                      |
      +---------------+---------------+
      |               |               |
 TradingView      Coinbase      Local Tools
      |               |               |
      +---------------+---------------+
                      |
             Agent Bus Interface
      (SQLite / Redis / RabbitMQ / NATS Adapter)
                      |
+------------------------------------------------+
| AI Analyst        | AI Risk Manager             |
| AI Trader         | Portfolio Manager           |
| Research Agent    | Memory Agent                |
| Notification Agent|                              |
+------------------------------------------------+
                      |
            Shared Memory / Knowledge
                      |
+------------------------------------------------+
| SQLite (default) → Postgres (kalau perlu scale) |
| Chroma (ringan) → Qdrant (kalau perlu scale)    |
| Redis (opsional, on-demand)                     |
+------------------------------------------------+
                      |
          Dashboard / Telegram / Discord
```

## 4. Layer Breakdown

### 01 — Infrastructure
Fondasi non-AI: Ubuntu, Docker, Git, SSH, VSCode, storage, networking, secrets.

### 02 — Deployment
```text
Deployment
├── Local
├── Homelab      ← posisi sekarang
├── VPS
├── Cloud
└── Kubernetes (future)
```
Deployment dipisah dari Docker karena ini keputusan *tempat jalan*, bukan *apa yang jalan*.

### 03 — Docker (service layer)
> **Prinsip: jangan nyalain semua sekaligus.** Pakai Docker Compose profiles.

| Service | Default status | Kapan dinyalain |
|---|---|---|
| SQLite | selalu (bukan container) | dari awal |
| Chroma | ringan, jalan dari awal | Milestone 2 (Memory Agent) |
| Ollama + 1 model kecil | on-demand | Milestone 2 |
| Redis | off by default | hanya kalau butuh queue/cache real-time |
| Postgres | off by default | kalau SQLite mulai jadi bottleneck |
| Qdrant | off by default | kalau Chroma gak cukup buat scale |
| n8n | on-demand | Milestone 2 (workflow automation) |
| OpenWebUI | opsional | nice-to-have |
| Supabase | **skip dulu** | evaluasi lagi kalau butuh Auth/Storage |

### 04 — AI Layer
Dipisah reasoning vs execution — sering beda tujuan, beda biaya, beda latency.
```text
Reasoning Layer   → Claude, Gemini, OpenAI (task berat, kualitas penting)
Execution Layer   → Ollama: Phi-3, Qwen2.5 Q4 (task ringan, lokal, privasi)
Prompt Layer      → system prompt (GEMINI.md), prompt library, few-shot templates
Memory Layer      → lihat section Memory di bawah
```

### 05 — Memory
```text
Short-term Memory   → Conversation, context window aktif
Working Memory       → Current tasks, state yang lagi dikerjain agent
Long-term Memory     → Embeddings, knowledge base (Chroma/Qdrant)
```
Working Memory sering dilewatkan orang, padahal krusial buat agent yang
ngerjain task multi-step tanpa kehilangan konteks task saat ini.

### 06 — Agents
```
Research Agent → cari berita/whitepaper/GitHub → ringkas
AI Analyst     → analisa market, sentiment, on-chain
Risk Manager   → max loss, exposure, position sizing
Trader         → generate signal
Execution      → Coinbase / Hyperliquid / Binance
```
Semua agent independen, komunikasi lewat **Agent Bus Interface** — agent tidak
peduli backend bus-nya apa (SQLite di awal, upgrade ke Redis/RabbitMQ/NATS nanti
tanpa ubah kode agent).

### 07 — Blockchain
Wallet, Coinbase SDK, RPC, smart contract, DEX (Hyperliquid, Uniswap), data
(GMGN, Moralis). Paling belakang sesuai roadmap — masuk pas fase Agentic
Wallet/Mainnet.

### 08 — Quant
```
Market Data → Indicators → Feature Engineering → ML Model → Backtest → Paper Trading → Live
```

### 09 — Workflows
Automasi jadwal (n8n): research pagi → analisa → watchlist → Telegram.
Automasi trigger: harga turun 5% → AI baca → Risk Manager → Trader → Execute → Laporan.

### 10 — Dashboard
Telegram Bot (prioritas pertama, paling ringan) → CLI → Grafana/NextJS (belakangan).

### 11 — Monitoring
```text
Logging   → catat apa yang terjadi
Metrics   → catat seberapa sering/cepat
Tracing   → catat alur request antar agent
```
Implementasi belakangan, tapi dipikirkan strukturnya dari awal.

### 12 — Knowledge (Second Brain)
Books, PDF, whitepaper, notes, meeting, prompt docs — masuk ke embeddings/Chroma.

### 13 — Projects
Wadah eksekusi nyata: Agentic Wallet, Trading Bot, Sales Automation, Coffee Shop
Automation, dll.

## 5. Milestone Roadmap

**Milestone 1 — Foundation**
```
Deployment (Homelab) → Docker Compose (profiles) → SQLite → Chroma
```

**Milestone 2 — First Agent**
```
Ollama (1 model kecil) → Research Agent → Memory (3-tier) → Telegram Bot
```

**Milestone 3 — Market Connection**
```
TradingView-MCP → Coinbase SDK (read-only) → Paper Trading
```

**Milestone 4 — Risk & Execution**
```
Risk Manager → Execution (testnet) → Portfolio Manager → Agent Bus (Redis kalau perlu)
```

**Milestone 5 — Scale & Production**
```
Multi-Agent orchestration → Postgres/Qdrant (kalau bottleneck terukur)
→ Logging/Metrics/Tracing → Mainnet → Kubernetes (future, kalau perlu)
```

## 6. ADR Index
```
docs/ADR/
├── ADR-001-sqlite-before-postgres.md
├── ADR-002-chroma-before-qdrant.md
├── ADR-003-docker-compose-profiles.md
├── ADR-004-no-kubernetes-yet.md
├── ADR-005-local-first-models.md
├── ADR-006-api-model-selection.md
├── ADR-007-agent-communication-bus.md
├── ADR-008-memory-architecture.md
├── ADR-009-trading-risk-boundaries.md
└── ADR-010-mcp-strategy.md
```
Setiap keputusan besar wajib punya ADR — jejak evolusi desain, bukan andalkan ingatan.

## 7. Open Questions / TODO
- [ ] Pilih adapter awal Agent Bus Interface (SQLite dulu — konfirmasi di ADR-007)
- [ ] Docker Compose profile mapping per milestone
- [ ] Keputusan final: Supabase skip permanen atau dievaluasi ulang?
- [ ] MCP servers mana yang diaktifkan duluan (TradingView, Coinbase)?