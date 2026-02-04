from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "production"
    app_base_url: str = "http://localhost:8080"
    app_port: int = 8080
    jwt_issuer: str = "machwork"
    jwt_audience: str = "machwork-api"
    jwt_access_ttl_minutes: int = 15
    jwt_refresh_ttl_days: int = 30
    jwt_private_key_path: str = "/secrets/jwt_private.pem"
    jwt_public_key_path: str = "/secrets/jwt_public.pem"
    password_hasher: str = "argon2id"
    mfa_issuer: str = "MachWork"
    database_url: str
    smtp_host: str
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    smtp_from: str
    log_level: str = "info"
    rate_limit_window_seconds: int = 60
    rate_limit_max_requests: int = 100
    auth_rate_limit_max_requests: int = 20

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
