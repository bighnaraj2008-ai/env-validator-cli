# CI Runner Performance Benchmark Tracking Guide

Monitoring workflow duration keeps developer feedback cycles fast across the
multi-version matrix.

---

## 1. Workflow Execution Targets

| Workflow | Runner OS | Target Duration | Notes |
|:---------|:----------|:---------------:|:------|
| `ci_validation.yml` | `ubuntu-latest` | `< 60s` per matrix job | Uses `cache: "pip"` for fast setup |
| `python_lint.yml` | `ubuntu-latest` | `< 30s` | Static analysis with flake8 + black |
| `docs_check.yml` | `ubuntu-latest` | `< 20s` | Stdlib Python link verification |
| `security_scan.yml` | `ubuntu-latest` | `< 45s` | Bandit + secret grep |
| `dependency_check.yml` | `ubuntu-latest` | `< 30s` | Dependency tree validation (`pip check`) |

---

## 2. Tracking Regression in Pull Requests

Monitor CI step durations to ensure test suites and static analysis remain
performant as new rules are added.
