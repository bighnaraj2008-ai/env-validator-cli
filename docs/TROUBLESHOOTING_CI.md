# Troubleshooting Guide - CI/CD Validation Builds

This guide covers common issues encountered in GitHub Actions CI workflows
and how to resolve them locally.

---

## 1. Flake8 Style Violations

**Symptom:** `flake8` reports `F401 imported but unused` or `E501 line too long`.

**Resolution:**
```bash
flake8 main.py src schemas tests scripts
```
Remove unused imports or split lines longer than 120 characters.

---

## 2. Black Formatting Checks

**Symptom:** `black --check` reports that files would be reformatted.

**Resolution:**
```bash
./scripts/format_code.sh
```

---

## 3. Test Failures Across Python Matrix

**Symptom:** Tests pass on Python 3.12 but fail on Python 3.9.

**Resolution:** Ensure `from __future__ import annotations` is included at the top
of modules using PEP 585/604 type unions. Run tests across matrix locally:
```bash
pytest tests/ -v
```

---

## 4. Documentation Link Failures

**Symptom:** `docs_check.yml` fails on broken markdown links.

**Resolution:**
```bash
python scripts/validate_docs.py
```
Fix any missing files or broken relative links.
