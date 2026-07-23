# ADR-013: Automated Versioning & Release Strategy

## Status
Accepted — Implemented (Research Agent v0.1.1)

---

## Context
CEREBRUM adalah monorepo yang akan berisi banyak service independen, seperti:
- Research Agent
- Memory Agent
- Analyst Agent
- AI Trader
- Risk Manager
- dan service lain di masa depan.

Sebelum ADR ini, proses release dilakukan secara manual:
- bump version manual
- membuat git tag manual
- changelog manual
- GitHub Release manual

Pendekatan tersebut mudah menimbulkan human error dan tidak akan scalable ketika jumlah service bertambah.

Target implementasi:
- version mengikuti commit history
- release otomatis
- build otomatis
- changelog otomatis
- GitHub Release otomatis
- setiap service mempunyai lifecycle release sendiri tanpa saling mengganggu.

Selama implementasi ditemukan beberapa masalah nyata yang mengubah desain awal, seperti:
- python-semantic-release membaca root repository apabila directory tidak di-scope.
- Default konfigurasi semantic-release langsung menghasilkan v1.0.0.
- Action release berjalan pada container berbeda sehingga `uv` tidak tersedia.
- Project tidak dapat di-build tanpa tabel `[build-system]`.
- Coverage turun karena CLI entrypoint ikut dihitung.

ADR ini mendokumentasikan keputusan final hasil implementasi tersebut.

---

# Decision

## 1. Commit Convention
Semua repository menggunakan Conventional Commits.

| Commit | Version |
|---------|----------|
| feat: | Minor |
| fix: | Patch |
| perf: | Patch |
| BREAKING CHANGE / ! | Major |
| docs | No bump |
| chore | No bump |
| ci | No bump |
| build | No bump |
| refactor | No bump |
| style | No bump |
| test | No bump |

Dokumen lengkap terdapat pada:

COMMIT_CONVENTION.md


---

## 2. Release Tool
Dipilih:

python-semantic-release v10

karena mampu melakukan otomatis:
- Version bump
- Git Tag
- CHANGELOG
- GitHub Release
- Artifact upload

tanpa proses manual.

---

## 3. Workflow dipisah per Service
Setiap service memiliki workflow release sendiri.

Contoh:

.github/workflows/release-research-agent.yml
.github/workflows/release-memory-agent.yml
.github/workflows/release-analyst-agent.yml


Workflow hanya dijalankan apabila folder service tersebut berubah.

Contoh:
```yaml
paths:
  - services/research-agent/**
```

Keuntungan: perubahan pada Memory Agent tidak akan me-release Research Agent.

---

## 4. Directory Scoping
Selama implementasi ditemukan bahwa python-semantic-release secara default mencari konfigurasi dari root repository.

Karena CEREBRUM adalah monorepo, setiap action release wajib diberikan:
```yaml
directory: services/research-agent
```

agar:
- pyproject.toml yang dibaca benar
- version yang dibump benar
- build berjalan pada service yang tepat

Bukan root repository.

---

## 5. Tag Format per Service
Tag tidak menggunakan:

v0.1.0

melainkan:
```toml
tag_format = "research-agent-v{version}"
```

Contoh hasil:

research-agent-v0.1.0
research-agent-v0.1.1
memory-agent-v0.1.0
analyst-agent-v0.1.0


Keputusan ini mencegah konflik tag antar service.

---

## 6. Versioning dimulai dari 0.x
Implementasi final:
```toml
allow_zero_version = true
major_on_zero = false
```

Alasan: Research Agent masih experimental, belum layak dianggap API stabil.

Versi akan berkembang seperti:

0.1.0 → 0.1.1 → 0.2.0 → 0.3.0 → ... → 1.0.0

Bukan langsung `0.1.0 → 1.0.0`. Kesalahan ini sempat terjadi saat implementasi dan sudah diperbaiki.

---

## 7. Build Command
Action semantic-release berjalan di container Docker terpisah miliknya sendiri, yang hanya berisi Python + pip — **tidak ada `uv`** di dalamnya, walaupun job `test` di workflow yang sama menggunakan `uv`.

Konfigurasi final yang sudah terverifikasi jalan:
```toml
build_command = "pip install build && python -m build"
```

Bukan `uv build`. Keputusan ini membuat build berjalan konsisten di dalam container action PSR.

---

## 8. Build System
Seluruh service wajib mempunyai:
```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
```

