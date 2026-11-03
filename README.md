# env-validator-cli

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
