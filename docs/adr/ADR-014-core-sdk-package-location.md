# ADR-014: Core SDK Package Location and Structure

**Status:** Accepted
**Date:** 2026-07-25
**Supersedes:** —
**Superseded by:** —

## Context

CEREBRUM memasuki Phase 3 (Core SDK), fondasi yang akan dipakai ulang oleh
seluruh agent (Research, Memory, Analyst, Trader, Risk Manager, dst).
Ada dua kandidat lokasi:

1. `services/shared/` — folder yang sudah ada (berisi `storage/` dari commit lama)
2. `packages/cerebrum-core/` — package terpisah di luar `services/`

Menempatkan shared code di dalam `services/` mengaburkan identitasnya: apakah
`shared` itu sebuah service, atau library? Monorepo yang sehat memisahkan
*executable* (service yang jalan sendiri, punya entrypoint) dari *reusable
library* (dipakai/di-import, tidak punya proses sendiri).

## Decision

Core SDK ditempatkan di `packages/cerebrum-core/`, bukan `services/shared/`.

Struktur direktori:

CEREBRUM/
├── packages/
│ └── cerebrum-core/
│ ├── pyproject.toml
│ ├── README.md
│ ├── src/
│ │ └── cerebrum_core/
│ └── tests/
├── services/
│ ├── research-agent/
│ ├── memory-agent/
│ ├── analyst-agent/
│ └── trader-agent/
├── storage/
└── docs/


Nama package: `cerebrum-core` / import path `cerebrum_core` (bukan `core`,
karena `core` terlalu generik dan rawan bentrok dengan dependency lain).

### Dependency rule (satu arah)

- Service (agent) **boleh** import `cerebrum_core`.
- `cerebrum_core` **tidak boleh** import kode dari service manapun
  (`research_agent`, `memory_agent`, `trader`, dll).

Pelanggaran terhadap rule ini dianggap architecture violation dan harus
diperbaiki sebelum merge.

## Consequences

**Positif:**
- Boundary jelas antara reusable library dan executable service.
- Konsisten dengan struktur monorepo modern (`packages/` vs `services/`).
- Menghindari refactor besar saat jumlah service bertambah (Memory, Analyst,
  Trader, Risk Manager, dst).
- Membuka ruang untuk package tambahan di masa depan tanpa bongkar fondasi
  (`cerebrum-types`, `cerebrum-testing`, `cerebrum-cli`, `cerebrum-devtools`
  — belum dibuat, hanya dicatat sebagai kemungkinan arah).

**Trade-off:**
- Effort setup awal sedikit lebih besar dibanding `services/shared/`: butuh
  `pyproject.toml` sendiri untuk `cerebrum-core`, dan konfigurasi `uv workspace`
  di root supaya service lain bisa `import cerebrum_core` secara local/editable.

## Alternatives Considered

- **`services/shared/`** — ditolak. Effort awal lebih kecil, tapi identitas
  ambigu (service atau library?) dan akan butuh migrasi ulang begitu ada
  package kedua (mis. `cerebrum-types`, `cerebrum-sdk`).
