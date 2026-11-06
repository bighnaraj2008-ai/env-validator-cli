# Python Coding Standards and Linter Rule Guide

All source code, test suites, and automation scripts in `env-validator-cli`
must pass automated static analysis before merging.

---

## 1. Python Standards (`black` + `flake8`)

Configuration is defined centrally in [`pyproject.toml`](../pyproject.toml) and [`.flake8`](../.flake8).

| Tool | Setting | Value | Rationale |
|:-----|:--------|:------|:----------|
| `black` | `line-length` | `100` | Clean readable formatting across all editors |
| `black` | `target-version` | `py39` | Syntax compatibility across Python 3.9-3.12 |
| `flake8` | `max-line-length` | `120` | Permits descriptive assertion lines without wrapping |
| `flake8` | `extend-ignore` | `E203, W503` | Avoids whitespace-before-colon conflicts with slicing |
| `flake8` | `per-file-ignores` | `__init__.py: F401` | Allows clean package exports |

---

## 2. Running Linters Locally

```bash
# Run flake8 static analysis
flake8 main.py src schemas tests scripts

# Check formatting with black
python -m black --check --diff main.py src schemas tests scripts

# Auto-format sources
./scripts/format_code.sh
```
