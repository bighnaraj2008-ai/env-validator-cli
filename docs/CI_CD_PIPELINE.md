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
