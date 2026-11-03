# ARCHITECTURE REFACTOR — env-validator-cli

**Day 1 — Core modularization, strict schema validation, and error reporting.**

This document describes the modular validation workflow and parsing flow
introduced in the Day 1 refactor. It is intended for contributors and
operators who need to extend or maintain the validator.

---

## 1. Goals

| Goal | How it is achieved |
|------|--------------------|
| **Separation of concerns** | Parsing, schema rules, and reporting live in independent modules. |
| **Strict type validation** | Values are cast against declared types (`string`, `integer`, `number`, `boolean`) before pattern checks. |
| **Structured error reporting** | Every violation is a `ValidationIssue` with key, code, message, severity, expected/actual values. |
| **Zero dependencies** | Pure Python standard library; works in CI/CD, Docker, and pre-commit hooks. |
| **Extensible schemas** | New environment contracts are added as schema template files under `schemas/`. |

---

## 2. Project Structure (post-refactor)

```text
env-validator-cli/
├── .env                 # Local configuration (gitignored)
├── .env.example         # Authoritative key template
├── .gitignore           # Ignores venv/, __pycache__/, .env, *.log, .vscode/, .idea/
├── main.py              # CLI entry point (argparse → modules)
├── README.md            # User-facing usage guide
├── docs/
│   └── ARCHITECTURE_REFACTOR.md   # This document
├── schemas/
│   ├── __init__.py      # Package marker, re-exports ENV_SCHEMA
│   └── env_schema.py    # Default schema template (ENV_SCHEMA + SchemaCatalog)
└── src/
    ├── __init__.py      # Package root
    ├── config/
    │   ├── __init__.py  # Re-exports settings + errors
    │   ├── errors.py    # Custom exceptions + ValidationIssue dataclass
    │   └── settings.py  # EnvType, EnvFieldSchema, ValidationConfig
    └── validator/
        ├── __init__.py  # Public API surface
        ├── parser.py    # .env parsing (tokenize → unquote → dict)
        ├── rules.py     # RequiredRule, TypeCastRule, PatternRule, MinLengthRule
        ├── schema.py    # Schema engine + ValidationReport
        └── reporter.py  # ConsoleReporter (text / JSON output)
```

---

## 3. Module Responsibilities

### `src/config/errors.py` — Error handling

Defines the exception hierarchy and the structured issue type:

* `EnvValidationError` — base exception; every validator error derives from it.
* `EnvFileNotFoundError`, `EnvParseError` — input/file problems.
* `MissingEnvVarError`, `TypeCastError`, `PatternMismatchError` — semantic violations.
* `SchemaError` — the schema definition itself is invalid (bad type, bad regex).
* `ValidationIssue` — immutable record of one violation (`key`, `code`, `message`,
  `severity`, `expected`, `actual`). Convertible to `dict` for JSON output.
* `IssueSeverity` — `"error"` or `"warning"`.

### `src/config/settings.py` — Configuration

* `EnvType` — supported cast targets: `STRING`, `INTEGER`, `NUMBER`, `BOOLEAN`.
* `EnvFieldSchema` — frozen declaration of one variable's contract
  (`name`, `required`, `type`, `pattern`, `min_length`, `default`, `description`).
  Validates its own type and pattern in `__post_init__`.
* `ValidationConfig` — runtime knobs (`env_file`, `strict`, `warn_on_extra`,
  `compare_example`, `encoding`).

### `src/validator/parser.py` — .env parsing

`parse_env_file(path, encoding="utf-8") -> ParsedEnv`:

1. Reads the file (raises `EnvFileNotFoundError` if missing/unreadable).
2. Skips blank lines and `#` comments.
3. Strips a leading `export ` prefix (shell-style).
4. Splits on the first `=`; empty key or missing `=` raises `EnvParseError`.
5. Unquotes matching single/double quotes around the value.

Returns `ParsedEnv(values={...}, source=..., line_count=...)`. A
`parse_env_text(text, source=...)` variant is available for tests.

### `src/validator/rules.py` — Validation rules

