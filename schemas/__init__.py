"""Environment variable schema templates.

This package contains schema definitions describing the expected contract of
environment variables. Import :data:`ENV_SCHEMA` from :mod:`schemas.env_schema`
to validate a project's own ``.env`` file.
"""

from .env_schema import ENV_SCHEMA, SchemaCatalog

__all__ = ["ENV_SCHEMA", "SchemaCatalog"]
