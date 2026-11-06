# CI/CD Pipeline - env-validator-cli

Automated build, test, static analysis, and release workflows for
`env-validator-cli`. All pipelines run on GitHub Actions and are triggered by
pushes to `main`, pull requests, and version tags.

---

## 1. Pipeline Overview

| Workflow | File | Trigger | Purpose |
|:---------|:-----|:--------|:--------|
| CI Validation | [`.github/workflows/ci_validation.yml`](../.github/workflows/ci_validation.yml) | push / PR to `main` | Build + test + lint across Python 3.9-3.12 |
| Python Lint | [`.github/workflows/python_lint.yml`](../.github/workflows/python_lint.yml) | PR to `main` | flake8 + black static analysis |
| Release Package | [`.github/workflows/release_package.yml`](../.github/workflows/release_package.yml) | push tag `v*` | Build wheel/sdist and publish |
| Test Coverage | [`.github/workflows/test_coverage.yml`](../.github/workflows/test_coverage.yml) | push / PR to `main` | Coverage & performance profiling |
| Documentation | [`.github/workflows/docs_check.yml`](../.github/workflows/docs_check.yml) | push / PR to `main` | Markdown link & syntax verification |
| Security Scan | [`.github/workflows/security_scan.yml`](../.github/workflows/security_scan.yml) | push / PR / cron | Bandit + secret vulnerability scan |
| CodeQL | [`.github/workflows/code_ql.yml`](../.github/workflows/code_ql.yml) | push / PR / weekly | Semantic data-flow security analysis |
| Dependency Check | [`.github/workflows/dependency_check.yml`](../.github/workflows/dependency_check.yml) | push / PR to `main` | Dependency tree & integrity checks |

---

## 2. Build Matrix & Runner Specifications

The CI Validation job uses a multi-version build matrix to guarantee
compatibility across supported Python releases:

| Matrix Axis | Values | Purpose |
|:------------|:-------|:--------|
| `python-version` | 3.9, 3.10, 3.11, 3.12 | Multi-version standard runtime verification |
| `runs-on` | `ubuntu-latest` | Standard Linux runner environment |
| `fail-fast` | `false` | All matrix jobs complete independently |

Each matrix cell executes:
1. `pip install --upgrade pip` and `pip install ".[dev]"`
2. Static analysis with `flake8 main.py src schemas tests scripts`
3. Unit and integration tests with `pytest tests/ -v`
4. Pre-flight smoke test with `bash scripts/smoke_test.sh`

---

## 3. Local Reproduction

Developers can execute the exact pipeline steps locally prior to pushing:

```bash
# 1. Lint with flake8
flake8 main.py src schemas tests scripts

# 2. Run test suite
pytest tests/ -v

# 3. Pre-flight integration smoke test
bash scripts/smoke_test.sh

# 4. Verify documentation links
python scripts/validate_docs.py
```
