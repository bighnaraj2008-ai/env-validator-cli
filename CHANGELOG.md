# Changelog

All notable changes to `env-validator-cli` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.2.0] - 2026-11-03

### Added
- Modularized `.env` validation engine into `src/validator/` (`parser`, `rules`, `schema`, `reporter`, `cli`) and `src/config/` (`errors`, `settings`).
- Added strict declarative schema definitions (`schemas/env_schema.py`, `schemas/env_schema.yaml`) and `schemas/loader.py`.
- Added unit test suite under `tests/` (`test_parser`, `test_schema`, `test_rules`, `test_cli`) and `tests/harness/mock_env.py`.
- Added CLI automation wrappers (`scripts/validate_env.py`, `scripts/generate_template.py`, `scripts/smoke_test.sh`).
- Configured GitHub Actions CI matrix across Python 3.9-3.12 with Flake8 and Pytest.

<!-- Day 1 Core Architecture & Modular Refactoring Completed -->