Stateless rules, each implementing `Rule.check(key, value, schema) -> ValidationResult`:

| Rule | Code | Enforces |
|------|------|----------|
| `RequiredRule` | `missing` | Required variables are present and non-empty. |
| `TypeCastRule` | `type_mismatch` | Strict cast to `EnvType`; booleans accept `1/0`, `true/false`, `yes/no`, `on/off`. |
| `PatternRule` | `pattern_mismatch` | `re.search` against the field's regex pattern. |
| `MinLengthRule` | `too_short` | String length >= `min_length` (secrets/tokens). |

`DEFAULT_RULES` bundles them in pipeline order: required → type → pattern → length.

### `src/validator/schema.py` — Schema engine

* `Schema` — holds declared fields + rule pipeline; `validate(values, config)`
  runs every rule against every declared field and returns a `ValidationReport`.
  In strict mode it also flags undeclared keys present in the environment.
* `ValidationReport` — aggregates issues; exposes `errors`, `warnings`, and the
  `passed` property (no errors). Serializes via `to_dict()`.

### `src/validator/reporter.py` — Error reporting

`ConsoleReporter` renders a report as plain text (default) or JSON.
Colours/emojis are used only on TTYs; piped/CI output is plain and
machine-friendly. Returns exit code `0` on pass, `1` on failure.

---

## 4. Validation Workflow

```
┌──────────────┐      ┌─────────────────┐      ┌──────────────────┐
│  CLI (main)  │────▶│   parser.py     │────▶│   rules.py       │
│  argparse    │      │  .env → dict    │      │  required/type/  │
└──────────────┘      └─────────────────┘      │  pattern/length  │
      │                                         └────────┬─────────┘
      │                                                  │
      │      ┌────────────────┐      ┌──────────────────┘
      │      │   schema.py    │◀─────┤
      │      │  Schema engine │      │
      └─────▶│  + report      │      │
             └────────────────┘      │
                   │                 │
                   ▼                 ▼
             ┌─────────────────────────────┐
             │ reporter.py                 │
             │ ConsoleReporter (text/JSON) │
             └─────────────────────────────┘
                         │
                         ▼
                    exit code (0/1/2)
```

Steps:

1. **Parse** — `.env` → `dict[str, str]` via `parse_env_file`.
2. **Validate** — `Schema.validate()` applies `DEFAULT_RULES` to each declared field.
3. **Report** — `ConsoleReporter` prints errors/warnings and returns an exit code.

### Legacy mode

`--compare-example` preserves the original behaviour: key-set diff between
`.env` and `.env.example` (missing/extra keys only, no typing).

---

## 5. Extending the Schema

1. Open `schemas/env_schema.py`.
2. Append an `EnvFieldSchema` to the `ENV_SCHEMA.fields` list.
3. Choose `required`, `type`, and optionally `pattern` / `min_length`.
4. Run `python main.py` — new fields are enforced immediately.

To add a new rule:

1. Subclass `Rule` in `src/validator/rules.py` and implement `check()`.
2. Add it to `DEFAULT_RULES` or pass a custom `rules` sequence to `Schema(...)`.

---

## 6. CLI Usage

```bash
# Default: strict schema validation against .env
python main.py

# Strict mode: also fail on keys not declared in the schema
python main.py --strict

# JSON output for CI/CD
python main.py --format json

# Validate a different environment file
python main.py --env .env.production --schema default

# Legacy key-sync check vs .env.example
python main.py --compare-example

# List available schema templates
python main.py --list-schemas
```

Exit codes: `0` valid, `1` validation failed, `2` usage/file error.

---

## 7. Error Handling Philosophy

* **Fail fast on configuration problems**: missing files and unreadable input
  raise exceptions that the CLI converts to exit code `2`.
* **Collect, don't abort**: all rule violations across all fields are gathered
  into one report so a developer sees every problem in a single run.
* **Never print from logic**: parser, rules, and schema modules raise or
  return structured data; only the reporter layer renders output. This keeps
  the core testable without mocking stdout.
