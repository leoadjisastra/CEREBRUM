# CEREBRUM — Roadmap (Single Source of Truth)

> Dokumen ini adalah **satu-satunya** acuan resmi urutan phase & sprint CEREBRUM.
> Setiap perubahan roadmap WAJIB diubah di sini dulu, baru direfleksikan ke
> ADR, README, atau ringkasan lain (mis. status snapshot yang dipakai untuk
> membuka chat baru). Jangan pernah sebaliknya.

**Last updated:** 2026-07-25

## Progress Phase

| Phase | Nama                      | Status              |
|:-----:|---------------------------|:--------------------:|
| 1     | Repository Foundation     | ✅ 100%              |
| 2     | Engineering Foundation    | ✅ 100%              |
| 3     | Core SDK                  | 🟡 In Progress       |
| 4     | Research Agent v0.1       | ✅ 100%              |
| 5     | Research Agent v0.2       | ⚪ 0%                |
| 6     | Research Agent v0.3       | ⚪ 0%                |
| 7     | Observability              | ⚪ 0%                |
| 8     | Memory Agent               | ⚪ 0%                |
| 9     | Analyst Agent               | ⚪ 0%                |
| 10    | Evaluation Framework        | ⚪ 0%                |
| 11    | AI Trader                    | ⚪ 0%                |
| 12    | Blockchain                    | ⚪ 0%                |
| 13    | Dashboard / UI                 | ⚪ 0%                |

## Phase 3 — Core SDK (`packages/cerebrum-core/`)

Filosofi: **bangun fondasi paling bawah dulu, baru feature.** Semua sprint di
bawah ini murni infrastruktur — belum ada implementasi spesifik (LLM provider,
prompt loader, dll masuk fase berikutnya, lihat catatan di bawah).

| Sprint | Modul       | Status |
|:------:|-------------|:------:|
| 3.1    | Config      | ⚪     |
| 3.2    | Logging     | ⚪     |
| 3.3    | Retry       | ⚪     |
| 3.4    | Timeout     | ⚪     |
| 3.5    | Exceptions  | ⚪     |
| 3.6    | Telemetry   | ⚪     |
| 3.7    | Utilities   | ⚪     |
| 3.8    | Interfaces  | ⚪     |
| 3.9    | Shared Types| ⚪     |

**Catatan penting:** LLM Provider (Anthropic/OpenAI/Gemini/Ollama) dan Prompt
Loader **bukan bagian Phase 3**. Mereka adalah *implementasi* dari Interface
yang didefinisikan di Sprint 3.8, jadi urutannya:

Sprint 3.8 (Interfaces)
↓
AnthropicProvider / OpenAIProvider / ... (dijadwalkan belakangan, phase TBD)


Referensi keputusan: `docs/adr/ADR-014-core-sdk-package-location.md`

## Setelah Phase 3 selesai

Core SDK (packages/cerebrum-core/)
↓
Research Agent v0.2 (migrasi ke cerebrum-core)
↓
Memory Agent → Analyst Agent → Trader Agent → ...

