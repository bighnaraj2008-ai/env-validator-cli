# Performance Tuning & Parser Optimization Guide

Optimizations and best practices for scaling `env-validator-cli` to handle massive environments.

---

## 1. Fast Path Tokenization

`src.validator.parser` bypasses regular expressions for normal `KEY=value` lines, using Python's
fast C-implemented `str.partition("=")` and `str.strip()`.

---

## 2. In-Memory Schema Caching

When embedding `Schema` into long-lived web services or CLI watchers:
```python
from schemas.loader import load_yaml_schema

# Load and compile once at startup
SCHEMA = load_yaml_schema("schemas/env_schema.yaml")

def validate_request(env_data: dict):
    return SCHEMA.validate(env_data)
```
