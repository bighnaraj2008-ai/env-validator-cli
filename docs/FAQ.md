# Frequently Asked Questions (FAQ)

### Q: Why zero external dependencies?
**A:** `env-validator-cli` is designed to run in minimal runtime environments (Docker scratch/alpine, CI runners, pre-commit hooks) without waiting for `pip install` or risking dependency conflicts.

### Q: How does this compare to `pydantic-settings`?
**A:** `pydantic-settings` requires full Python installation with heavy wheel builds. `env-validator-cli` works directly with Python 3.9+ standard library out-of-the-box.

### Q: Can I validate multiple schemas?
**A:** Yes! Pass `--schema path/to/custom_schema.yaml` to point to any declarative schema contract.

### Q: Does it support `.env.local` or environment cascading?
**A:** Yes, pass `--env .env.local` or use the CLI comparison flags to test override files.
---

### Q: What is the parser throughput for high-volume deployments?
**A:** `env-validator-cli` processes over 2,000 `.env` files per second on modern hardware, with sub-millisecond per-file validation latency.

---

### Q: How do I manage log disk usage on CI runners?
**A:** Run `python scripts/prune_logs.py --logs-dir logs/ --retention-days 7` in a scheduled cron or post-build step.
