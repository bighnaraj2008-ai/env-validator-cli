# ⚙️ env-validator-cli

> **Industry-grade, zero-dependency CLI tool to validate, compare, and synchronize `.env` configurations against `.env.example` templates.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)](#)

---

## 📌 Overview

In modern cloud-native and 12-factor application architectures, environment variables drive configuration across environments (Local, Staging, Production). However, a frequent source of deployment failures, unexpected downtime, and onboarding friction is **configuration drift**—where required environment variables declared in template files (`.env.example`) are missing in local configurations or CI/CD pipelines.

`env-validator-cli` provides a lightweight, automated check to ensure that every necessary configuration key is present and flags any stale or undocumented keys before runtime.

---

## 💼 Industry Value & DevOps Impact

1. **Prevents Silent Runtime Crashes:**
   Catch missing API keys, database URLs, and secret tokens before your web framework or backend microservice attempts to boot and fails in production or CI.

2. **Standardizes Team Onboarding:**
   New engineers can run a single command after cloning a repository to verify that their local `.env` has all necessary variables matching the authoritative `.env.example`.

3. **Guards Against Configuration Drift:**
   Identifies orphan or deprecated configuration keys that are no longer used or documented by the team.

4. **Zero-Dependency Architecture:**
   Built completely with Python standard library utilities (`pathlib`, `os`). It requires no external package installations (`pip install`), making it fast and universally portable across Docker containers, Linux, macOS, and Windows.

5. **CI/CD & Pre-Commit Ready:**
   Easily drop into pre-commit hooks, GitHub Actions, or deployment pipelines to enforce environment hygiene prior to testing and containerization.

---

## 📁 Project Structure

```text
env-validator-cli/
├── .env.example       # Authoritative template defining expected environment keys
├── .env               # Local environment configuration (ignored by git)
├── .gitignore          # Ignores venv/, __pycache__/, and local .env
├── main.py            # Core CLI validator engine
└── README.md          # Project documentation and usage guide
```

---

## 🚀 Quick Start & Usage

### Prerequisites
- Python 3.8 or higher installed on your machine.

### Installation

Clone the repository:

```bash
git clone https://github.com/bighnaraj2008-ai/env-validator-cli.git
cd env-validator-cli
```

*(Optional) Create and activate a virtual environment:*

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

### Running the Validator

Run the script directly using Python:

```bash
python main.py
```

---

## 🖥️ Example Scenarios & Output

### 1. Fully Synchronized (Success)
When all variables defined in `.env.example` are present in your local `.env`:

```text
🔍 Scanning environment configuration...

✅ Environment configuration is fully synchronized and valid!
```

### 2. Missing Environment Keys (Error)
If a critical key such as `DATABASE_URL` or `JWT_SECRET` is missing in `.env`:

```text
🔍 Scanning environment configuration...

❌ Missing keys in your local .env: ['DATABASE_URL', 'JWT_SECRET']
```

### 3. Extra Undocumented Keys (Warning)
If your local `.env` has keys not listed in `.env.example`:

```text
🔍 Scanning environment configuration...

⚠️ Extra keys in your local .env not found in example: ['DEBUG_DEV_OVERRIDE']
```

---

## 🔄 CI/CD Pipeline Integration

You can integrate `env-validator-cli` into your GitHub Actions workflow:

```yaml
name: Validate Environment Configuration

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  validate-env:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Validate .env template
        run: |
          python main.py
```

---

## 🛡️ Security Best Practices

- **Never commit `.env` files** containing production secrets or credentials to source control.
- Ensure `.gitignore` always includes `.env`.
- Use `.env.example` exclusively for dummy values, mock placeholders, or structural templates.

---

## 📄 License

This project is licensed under the MIT License.
