# Guidelines for Contributing Custom Validation Rules

We welcome community contributions to `env-validator-cli`!

---

## 1. Developing New Validation Rules

All validation rules inherit from `src.validator.rules.Rule`:

```python
from src.validator.rules import Rule, ValidationResult
from src.config.settings import EnvFieldSchema

class MaxLengthRule(Rule):
    def check(self, key: str, value: str | None, schema: EnvFieldSchema) -> ValidationResult:
        if value and len(value) > schema.max_length:
            return ValidationResult(
                passed=False,
                code="too_long",
                message=f"Key '{key}' exceeds max length {schema.max_length}",
            )
        return ValidationResult(passed=True)
```

---

## 2. Testing Your Rule

1. Add unit test suite in `tests/edge_cases/`.
2. Verify zero flake8 warnings: `flake8 main.py src schemas tests scripts`.
3. Run test runner: `python scripts/run_unit_tests.py`.
