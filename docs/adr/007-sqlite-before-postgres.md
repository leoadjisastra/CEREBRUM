# ADR-007: SQLite Before Postgres

## Status
Accepted

## Date
2026-07-09

## Context
CEREBRUM butuh database buat nyimpen state agent, log trading, dan data
operasional lainnya. The current reference deployment provides limited
compute resources. The architecture intentionally optimizes for constrained
environments first, while preserving a migration path toward larger
deployments.

Postgres itu solid buat production, tapi punya overhead: proses server
terpisah, connection pooling, minimal footprint idle RAM, plus butuh
container sendiri di Docker Compose.

## Decision Drivers
Priority order:
1. Simplicity
2. Low memory usage
3. Fast development
4. Easy maintenance
5. Scalability later

## Alternatives Considered

### PostgreSQL
Pros:
- Mature
- Excellent concurrency
- Rich ecosystem

Cons:
- Extra container
- Higher idle RAM usage
- Operational complexity not justified yet

Decision: Rejected for the current stage.

### DuckDB
Pros:
- Excellent analytical performance
- Great for local analytics

Cons:
- Not designed as an operational database
- Weak fit for agent state management

Decision: Rejected.

## Decision
Pakai **SQLite** sebagai database default di awal, bukan Postgres.

Alasan:
1. **Zero overhead** — SQLite adalah file, bukan server. Gak ada proses
   tambahan yang makan RAM 24/7.
2. **Cukup buat skala saat ini** — CEREBRUM masih single-user, single-machine.
   Concurrent write yang jadi kelemahan SQLite belum relevan di skala ini.
3. **Setup instan** — gak perlu container, gak perlu migration tooling berat,
   gak perlu network config antar service.
4. **Sejalan dengan Engineering Philosophy #4 & #6** — scale only after
   bottlenecks are measured, infrastructure follows project maturity.

## Scope
This decision applies to:
- Agent state
- Metadata
- Task queue metadata
- Audit logs
- Trading logs

This decision does NOT apply to:
- Embeddings
- Large datasets
- Model files
- Market history archives

## Migration Strategy
Migration to PostgreSQL should require minimal application changes.
To achieve this:
- Access database through a repository/data-access layer.
- Avoid SQLite-specific SQL features.
- Keep schema portable.
- Version schema migrations.

## When to Revisit
Pindah ke Postgres kalau salah satu ini kejadian (bukan asumsi, tapi terukur):
- Butuh concurrent write dari banyak agent/service secara bersamaan
- Butuh fitur relasional lanjutan (row-level locking, replication)
- Ukuran database mulai bikin query lambat meskipun udah di-index
- Deployment pindah ke multi-instance/multi-server

## Consequences
- Migrasi ke Postgres nanti butuh effort (schema porting, query adjustment)
  — tapi ini trade-off yang diterima demi kesederhanaan sekarang.
- Semua service harus akses data lewat layer abstraksi (bukan raw SQLite
  query tersebar), biar gampang di-swap ke Postgres nanti tanpa nulis ulang
  logic tiap service.

## Risks
- Concurrent writes may become a bottleneck.
- SQLite file corruption is possible after unexpected power loss.
- Less suitable for distributed deployments.

## Non Goals
This ADR does not attempt to optimize:
- HA (High Availability)
- Replication
- Horizontal scaling
- Multi-region deployment

## Related ADRs
- ADR-002 Docker First
- ADR-004 Agent Boundary
- ADR-006 Repository Structure
