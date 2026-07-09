# ADR-006: Repository Structure — services/ vs projects/ Separation

## Status
Accepted

## Context
Seiring CEREBRUM berkembang, folder awal (`docs/`, `docker/`) sudah cukup,
tapi belum ada tempat jelas buat:
- Building block yang dipakai berkali-kali oleh banyak project (agents,
  config, prompts, memory logic)
- Aplikasi/produk nyata yang MENGGUNAKAN building block tersebut
- Storage buat data, model, log, backup yang bakal membesar seiring waktu
- Test suite yang terpisah dari kode fungsional

Tanpa struktur ini, ada risiko agent logic ke-duplikat di tiap project, atau
config/prompt tersebar gak konsisten.

## Decision
Repository dipecah jadi layer yang jelas peruntukannya:

- **`services/`** — building block reusable (microservice-style): research-agent,
  analyst-agent, risk-manager, trader, execution, portfolio, notification.
  Ini yang di-*consume*, bukan yang berdiri sendiri sebagai produk.

- **`projects/`** — aplikasi/produk nyata yang MENGGUNAKAN service-service di atas:
  agentic-wallet, ai-agents, blockchain, mcp, quant-engine, sandbox.

- **`shared/`** — resource lintas-service: config, prompts, memory, utils,
  schemas, types. Semua service baca dari sini, bukan hardcode masing-masing.

- **`storage/`** — data yang bakal membesar: datasets, embeddings, models,
  logs, backups, artifacts. Dipisah dari kode biar gampang di-`.gitignore`
  atau dipindah ke storage eksternal nanti.

- **`tests/`** — unit, integration, e2e. Dibuat dari awal walau kosong, biar
  jadi kebiasaan nulis test seiring service bertambah.

- **`docs/runbooks/`** — panduan operasional darurat (deploy, backup, restore,
  incident) yang harus bisa diakses cepat tanpa mikir ulang saat ada masalah.

- **`docs/api/`** — dokumentasi integrasi eksternal (Coinbase, TradingView,
  Telegram, Discord) — penting karena MCP server akan terus bertambah.

- **`docs/diagrams/`** — semua diagram visual (PNG, drawio, mermaid), terpisah
  dari teks ARCHITECTURE.md.

## What we explicitly did NOT add yet
Kubernetes, Terraform, Ansible, Helm, Kafka, RabbitMQ, Airflow, Prometheus,
Elasticsearch — semua ini infra "enterprise" yang belum ada kebutuhan nyata.
Ditambahkan hanya kalau bottleneck terukur (lihat Engineering Philosophy #4
dan #6 di ARCHITECTURE.md).

## Consequences
- Repo terlihat lebih besar dari fungsionalitas saat ini — trade-off yang
  disengaja demi menghindari refactor besar-besaran nanti.
- Developer (termasuk AI agent yang bantu coding) harus tau aturan: agent
  logic reusable → `services/`, produk jadi → `projects/`.
- Folder kosong tetap di-commit pakai `.gitkeep` biar struktur konsisten
  meski isinya belum ada.
