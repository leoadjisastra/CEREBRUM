# ADR-001: Workspace Layout

## Status
Accepted

## Date
2026-07-10

## Context
CEREBRUM dirancang sebagai AI Engineering Platform yang akan berkembang secara
bertahap menjadi platform modular untuk AI Agents, Blockchain, Quant Trading,
Automation, dan Knowledge Management.

Repository diperkirakan akan terus bertambah selama bertahun-tahun. Tanpa
workspace yang memiliki batas tanggung jawab jelas sejak awal, repository akan
mengalami:
- Struktur yang tidak konsisten.
- Dokumentasi sulit ditemukan.
- Kode reusable tersebar di berbagai lokasi.
- Refactor besar ketika project bertambah.
- Developer maupun AI coding agent kesulitan memahami organisasi repository.

Karena itu struktur workspace diputuskan terlebih dahulu sebelum implementasi
fitur dimulai.

## Decision Drivers
Prioritas keputusan ini adalah:
1. Konsistensi repository.
2. Separation of Concerns.
3. Kemudahan navigasi.
4. Skalabilitas jangka panjang.
5. Kemudahan onboarding developer maupun AI agent.
6. Refactor seminimal mungkin.

## Alternatives Considered

### Flat Repository
Semua file berada di root repository.

Pros:
- Sangat sederhana.
- Cepat dibuat.

Cons:
- Sulit dipelihara.
- Cepat berantakan.

Rejected.

### Multiple Repositories
Setiap project memiliki repository sendiri.

Pros:
- Isolasi project sangat jelas.

Cons:
- Sulit berbagi library internal.
- Dokumentasi terpecah.
- Sulit melakukan perubahan lintas project.

Rejected pada tahap awal.

### Modular Monorepo
Pros:
- Dokumentasi terpusat.
- Shared resource mudah digunakan ulang.
- Cocok untuk platform AI engineering.

Cons:
- Struktur awal terlihat lebih besar.

Accepted.

## Decision
CEREBRUM menggunakan pendekatan **modular monorepo**.

Workspace dibagi berdasarkan area tanggung jawab tingkat tinggi, seperti:
- Documentation
- Infrastructure
- Source Code
- Shared Resources
- Storage
- Automation
- Testing

Detail struktur masing-masing area dijelaskan pada ADR tersendiri.

## Scope
ADR ini hanya mengatur filosofi dan organisasi workspace.

ADR ini **tidak** menentukan:
- Struktur folder internal.
- Docker.
- Database.
- Bahasa pemrograman.
- Agent architecture.
- Deployment.

Semua keputusan tersebut dibuat pada ADR terpisah.

## Migration Strategy
Workspace dapat berkembang mengikuti kebutuhan project.

Perubahan besar terhadap struktur workspace harus:
- Memiliki alasan yang jelas.
- Menghindari duplikasi.
- Didokumentasikan melalui ADR baru atau revisi ADR ini.

## When to Revisit
ADR ini dievaluasi apabila:
- Monorepo tidak lagi sesuai.
- Repository menjadi terlalu besar.
- Dibutuhkan pemisahan menjadi beberapa repository.

## Consequences
Positif:
- Repository lebih mudah dipahami.
- Struktur konsisten.
- Dokumentasi lebih mudah ditemukan.
- Refactor besar dapat diminimalkan.

Negatif:
- Jumlah folder terlihat lebih banyak pada tahap awal.
- Sebagian folder masih kosong sampai milestone berikutnya.

Trade-off ini diterima.

## Risks
- Overengineering apabila struktur bertambah tanpa implementasi nyata.
- Struktur menjadi usang apabila tidak dievaluasi secara berkala.

## Non Goals
ADR ini tidak menentukan:
- Database.
- Docker strategy.
- AI model.
- MCP architecture.
- Deployment architecture.

## Related ADRs
- ADR-002 Docker First
- ADR-004 Agent Boundary
- ADR-006 Repository Structure
- ARCHITECTURE.md
