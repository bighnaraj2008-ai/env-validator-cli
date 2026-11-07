# Production Deployment Readiness Checklist for CLI Tools

Checklist for deploying `env-validator-cli` into production CI/CD pipelines.

---

## 1. Pre-Deployment Verification

- [ ] All unit and edge-case tests passing (`pytest tests/ -v`).
- [ ] Static analysis clean (`flake8 main.py src schemas tests scripts`).
- [ ] Documentation links verified (`python scripts/validate_docs.py`).
- [ ] Memory footprint bounded under 1 MB peak (`python tests/benchmarks/bench_memory.py`).

---

## 2. Pipeline Integration

- [ ] Pipeline step configured with strict validation (`--strict`).
- [ ] Machine-readable JSON output piped to log aggregation (`--format json`).
- [ ] Secret rotation and retention policy applied via `scripts/prune_logs.py`.
