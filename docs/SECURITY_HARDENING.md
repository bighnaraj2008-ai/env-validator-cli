# Secret Management and Environment Security Guide

Guidelines for preventing secret leakage, managing credentials, and maintaining configuration hygiene.

---

## 1. Core Security Principles

1. **Never Commit Real `.env` Files**: Only commit tracked template files such as `.env.example`.
2. **Minimal Privileges**: Microservices should only receive the environment variables they explicitly require.
3. **Secret Rotation Readiness**: Store secret names, never hardcode values in application source code.

---

## 2. Repository Hygiene Protocols

- Keep `.gitignore` strictly enforced:
  ```gitignore
  .env
  .env.*
  !.env.example
  ```
- Use automated pre-commit hooks to block accidental secret staging.
- Enforce minimum entropy and length constraints in `schemas/env_schema.yaml`.
