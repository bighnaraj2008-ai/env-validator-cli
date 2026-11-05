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
| `--format` | `text/json` | Telemetry rendering output mode | `text` |
| `--list-schemas` | None | Print available built-in schemas | Disabled |
