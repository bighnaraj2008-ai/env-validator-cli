# TEST COVERAGE — env-validator-cli (Day 2)

Test fixtures, edge-case unit tests, the automated test harness, and the
validation matrices used to verify `env-validator-cli`.

---

## 1. Test layout

```text
tests/
├── __init__.py
├── test_cli.py               # CLI entrypoint (exit codes, JSON output, strict mode)
├── test_parser.py            # .env parser: comments, export, quotes, BOM, errors
├── test_rules.py             # required / type-cast / pattern / min-length rules
├── test_schema.py            # Schema engine, YAML loader, duplicate fields
├── test_edge_cases.py        # Day 2: unquoted special chars, dupes, casts, booleans
├── test_fixtures.py          # Day 2: parser output vs fixture telemetry
├── harness/
│   └── mock_env.py           # Fixture writer helper for temp .env files
└── fixtures/
    ├── __init__.py
    ├── valid.env             # All 10 ENV_SCHEMA fields, valid values
    ├── malformed.env         # Syntax anomalies (no '=', empty key)
    ├── missing_required.env  # Omits PORT, JWT_SECRET, DATABASE_URL, REDIS_URL
    └── invalid_types.env     # Type, pattern, and min-length violations
```

`scripts/run_unit_tests.py` ingests the fixtures, runs the suite with pytest,
and prints a structured diagnostic summary (human-readable + JSON).

---

## 2. Fixture specifications

| Fixture | Contents | Expected outcome |
|---------|----------|------------------|
| `tests/fixtures/valid.env` | All 10 `ENV_SCHEMA` keys with conforming values (`APP_ENV=production`, `PORT=8000`, `DEBUG=true`, 8+ char secrets, URL patterns) | Parser telemetry: 10 keys. Schema `ValidationReport.passed == True`, 0 errors. |
| `tests/fixtures/malformed.env` | Mix of valid lines and `INVALID_LINE_WITHOUT_EQUALS` / `=value_without_key` | `parse_env_file` raises `EnvParseError`. |
| `tests/fixtures/missing_required.env` | `APP_NAME`, `APP_ENV`, `DEBUG`, `SECRET_KEY`, `API_KEY` only | Parses fine; schema validation reports `missing` errors for `PORT`, `JWT_SECRET`, `DATABASE_URL`, `REDIS_URL`. |
| `tests/fixtures/invalid_types.env` | `APP_ENV=invalid-tier`, `PORT=not-a-number`, `DEBUG=maybe`, `SECRET_KEY=short`, bad URL patterns | Schema validation reports `pattern_mismatch`, `type_mismatch`, `too_short` errors, each with `expected`/`actual` telemetry. |

---

## 3. Edge-case validation matrix (`tests/test_edge_cases.py`)

| Scenario | Covered by | Assertion |
|----------|-----------|-----------|
| Unquoted `=` inside values | `test_unquoted_special_characters_are_preserved` | `KEY=value=with=equals` → `"value=with=equals"` |
| Nested quotes inside values | same | `'single=double=mixed'` → `"single=double=mixed"` |
| Surrounding whitespace on values | same | `"  padded  "` → `"padded"` |
| Empty values | same | `EMPTY=` → `""` |
| Duplicate keys | `test_duplicate_keys_resolve_to_last_value` | Last declaration wins (dict semantics) |
| Comments and blank lines | `test_comment_and_blank_lines_do_not_pollute_telemetry` | Skipped in values; still counted in `line_count` |
| `export ` prefix | `test_export_prefix_is_stripped` | `export APP_NAME=x` → `APP_NAME=x` |
| Integer cast: valid | `test_integer_cast_rejects_non_numeric_and_float_strings` | `"8080"`, `"0"`, `"-42"` pass |
| Integer cast: float / hex / alphanumeric | same | `"12.5"`, `"0x10"`, `"8k"`, `"1_000"` → `type_mismatch` |
| Number cast: decimals | `test_number_cast_accepts_decimals` | `"3.5"`, `"10"` pass; `"not-a-float"` fails |
| Boolean cast: true forms | `test_boolean_cast_accepts_common_true_false_forms` | `1/true/t/yes/y/on` (any case) pass |
| Boolean cast: false forms | same | `0/false/f/no/n/off` (any case) pass |
| Boolean cast: invalid | `test_boolean_cast_rejects_invalid_values` | `maybe/2/-1/enabled/""` → `type_mismatch` |
| Required rule: missing / empty | `test_required_rule_rejects_empty_and_missing` | `None` and `""` fail; whitespace-only passes |
| Malformed text | `test_malformed_text_raises_parse_error` | No-`=` line and `=value` raise `EnvParseError` |

