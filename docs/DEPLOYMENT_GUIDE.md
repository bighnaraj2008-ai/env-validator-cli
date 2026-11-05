# Production CI/CD Integration Runbook

Step-by-step instructions for embedding `env-validator-cli` into production deployment pipelines.

---

## 1. GitHub Actions Pipeline

Add validation gates before container image building or deployment stages:

```yaml
name: Environment Gate
on: [push, pull_request]

jobs:
  validate-env:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Validate Environment Template
        run: |
          python main.py --env .env.example --strict
```

---

## 2. Docker Pre-flight Entrypoint

Validate container environment variables at container boot:

```dockerfile
# entrypoint.sh
#!/bin/sh
set -e
python -m src.validator.cli --strict
exec "$@"
```

---

## 3. Kubernetes Pre-Start Hook

Run validator in Kubernetes initContainers to prevent pod restart loops:

```yaml
initContainers:
  - name: config-validator
    image: python:3.12-alpine
    command: ["python", "main.py", "--env", "/etc/config/.env", "--strict"]
```
