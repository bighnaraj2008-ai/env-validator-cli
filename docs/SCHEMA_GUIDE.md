# Schema Authoring Guide — Strict Environment Contracts

`env-validator-cli` validates `.env` configurations using declarative field
contracts defined in Python (`schemas/env_schema.py`) or YAML (`schemas/env_schema.yaml`).

---

## 1. Field Schema Attributes

| Attribute | Type | Required | Description |
|:----------|:-----|:--------:|:------------|
| `name` | `string` | yes | Environment variable name (e.g. `DATABASE_URL`) |
| `required` | `bool` | no | Defaults to `true`. Optional variables emit warnings when unset |
| `type` | `string` | no | `string`, `integer`, `number`, or `boolean` |
| `pattern` | `regex` | no | Regular expression constraint evaluated via `re.search` |
| `min_length` | `int` | no | Minimum string character length (ideal for signing keys) |
| `description` | `string` | no | Human-readable purpose displayed in generated templates |

---

## 2. Example Declarative YAML Contract

```yaml
schema_name: service-env
version: "1.0"

fields:
  - name: PORT
    required: true
    type: integer
    description: Service HTTP listen port.

  - name: APP_ENV
    required: true
    type: string
    pattern: "^(development|staging|production)$"
```

Load any custom YAML schema programmatically with [`schemas/loader.py`](../schemas/loader.py):

```python
from schemas.loader import load_yaml_schema

schema = load_yaml_schema("schemas/env_schema.yaml")
```
