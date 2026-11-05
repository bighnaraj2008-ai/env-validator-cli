# API Reference Guide — Core Parser & Schema Engine

Technical documentation for developers extending or embedding `env-validator-cli`.

---

## 1. Parser Engine (`src.validator.parser`)

### `parse_env_file(path: Union[str, Path]) -> ParsedEnv`
Reads an environment file from disk, strips comments, trailing whitespace,
and quotes, and returns structured `ParsedEnv`.

- **Parameters**: `path` — Path to `.env` file.
- **Returns**: `ParsedEnv` named tuple containing `values` (dict), `source` (str), and `line_count` (int).
- **Raises**: `EnvFileNotFoundError` if file missing; `EnvParseError` if line malformed.

### `parse_env_text(text: str, source: str = "<memory>") -> ParsedEnv`
Parses an in-memory string of environment variables.

---

## 2. Schema Engine (`src.validator.schema`)

### `Schema(fields: List[EnvFieldSchema], name: str = "default")`
Represents an environment contract against which variable dictionaries are validated.

#### Methods:
- `validate(values: Mapping[str, str], config: ValidationConfig) -> ValidationReport`
  Runs configured rules across declared fields and reports status.

---

## 3. Validation Rules (`src.validator.rules`)

### `RequiredRule`
Flags declared keys whose values are missing or empty string.

### `TypeCastRule`
Ensures string values can be cast to `integer`, `boolean`, or `number`.

### `PatternRule`
Validates values against regex patterns declared in the schema.

### `MinLengthRule`
Verifies character string length meets or exceeds minimum boundaries.
