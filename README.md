# env-validator-cli

[![Env Validator CI](https://github.com/bighnaraj2008-ai/env-validator-cli/actions/workflows/validator_ci.yml/badge.svg)](https://github.com/bighnaraj2008-ai/env-validator-cli/actions/workflows/validator_ci.yml)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style: Flake8](https://img.shields.io/badge/code%20style-flake8-brightgreen.svg)](https://flake8.pycqa.org/)

> **Industry-grade, zero-dependency CLI tool to validate, cast, and synchronize `.env` configurations against strict schemas and `.env.example` templates.**

---

## Overview

In modern cloud-native and 12-factor application architectures, environment variables
drive configuration across environments (Local, Staging, Production). A frequent source
of runtime crashes and deployment failures is **configuration drift**—missing keys,
malformed URLs, invalid integer ports, or short signing secrets.

`env-validator-cli` catches misconfigurations before boot by validating every `.env`
variable against strict type, regex, length, and required rules.

---

## Modular Architecture

```text
env-validator-cli/
├── main.py                        # CLI entrypoint (argparse -> modules)
├── schemas/
│   ├── env_schema.py              # Default schema contract (ENV_SCHEMA)
│   ├── env_schema.yaml            # Declarative YAML schema template
│   └── loader.py                  # YAML schema loader
├── src/
│   ├── config/
│   │   ├── errors.py              # Custom exception hierarchy + ValidationIssue
│   │   └── settings.py            # EnvType, EnvFieldSchema, ValidationConfig
│   └── validator/
│       ├── parser.py              # Dependency-free .env parser
│       ├── rules.py               # Required, TypeCast, Pattern, MinLength rules
│       ├── schema.py              # Schema validation engine + ValidationReport
│       ├── reporter.py            # Console text + JSON reporter
│       └── cli.py                 # CLI delegation module
├── scripts/
│   ├── validate_env.py            # CLI wrapper script
│   ├── generate_template.py       # .env.example template generator
│   └── smoke_test.sh              # Pre-flight integration smoke check
└── tests/                         # Unit tests & mock harness
```

For full module specs and data-flow diagrams, see [`docs/ARCHITECTURE_REFACTOR.md`](docs/ARCHITECTURE_REFACTOR.md) and [`docs/SCHEMA_GUIDE.md`](docs/SCHEMA_GUIDE.md).

---

## Quickstart Guide

### 1. Installation

```bash
git clone https://github.com/bighnaraj2008-ai/env-validator-cli.git
cd env-validator-cli
python -m pip install -e ".[dev]"
```

*(Because the core engine uses only Python's standard library, `python main.py` also runs directly without external installs.)*

### 2. Validate Environment Files

```bash
# Strict schema validation against an example file
python main.py --env .env.example

# Strict hygiene mode (fails on undeclared extra keys)
python main.py --env .env.example --strict

# Machine-readable JSON output for CI/CD gates
python main.py --env .env.example --format json

# Legacy key-sync check against .env.example
python main.py --env .env.example --compare-example
```

### 3. Run Unit Tests & Linters

```bash
pytest tests/ -v
flake8 main.py src schemas tests scripts
```

---

## Troubleshooting

- **`EnvFileNotFoundError`:** Ensure `--env` points to an existing file (default is `.env`; pass `--env .env.example` in CI).
- **Unexpected extra keys in `--strict` mode:** Add newly introduced keys to `schemas/env_schema.py` or `schemas/env_schema.yaml`.
- **`TypeCastError` on booleans:** Accepted truthy/falsy strings are `1/0`, `true/false`, `yes/no`, and `on/off` (case-insensitive).

---

## Contributing & Security

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for development guidelines and [`SECURITY.md`](SECURITY.md) for responsible disclosure.

---

## License

Licensed under the MIT License — see [`LICENSE`](LICENSE) for details.
