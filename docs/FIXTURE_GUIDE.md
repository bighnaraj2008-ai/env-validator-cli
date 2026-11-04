# Guide to Authoring Custom `.env` Test Fixtures

Test fixtures provide deterministic environment inputs to verify parser robustness
and schema validation error reporting.

---

## 1. Directory Structure

Fixtures reside under `tests/fixtures/`:
- `valid.env`: Complete configuration satisfying all schema contracts.
- `malformed.env`: Syntax anomalies for parser error testing.
- `missing_required.env`: Missing required keys for contract violation testing.
- `invalid_types.env`: Type-casting and regex mismatch scenarios.

---

## 2. Naming Conventions

- Use lowercase filenames with `.env` extension (e.g., `feature_flag_test.env`).
- Accompany test cases in `tests/test_fixtures.py`.
- Ensure values never contain real production secrets.

---

## 3. Synthetic Fixture Generation

Use `examples/custom_fixture_generator.py` to produce test configurations:
```bash
python examples/custom_fixture_generator.py --out tests/fixtures/staging.env --tier staging --port 9090
```
