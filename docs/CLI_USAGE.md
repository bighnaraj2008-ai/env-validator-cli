# Command-Line Interface (CLI) Usage Guide

`env-validator-cli` provides a zero-dependency CLI tool to validate, cast,
and synchronize `.env` configurations.

---

## 1. Synopsis & Core Flags

```bash
python main.py [OPTIONS]
```

### Options Reference

| Flag | Argument | Description | Default |
|---|---|---|---|
| `--env` | `PATH` | Path to target `.env` file | `.env` |
| `--schema` | `PATH` | Path to declarative YAML schema | `schemas/env_schema.yaml` |
| `--strict` | None | Reject undeclared variables | Disabled |
| `--format` | `text|json` | Telemetry rendering output mode | `text` |
| `--list-schemas` | None | Print available built-in schemas | Disabled |

---

## 2. Exit Codes & CI/CD Pipeline Automation

`env-validator-cli` returns POSIX standard process exit codes to halt failing builds:

| Exit Code | Classification | Meaning | Action Required |
|---|---|---|---|
| `0` | **PASS** | Configuration valid | Proceed with container build or service boot |
| `1` | **FAIL** | Validation errors found | Check missing variables or type mismatch errors |
| `2` | **ERROR** | File or runtime error | Verify file paths, permissions, and arguments |

### GitHub Actions Step Example
```yaml
- name: Validate Environment Configuration
  run: |
    python main.py --env .env.staging --strict
```

---

## 3. Automated Template Generation & Drift Detection

Synchronize `.env.example` templates directly from your schema:

```bash
# Generate a fresh .env.example with descriptive comments
python scripts/generate_template.py --output .env.example

# Compare local .env against .env.example to detect key drift
python scripts/validate_env.py --env .env --compare-example --example .env.example
```
