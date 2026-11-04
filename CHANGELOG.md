# Changelog

All notable changes to `env-validator-cli` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.3.0] - 2026-11-04

### Added
- **Test Fixtures Suite**: Initialized comprehensive mock environment fixtures (`valid.env`, `malformed.env`, `missing_required.env`, `invalid_types.env`).
- **Edge-Case Validation**: Implemented dedicated tests for unquoted special characters, duplicate key overrides, integer/number casting limits, and strict boolean coercion.
- **Harness & Assertion Helpers**: Added fixture generation utilities (`tests/harness/mock_env.py`) and custom assertion macros with rich failure diagnostics (`tests/harness/assertions.py`).
- **Automation & Reporting**: Developed `scripts/run_unit_tests.py` with fixture ingestion telemetry and `scripts/generate_test_report.py` for automated Markdown reports.
- **Performance & Stress Telemetry**: Built micro-benchmarks (`tests/performance/test_parser_perf.py`), 5,000-variable stress tests (`tests/stress/test_env_storm.py`), and memory profile verification (`tests/memory/test_memory_safety.py`).
- **CI/CD Automation**: Introduced GitHub Actions workflow `.github/workflows/test_coverage.yml` validating coverage and profiling across Python 3.9-3.12.
- **Documentation**: Authored `docs/TEST_COVERAGE.md`, `docs/EDGE_CASES.md`, `docs/FIXTURE_GUIDE.md`, and `docs/BENCHMARK_TEMPLATE.md`.

## [0.2.0] - 2026-11-03

### Added
- Modularized `.env` validation engine into `src/validator/` (`parser`, `rules`, `schema`, `reporter`, `cli`) and `src/config/` (`errors`, `settings`).
- Added strict declarative schema definitions (`schemas/env_schema.py`, `schemas/env_schema.yaml`) and `schemas/loader.py`.
- Added unit test suite under `tests/` (`test_parser`, `test_schema`, `test_rules`, `test_cli`) and `tests/harness/mock_env.py`.
- Added CLI automation wrappers (`scripts/validate_env.py`, `scripts/generate_template.py`, `scripts/smoke_test.sh`).
- Configured GitHub Actions CI matrix across Python 3.9-3.12 with Flake8 and Pytest.

<!-- Day 2 Test Coverage & Fixture Improvements Sprint Completed -->
