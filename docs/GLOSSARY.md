# Configuration Management & Environment Glossary

- **12-Factor App**: Architectural methodology recommending strict separation of config from code.
- **Configuration Drift**: Divergence between declared environment schemas and actual deployed variables.
- **Declarative Schema**: Structured YAML or Python contract describing expected types, patterns, and boundaries.
- **Strict Mode**: Validation mode that rejects undeclared extra environment keys to maintain hygiene.
- **POSIX Dict Semantics**: Standard dictionary resolution where trailing key declarations override earlier occurrences.
- **Type Coercion**: Converting raw string environment tokens into typed representations (integer, boolean, float).
