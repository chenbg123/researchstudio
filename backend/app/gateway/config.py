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


def get_gateway_config() -> GatewayConfig:
    """Get gateway config, loading from environment if available."""
    global _gateway_config
    if _gateway_config is None:
        cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
        _gateway_config = GatewayConfig(
            host=os.getenv("GATEWAY_HOST", "0.0.0.0"),
            port=int(os.getenv("GATEWAY_PORT", "8001")),
            cors_origins=cors_origins_str.split(","),
            database_url=os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/diresearchstudio"),
            trusted_header_auth_enabled=os.getenv("TRUSTED_HEADER_AUTH_ENABLED", "false").lower() == "true",
            trusted_header_user_id=os.getenv("TRUSTED_HEADER_USER_ID", "X-User-Id"),
            trusted_header_display_name=os.getenv("TRUSTED_HEADER_DISPLAY_NAME", "X-User-Name"),
            trusted_header_email=os.getenv("TRUSTED_HEADER_EMAIL", "X-User-Email"),
        )
    return _gateway_config
