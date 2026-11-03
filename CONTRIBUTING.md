# Contributing to env-validator-cli

Thank you for contributing!

## Workflow
1. Fork and clone the repository.
2. Write unit tests under `tests/` for any new validation rule or parser change.
3. Run `flake8 main.py src schemas tests scripts` and `pytest tests/ -v`.
4. Never commit real `.env` secrets—use placeholder values in `examples/.env.example`.
