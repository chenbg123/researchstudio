import os

from pydantic import BaseModel, Field


class GatewayConfig(BaseModel):
    """Configuration for the API Gateway."""

    host: str = Field(default="0.0.0.0", description="Host to bind the gateway server")
    port: int = Field(default=8001, description="Port to bind the gateway server")
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"], description="Allowed CORS origins")
    database_url: str = Field(default="postgresql+psycopg://postgres:postgres@localhost:5432/diresearchstudio", description="Application database URL")
    trusted_header_auth_enabled: bool = Field(default=False, description="Enable trusted-header SSO")
    trusted_header_user_id: str = Field(default="X-User-Id", description="Header name for user ID")
    trusted_header_display_name: str = Field(default="X-User-Name", description="Header name for display name")
    trusted_header_email: str = Field(default="X-User-Email", description="Header name for user email")


_gateway_config: GatewayConfig | None = None


def _load_gateway_section() -> dict:
    """Load the gateway section from config.yaml if available."""
    try:
        from deerflow.config.app_config import AppConfig

        config_path = AppConfig.resolve_config_path()
        if config_path and config_path.is_file():
            import yaml

            with open(config_path) as f:
                data = yaml.safe_load(f) or {}
            return data.get("gateway", {}) or {}
    except Exception:
        pass
    return {}


def get_gateway_config() -> GatewayConfig:
    """Get gateway config, loading from config.yaml and environment overrides."""
    global _gateway_config
    if _gateway_config is None:
        # Read defaults from config.yaml gateway section
        yaml_section = _load_gateway_section()

        # CORS origins: env var (comma-separated) > config.yaml list > default
        cors_origins_env = os.getenv("CORS_ORIGINS")
        if cors_origins_env:
            cors_origins = cors_origins_env.split(",")
        elif "cors_origins" in yaml_section and isinstance(yaml_section["cors_origins"], list):
            cors_origins = yaml_section["cors_origins"]
        else:
            cors_origins = ["http://localhost:3000"]

        _gateway_config = GatewayConfig(
            host=os.getenv("GATEWAY_HOST", "0.0.0.0"),
            port=int(os.getenv("GATEWAY_PORT", "8001")),
            cors_origins=cors_origins,
            database_url=os.getenv("DATABASE_URL", yaml_section.get("database_url", "postgresql+psycopg://postgres:postgres@localhost:5432/diresearchstudio")),
            trusted_header_auth_enabled=os.getenv("TRUSTED_HEADER_AUTH_ENABLED", str(yaml_section.get("trusted_header_auth_enabled", "false"))).lower() == "true",
            trusted_header_user_id=os.getenv("TRUSTED_HEADER_USER_ID", yaml_section.get("trusted_header_user_id", "X-User-Id")),
            trusted_header_display_name=os.getenv("TRUSTED_HEADER_DISPLAY_NAME", yaml_section.get("trusted_header_display_name", "X-User-Name")),
            trusted_header_email=os.getenv("TRUSTED_HEADER_EMAIL", yaml_section.get("trusted_header_email", "X-User-Email")),
        )
    return _gateway_config
