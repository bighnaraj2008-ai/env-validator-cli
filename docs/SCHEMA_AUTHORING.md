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

### Top-Level Metadata Attributes
- `name`: Human-readable identifier for the schema.
- `description`: Purpose and scope of the configuration contract.
- `version`: (Optional) Contract version string (e.g., `"1.0"`).
- `fields`: Sequence of variable specifications evaluated in declaration order.
