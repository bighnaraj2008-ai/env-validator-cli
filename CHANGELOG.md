# Changelog

All notable changes to `env-validator-cli` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.0] - 2026-11-06

### Added
- **CI/CD Automation Pipelines**:
  - Added multi-version Python build matrix workflow (`.github/workflows/ci_validation.yml`) spanning Python 3.9 through 3.12.
  - Added dedicated static analysis workflow (`.github/workflows/python_lint.yml`) for flake8 and black.
  - Added release packaging and wheel publishing workflow (`.github/workflows/release_package.yml`).
  - Added security vulnerability and secret scanning workflow (`.github/workflows/security_scan.yml`).
  - Added GitHub CodeQL advanced semantic analysis workflow (`.github/workflows/code_ql.yml`).
  - Added dependency validation and checksum workflow (`.github/workflows/dependency_check.yml`).
- **Linter & Formatting Automation**:
  - Initialized strict `.flake8` configuration and `[tool.black]` formatting settings in `pyproject.toml`.
  - Added local helper scripts: `scripts/run_linter.sh`, `scripts/check_formatting.sh`, and `scripts/format_code.sh`.
  - Authored comprehensive coding standards guide ([`docs/LINTER_STANDARDS.md`](docs/LINTER_STANDARDS.md)) and CI architecture guide ([`docs/CI_CD_PIPELINE.md`](docs/CI_CD_PIPELINE.md)).
- **Community & Governance Templates**:
  - Added automated Dependabot configuration (`.github/dependabot.yml`).
  - Added standardized GitHub issue templates for bug reports and feature requests.
  - Added pull request review checklist template (`.github/pull_request_template.md`).
  - Added version release runbook ([`docs/RELEASE_PROCESS.md`](docs/RELEASE_PROCESS.md)) and bump script (`scripts/bump_version.sh`).
  - Added security reporting policy ([`docs/SECURITY_POLICY.md`](docs/SECURITY_POLICY.md)).
  - Added CI automation FAQ ([`docs/FAQ_AUTOMATION.md`](docs/FAQ_AUTOMATION.md)) and runner benchmark tracking ([`docs/BENCHMARK_CI.md`](docs/BENCHMARK_CI.md)).
- **Testing & Diagnostics**:
  - Added workflow build matrix verification test (`tests/ci/test_build_matrix.py`).
  - Added CI diagnostic health check script (`scripts/health_check.py`).
  - Added workflow cache cleaner utility (`scripts/clean_cache.py`).
  - Added sample GitHub Actions integration snippet (`examples/github_actions_snippet.yaml`).
  - Added automated style compliance test runner (`tests/linter/test_style_compliance.py`).
  - Added CI build troubleshooting guide ([`docs/TROUBLESHOOTING_CI.md`](docs/TROUBLESHOOTING_CI.md)).

## [1.0.0] - 2026-11-05

### Added
- **Core Architecture & Specifications**:
  - Authored comprehensive YAML schema authoring guide ([`docs/SCHEMA_AUTHORING.md`](docs/SCHEMA_AUTHORING.md)).
  - Added full command-line usage and exit code guide ([`docs/CLI_USAGE.md`](docs/CLI_USAGE.md)).
  - Added system architecture Mermaid diagrams ([`docs/ARCHITECTURE.mmd`](docs/ARCHITECTURE.mmd)).
  - Authored API reference guide ([`docs/API_REFERENCE.md`](docs/API_REFERENCE.md)) for core parser and schema engine.
- **Operations & Runbooks**:
  - Added production deployment runbook ([`docs/DEPLOYMENT_GUIDE.md`](docs/DEPLOYMENT_GUIDE.md)) and diagnostics playbook ([`docs/DIAGNOSTICS.md`](docs/DIAGNOSTICS.md)).
  - Added security hardening guide ([`docs/SECURITY_HARDENING.md`](docs/SECURITY_HARDENING.md)), contributors guide ([`docs/CONTRIBUTORS_GUIDE.md`](docs/CONTRIBUTORS_GUIDE.md)), and FAQ ([`docs/FAQ.md`](docs/FAQ.md)).
  - Added configuration glossary ([`docs/GLOSSARY.md`](docs/GLOSSARY.md)), benchmark reports ([`docs/BENCHMARK_REPORT.md`](docs/BENCHMARK_REPORT.md)), and incident playbook ([`docs/INCIDENT_PLAYBOOK.md`](docs/INCIDENT_PLAYBOOK.md)).
  - Added version migration guide ([`docs/MIGRATION_V2.md`](docs/MIGRATION_V2.md)) and environment governance guide ([`docs/ENV_GOVERNANCE.md`](docs/ENV_GOVERNANCE.md)).
- **Automation & Tooling**:
  - Added automated markdown link validator script (`scripts/validate_docs.py`) and CI workflow (`.github/workflows/docs_check.yml`).
  - Added schema documentation generator script (`scripts/generate_schema_docs.py`).
  - Added documentation syntax and structure unit tests (`tests/docs/test_markdown_syntax.py`).

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

<!-- Day 3 Advanced Documentation Sprint Finalized & Locked -->
<!-- Day 4 CI/CD & Automation Milestone Finalized & Locked -->
