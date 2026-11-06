# Frequently Asked Questions - CI/CD & Linter Automation

### Q: Why does `ci_validation.yml` run both `flake8` and `pytest`?
**A:** `flake8` guarantees strict code quality and syntax compliance before tests
execute, while `pytest` verifies behavioral correctness and schema logic.

---

### Q: How can I run the exact same checks locally before pushing?
**A:** Execute `./scripts/run_linter.sh` and `pytest tests/ -v`. Both mirror
the exact command flags executed by GitHub Actions runners.

---

### Q: How do I clean cached artifacts before running a release package build?
**A:** Run `python scripts/clean_cache.py` to remove `__pycache__/`, `.pytest_cache/`,
`build/`, and `dist/`.

---

### Q: What Python versions are tested in CI?
**A:** Python 3.9, 3.10, 3.11, and 3.12 are tested in parallel on `ubuntu-latest`.
