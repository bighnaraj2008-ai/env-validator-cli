"""Schema template for this project's own environment variables.

Each :class:`~src.config.settings.EnvFieldSchema` entry declares:

* ``name``        — environment variable name
* ``required``    — whether the variable must exist in ``.env``
* ``type``        — strict type cast (string, integer, number, boolean)
* ``pattern``     — optional regex the value must satisfy
* ``min_length``  — minimum length (useful for secrets/tokens)
* ``description`` — human readable purpose of the variable

Edit this file when adding, removing, or renaming configuration keys. It is
the single source of truth for what ``env-validator-cli`` expects.
"""

from __future__ import annotations

from src.config.settings import EnvFieldSchema, EnvType
from src.validator.schema import Schema


ENV_SCHEMA = Schema(
    name="env-validator-cli",
    fields=[
        EnvFieldSchema(
            name="APP_NAME",
            required=True,
            type=EnvType.STRING,
            description="Application identifier displayed in logs and health checks.",
        ),
        EnvFieldSchema(
            name="APP_ENV",
            required=True,
            type=EnvType.STRING,
            pattern=r"^(development|staging|production)$",
            description="Deployment environment tier.",
        ),
        EnvFieldSchema(
            name="PORT",
            required=True,
            type=EnvType.INTEGER,
            description="TCP port the application listens on.",
        ),
        EnvFieldSchema(
            name="DEBUG",
            required=True,
            type=EnvType.BOOLEAN,
            description="Enable verbose debug output (true/false).",
        ),
        EnvFieldSchema(
            name="SECRET_KEY",
            required=True,
            type=EnvType.STRING,
            min_length=8,
            description="Cryptographic secret used for signing (never commit real values).",
        ),
        EnvFieldSchema(
            name="JWT_SECRET",
            required=True,
            type=EnvType.STRING,
            min_length=8,
            description="Secret used to sign JSON Web Tokens.",
        ),
        EnvFieldSchema(
            name="DATABASE_URL",
            required=True,
            type=EnvType.STRING,
            pattern=r"^(postgres|postgresql)://.+",
            description="SQLAlchemy-compatible database connection URL.",
        ),
        EnvFieldSchema(
            name="REDIS_URL",
            required=True,
            type=EnvType.STRING,
            pattern=r"^redis://.+",
            description="Redis connection URL.",
        ),
        EnvFieldSchema(
            name="API_KEY",
            required=True,
            type=EnvType.STRING,
            description="Third-party service API key.",
        ),
        EnvFieldSchema(
            name="SENTRY_DSN",
            required=False,
            type=EnvType.STRING,
            pattern=r"^https://.+",
            description="Optional Sentry error-tracking DSN.",
        ),
    ],
)


class SchemaCatalog:
    """Registry of named schema templates.

    Usage::

        from schemas.env_schema import SchemaCatalog
        schema = SchemaCatalog.get("default")
    """

    _templates = {
        "default": ENV_SCHEMA,
    }

    @classmethod
    def get(cls, name: str = "default") -> Schema:
        try:
            return cls._templates[name]
        except KeyError as exc:
            available = ", ".join(sorted(cls._templates))
            raise KeyError(
                f"Schema template '{name}' not found. Available: {available}"
            ) from exc

    @classmethod
    def names(cls) -> list[str]:
        return sorted(cls._templates)
