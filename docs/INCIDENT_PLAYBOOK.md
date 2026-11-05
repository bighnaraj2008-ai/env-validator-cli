# Startup Failure & Misconfigured Environment Incident Playbook

Runbook for on-call engineers responding to deployment failures caused by configuration errors.

---

## Severity 1: Application Boot Loop (Missing Required Key)

### Symptoms
- Container terminates immediately upon launch with exit code 1.
- Log output: `[missing] DATABASE_URL is required but not declared`.

### Triage Actions
1. Inspect deployment manifest to confirm secret/ConfigMap mounting.
2. Run validation locally:
   ```bash
   python main.py --env /path/to/deployed/.env --schema schemas/env_schema.yaml
   ```
3. Inject missing parameter via orchestrator or secret manager.
4. Restart service pods.
