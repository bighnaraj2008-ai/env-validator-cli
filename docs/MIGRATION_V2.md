# Version Migration Guide — Schema Updates

Instructions for migrating configuration schemas from early prototypes (v0.1) to modern declarative contracts (v1.0).

---

## 1. Schema Key Renames

| Legacy Attribute | Modern Schema Attribute | Description |
|---|---|---|
| `schema_name` | `name` | Top-level schema identifier |
| `fields[].type_name` | `fields[].type` | Target casting type |
| `fields[].regex` | `fields[].pattern` | Regular expression match pattern |

---

## 2. Programmatic Migration

Run the automatic schema upgrade helper if converting legacy schemas:
```bash
python -m src.validator.schema --upgrade legacy_schema.yaml
```
