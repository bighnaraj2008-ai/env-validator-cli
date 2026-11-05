# Environment Configuration Diagnostic Playbook

Playbook for troubleshooting common `.env` syntax anomalies and validation failures.

---

## 1. Quick Diagnostic Checklist

- [ ] File exists and has read permissions.
- [ ] File encoding is UTF-8 without Byte Order Mark (BOM).
- [ ] No spaces around the assignment operator (`KEY=value`, not `KEY = value`).
- [ ] Quotation marks are balanced (single or double quotes).
- [ ] Multiline values are wrapped in quotes.

---

## 2. Common Errors and Resolutions

### Error: `EnvParseError: line X missing equals sign`
- **Cause**: Unquoted line or multiline string broken across physical lines.
- **Fix**: Wrap multiline values in double quotes or add missing `=` delimiter.

### Error: `[type_mismatch] PORT expected integer, got '8080/tcp'`
- **Cause**: Protocol or port identifier included with numeric value.
- **Fix**: Strip non-digit characters (`PORT=8080`).

### Error: `[missing] SECRET_KEY is required`
- **Cause**: Key omitted or value is an empty string.
- **Fix**: Supply key in `.env` file or export into process environment.
