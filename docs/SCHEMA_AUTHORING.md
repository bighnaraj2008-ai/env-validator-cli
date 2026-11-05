# YAML Schema Authoring Guide

This guide describes how to author declarative YAML schemas for `env-validator-cli`
to validate environment variables across development, staging, and production environments.

---

## 1. Schema Structure Overview

A validation schema is a YAML mapping containing top-level metadata and a `fields` list:

```yaml
name: my-service-env
description: Environment specification for MyService backend
fields:
  - name: APP_NAME
    required: true
    type: string
    description: Identifier displayed in application telemetry
```

---

## 2. Type Casting and Constraints

`env-validator-cli` supports strict type coercion and domain validation:

| Type | Accepted Formats | Failure Example |
|---|---|---|
| `string` | Any UTF-8 character sequence | N/A (unless pattern or min_length set) |
| `integer` | Decimal digits, optional leading `-` | `"8080.5"`, `"0x10"`, `"not-a-number"` |
| `boolean` | `true`, `false`, `1`, `0`, `yes`, `no`, `on`, `off` | `"maybe"`, `"2"`, `"enabled"` |
| `number` | Float or integer decimal notation | `"NaN"`, `"3.14.15"` |

### Regex Pattern Matching
Use Python-compatible regular expressions:
```yaml
  - name: DATABASE_URL
    required: true
    type: string
    pattern: "^(postgresql|postgres)://.+"
```

### Length Constraints
Enforce minimal character boundaries for secrets and keys:
```yaml
  - name: SECRET_KEY
    required: true
    type: string
    min_length: 32
```

---

## 3. Complex Schema Examples

### Microservice Production Contract
```yaml
name: orders-api
description: Production environment configuration schema
fields:
  - name: SERVICE_TIER
    required: true
    type: string
    pattern: "^(development|staging|production)$"
  - name: HTTP_PORT
    required: true
    type: integer
  - name: CACHE_TTL_SECONDS
    required: false
    type: integer
    default: "300"
  - name: ENABLE_PROMETHEUS
    required: false
    type: boolean
    default: "true"
  - name: KAFKA_BOOTSTRAP_SERVERS
    required: true
    type: string
    pattern: "^[a-zA-Z0-9.-]+:[0-9]+(,[a-zA-Z0-9.-]+:[0-9]+)*$"
```
