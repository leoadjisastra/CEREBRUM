# ADR-006: Repository Structure — Services vs Projects Separation

## Status
Accepted

## Date
2026-07-10

## Context
Setelah workspace utama ditetapkan (ADR-001), diperlukan aturan yang lebih
spesifik mengenai organisasi source code di dalam repository.

Tanpa aturan ini terdapat risiko:
- Logic agent terduplikasi di banyak project.
- Config dan prompt tersebar.
- Sulit membedakan reusable component dengan aplikasi akhir.
- Storage dan test bercampur dengan source code.

## Decision
Repository dipisahkan menjadi area yang memiliki tanggung jawab jelas.

### services/
Building block reusable. Contoh: research-agent, analyst-agent, risk-manager,
trader, execution, portfolio, notification. Service bukan aplikasi akhir,
tetapi komponen yang digunakan oleh project lain.

### projects/
Produk atau aplikasi nyata yang menggunakan service. Contoh: agentic-wallet,
ai-agents, blockchain, mcp, quant-engine, sandbox.

### shared/
Komponen lintas service. Contoh: config, prompts, memory, utils, schemas,
types. Semua service membaca resource bersama dari sini.

### storage/
Penyimpanan data yang berkembang seiring waktu. Contoh: datasets, embeddings,
models, logs, backups, artifacts. Dipisahkan dari source code agar mudah
dipindahkan ke storage eksternal.

### tests/
Seluruh test repository: unit, integration, e2e.

### docs/api
Dokumentasi integrasi eksternal.

### docs/runbooks
Panduan operasional: deploy, backup, restore, incident.

### docs/diagrams
Diagram visual: draw.io, mermaid, PNG, SVG.

## Alternatives Considered

### Semua logic berada di dalam projects/
Pros: awal lebih sederhana.
Cons: logic mudah terduplikasi, sulit dipelihara.
Rejected.

### Shared library tanpa services/
Pros: struktur lebih kecil.
Cons: sulit membedakan reusable business logic dengan utility.
Rejected.

### Services + Shared + Projects
Pros: separation of concerns, reusability tinggi, mudah berkembang menjadi
multi-service.
Accepted.

## Scope
ADR ini mengatur organisasi source code dan resource di dalam repository.

Tidak mengatur:
- Database.
- Docker Compose.
- Agent protocol.
- Memory architecture.
- Deployment.

## Migration Strategy
Folder baru hanya boleh ditambahkan apabila:
- Memiliki tanggung jawab yang jelas.
- Tidak menduplikasi folder yang sudah ada.
- Dibutuhkan oleh implementasi nyata.

## What We Explicitly Do Not Add Yet
Belum menggunakan: Kubernetes, Terraform, Helm, Ansible, Kafka, RabbitMQ,
Airflow, Prometheus, Elasticsearch. Komponen tersebut baru dipertimbangkan
setelah terdapat bottleneck yang terukur.

## When to Revisit
ADR ini dievaluasi apabila:
- Jumlah service meningkat drastis.
- Repository berubah menjadi multi-repository.
- Struktur saat ini mulai menghambat pengembangan.

## Consequences
Positif:
- Reusable component lebih jelas.
- Project lebih modular.
- Refactor lebih kecil.
- AI coding agent lebih mudah memahami struktur repository.

Negatif:
- Repository terlihat lebih besar pada tahap awal.
- Beberapa folder kosong hingga milestone berikutnya.

Trade-off ini diterima.

## Risks
- Struktur dapat menjadi terlalu kompleks apabila service dibuat tanpa kebutuhan.
- Folder kosong dapat membingungkan apabila tidak segera diisi implementasi.

## Non Goals
ADR ini tidak menentukan:
- Database.
- Docker strategy.
- Agent architecture.
- Deployment.
- AI model.

## Related ADRs
- ADR-001 Workspace Layout
- ADR-002 Docker First
- ADR-004 Agent Boundary
- ARCHITECTURE.md
