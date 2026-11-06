# Security Reporting & Vulnerability Disclosure Policy

We take the security of `env-validator-cli` and applications configuring secrets
seriously.

---

## 1. Supported Versions

| Version | Supported | Security Updates |
|:--------|:---------:|:----------------:|
| `1.x` | Yes | Automated scans + patches |
| `< 1.0.0` | No | Upgrade to latest release |

---

## 2. Automated Security Controls

Our CI pipeline continuously enforces:
- **Bandit Static Analysis**: Scans Python modules under `src/` and `scripts/`
  via [`.github/workflows/security_scan.yml`](../.github/workflows/security_scan.yml).
- **GitHub CodeQL**: Semantic data-flow vulnerability scanning via
  [`.github/workflows/code_ql.yml`](../.github/workflows/code_ql.yml).
- **Secret Prevention**: Regex scanning and strict `.gitignore` enforcement
  preventing accidental `.env` or token commits.

---

## 3. Reporting a Vulnerability

If you discover a security vulnerability, please do not open a public issue.
Instead review [`SECURITY.md`](../SECURITY.md) for private disclosure instructions.
