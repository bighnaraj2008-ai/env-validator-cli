# Edge Case Handling Guidelines & Failure Recovery Playbooks

This document outlines how `env-validator-cli` resolves ambiguous, non-standard,
and malformed `.env` patterns, along with recovery playbooks for production systems.

---

## 1. Syntax Ambiguities

### Unquoted Equals Signs in Values
In many service configurations (e.g., connection strings or base64 tokens), the value itself
contains one or more `=` characters:
```env
CONNECTION_STRING=Server=myServerAddress;Database=myDataBase;Uid=myUsername;Pwd=myPassword;
```
**Resolution**: The parser splits only on the first unquoted `=` delimiter. Everything to the right
is treated as the literal variable value.

### Quoting Rules
- Single quotes (`'value'`) preserve literal characters without escape expansion.
- Double quotes (`"value"`) preserve whitespace and allow embedded quotation marks.
- Surrounding quotes are stripped during tokenization while inner quotes remain intact.

### Duplicate Environment Keys
If a key is declared multiple times:
```env
PORT=3000
PORT=8080
```
**Resolution**: The parser follows standard POSIX dictionary semantics—the last occurrence wins.
Strict linting modes issue a warning to flag configuration ambiguity.

---

## 2. Failure Recovery Playbooks

### Playbook 1: Missing Required Variable
- **Symptom**: CLI exits with code 1; output flags `[missing] KEY_NAME`.
- **Action**: Inspect `schemas/env_schema.yaml` for field description and default value. Add the key to `.env` or pass via environment before starting the service.

### Playbook 2: Type Mismatch (Integer / Boolean)
- **Symptom**: `PORT=not-a-number` or `DEBUG=maybe`.
- **Action**: Check valid boolean literals (`true`, `false`, `1`, `0`, `yes`, `no`) or ensure numeric fields contain digits only without units.

### Playbook 3: Secret Length Violation
- **Symptom**: `[too_short] SECRET_KEY length 5 < min_length 8`.
- **Action**: Generate a cryptographically strong secret exceeding the minimum length specified by the schema.