Tanpa tabel ini:
- package project sendiri tidak ter-install oleh `uv sync`
- semantic-release gagal membuat wheel
- test gagal duluan dengan `ModuleNotFoundError`

Masalah ini ditemukan saat implementasi Research Agent.

---

## 9. Coverage Gate
Coverage minimum:

85%

Job `test` pada workflow release tidak akan lanjut ke job `release` apabila coverage gagal.

CLI entrypoint seperti `main.py` dikeluarkan dari coverage karena hanya berisi argparse, exit code, dan print — tanpa business logic. Business logic yang memanggil service eksternal (misalnya provider API) tetap wajib memiliki coverage, tidak boleh di-omit.

---

## 10. Release Pipeline
Pipeline release final, seluruhnya di dalam satu workflow `release-research-agent.yml`:

Push ke main (paths: services/research-agent/**)
│
▼
Job "test"

uv sync
pytest + coverage (fail-under 85%)
│
▼
PASS
│
▼
Job "release" (needs: test)
Semantic Release: version bump + Git Tag + CHANGELOG
│
▼
Build (pip install build && python -m build)
│
▼
GitHub Release + Upload Artifact

Release tidak pernah dijalankan apabila job `test` gagal.

Catatan: repo juga memiliki workflow terpisah `Research Agent CI` dari fase sebelumnya yang menjalankan pytest secara independen di luar alur release ini. Konsolidasi dua workflow test tersebut belum dilakukan dan bisa jadi item optimasi CI di masa depan — di luar scope ADR ini.

---

## 11. Artifact Strategy
Distribusi package menghasilkan:

dist/
├── research_agent-0.x.x.tar.gz
└── research_agent-0.x.x-py3-none-any.whl


Artifact:
- di-attach ke GitHub Release
- di-upload sebagai GitHub Actions Artifact

Publish ke PyPI **belum dilakukan**.

---

## 12. Monorepo Release Strategy
Setiap service mempunyai workflow sendiri, tag sendiri, version sendiri, changelog sendiri.

Contoh:

Research Agent → research-agent-v0.2.0
Memory Agent → memory-agent-v0.1.0
Analyst Agent → analyst-agent-v0.1.0


Tidak ada dependency release antar service.

---

# Consequences

## Positif
- Release sepenuhnya otomatis.
- Version selalu konsisten dengan commit history.
- Human error hampir hilang.
- Setiap service dapat berkembang sendiri.
- Mudah di-scale ke puluhan service.
- GitHub Release selalu sinkron dengan source code.
- Packaging telah tervalidasi.
- Struktur monorepo tetap bersih.

## Negatif
- Semua commit harus mengikuti Conventional Commits.
- Setiap service memiliki workflow release sendiri — sedikit duplikasi konfigurasi.
- Build release menggunakan `pip`/`python -m build`, bukan `uv`, karena keterbatasan container semantic-release.
- Job test di `release-research-agent.yml` saat ini berjalan terpisah dan tumpang tindih dengan workflow `Research Agent CI` yang sudah ada — belum dikonsolidasi.

---

# Alternatives Considered

### Manual Versioning
Ditolak. Sulit dipelihara dan rawan human error.

### Single Workflow Matrix
Ditolak untuk saat ini. Jumlah service masih sedikit sehingga workflow terpisah lebih mudah dipahami dan di-debug.

### bump2version
Ditolak. Tidak menyediakan automation GitHub Release sebaik python-semantic-release.

### Commitizen
Dipertimbangkan. Namun python-semantic-release memiliki integrasi GitHub Actions yang lebih matang sehingga dipilih sebagai standar CEREBRUM.

---

# Implementation Result
Status implementasi saat ADR ini ditulis:
- ✅ Conventional Commits
- ✅ python-semantic-release v10
- ✅ Service-scoped workflow
- ✅ Directory scoping
- ✅ Service-prefixed tags
- ✅ Zero-version strategy
- ✅ Automatic GitHub Release
- ✅ Automatic CHANGELOG
- ✅ Automatic wheel & sdist build
- ✅ Build-system configuration
- ✅ Coverage gate (85%)
- ✅ Artifact upload
- ✅ Monorepo-ready release architecture

Research Agent telah berhasil melakukan release otomatis dengan tag:

research-agent-v0.1.0
research-agent-v0.1.1

yang dihasilkan sepenuhnya melalui GitHub Actions tanpa proses manual.
