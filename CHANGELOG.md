# Changelog

All notable changes to `env-validator-cli` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.3.0] - 2026-11-04

### Added
- Expanded test suite with comprehensive fixture ingestion tests (`tests/fixtures/valid.env`, `malformed.env`, `missing_required.env`, `invalid_types.env`).
- Added edge-case test suites covering unquoted special characters, duplicate key resolution, integer casting bounds, and boolean parsing.
- Added mock environment fixture generator (`tests/harness/mock_env.py`) and assertion helpers (`tests/harness/assertions.py`).
- Added test execution runner script (`scripts/run_unit_tests.py`) and Markdown report generator (`scripts/generate_test_report.py`).
- Added performance benchmarks (`tests/performance/test_parser_perf.py`), stress tests (`tests/stress/test_env_storm.py`), and memory safety verification (`tests/memory/test_memory_safety.py`).
- Added automated profiler script (`scripts/run_profiler.py`) and GitHub Actions test coverage workflow (`.github/workflows/test_coverage.yml`).
- Added integration test suite (`tests/integration/test_cli_workflow.py`) and test configuration modules (`src/validator/test_config.py`, `src/validator/test_logger.py`).
- Added fixture generator utility (`examples/custom_fixture_generator.py`) and fixture checksum validator (`scripts/validate_fixtures.py`).
- Added artifact cleaner script (`scripts/clean_test_artifacts.py`) and comprehensive documentation (`docs/TEST_COVERAGE.md`, `docs/EDGE_CASES.md`, `docs/FIXTURE_GUIDE.md`, `docs/BENCHMARK_TEMPLATE.md`).

## [0.2.0] - 2026-11-03

### Added
- Modularized `.env` validation engine into `src/validator/` (`parser`, `rules`, `schema`, `reporter`, `cli`) and `src/config/` (`errors`, `settings`).
- Added strict declarative schema definitions (`schemas/env_schema.py`, `schemas/env_schema.yaml`) and `schemas/loader.py`.
- Added unit test suite under `tests/` (`test_parser`, `test_schema`, `test_rules`, `test_cli`) and `tests/harness/mock_env.py`.
- Added CLI automation wrappers (`scripts/validate_env.py`, `scripts/generate_template.py`, `scripts/smoke_test.sh`).
- Configured GitHub Actions CI matrix across Python 3.9-3.12 with Flake8 and Pytest.

<!-- Day 1 Core Architecture & Modular Refactoring Completed -->