---

## 4. Parser anomaly coverage (`tests/test_fixtures.py`)

| Fixture | Test | What is verified |
|---------|------|------------------|
| `valid.env` | `test_valid_env_parses_to_expected_telemetry` | Exact key set, `source` path, positive `line_count`, schema passes with 0 errors/warnings |
| `malformed.env` | `test_malformed_env_raises_parse_error` | `EnvParseError` raised on injected syntax anomalies |
| `missing_required.env` | `test_missing_required_env_detected_by_schema` | Parser telemetry well-formed; schema reports exactly the omitted required keys as `missing` errors |
| `invalid_types.env` | `test_invalid_types_env_detected_by_schema` | Each injected violation produces an error carrying `expected`/`actual` telemetry |

---

## 5. Test harness (`scripts/run_unit_tests.py`)

The runner performs four stages:

1. **Fixture ingestion** — asserts all four required fixtures exist, counts `KEY=value` lines per fixture, classifies the expected anomaly.
2. **Test execution** — runs `pytest tests/ -v --tb=short -p no:cacheprovider` (or a subset when paths are passed as arguments).
3. **Measurement** — parses the pytest summary for passed/failed/error counts, computes the pass rate, and collects per-test statuses.
4. **Diagnostic summary** — prints a human-readable table followed by a JSON block with `generated_at`, fixture telemetry, test counts, pass rate, per-test results, and exit code.

Exit codes: `0` = all fixtures present and all tests pass; `1` = any fixture missing or any test failure/error.

Usage:

```bash
# Full suite with structured diagnostics
python scripts/run_unit_tests.py

# JSON-only output (CI-friendly)
python scripts/run_unit_tests.py --json-only

# Run a subset
python scripts/run_unit_tests.py tests/test_edge_cases.py tests/test_fixtures.py
```

---

## 6. Pre-existing test modules

| Module | Scope |
|--------|-------|
| `tests/test_cli.py` | `--list-schemas`, JSON format (`fields_checked == 10`), `--strict` exit code 1 on undeclared key, `--compare-example` exit 0 on matching keys |
| `tests/test_parser.py` | Comment/export/quote stripping, `EnvFileNotFoundError`, `EnvParseError`, BOM roundtrip |
| `tests/test_rules.py` | Required/optional, int/boolean casts, regex patterns, min-length |
| `tests/test_schema.py` | Valid values pass, strict mode flags undeclared keys, duplicate field → `SchemaError`, YAML loader yields 10 fields with `PORT` as integer |

---

## 7. Running the suite locally

```bash
# Everything (Day 1 + Day 2 tests)
python scripts/run_unit_tests.py

# Equivalent raw pytest
python -m pytest tests/ -v

# Day 2 only
python scripts/run_unit_tests.py tests/test_edge_cases.py tests/test_fixtures.py
```

---

## 8. Coverage notes

* **Zero external test dependencies** beyond pytest (already a project dev dependency).
* Fixture files live under `tests/fixtures/` and contain only dummy values — no real secrets.
* The harness intentionally does not write artifacts (no report files, caches, or logs) so repository hygiene stays clean.
