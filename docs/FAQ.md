# Frequently Asked Questions (FAQ)

### Q: Why zero external dependencies?
**A:** `env-validator-cli` is designed to run in minimal runtime environments (Docker scratch/alpine, CI runners, pre-commit hooks) without waiting for `pip install` or risking dependency conflicts.

### Q: How does this compare to `pydantic-settings`?
**A:** `pydantic-settings` requires full Python installation with heavy wheel builds. `env-validator-cli` works directly with Python 3.9+ standard library out-of-the-box.

### Q: Can I validate multiple schemas?
**A:** Yes! Pass `--schema path/to/custom_schema.yaml` to point to any declarative schema contract.

### Q: Does it support `.env.local` or environment cascading?
**A:** Yes, pass `--env .env.local` or use the CLI comparison flags to test override files.
