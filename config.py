from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    symbol: str
    binance_rest_url: str
    binance_ws_base_url: str
    binance_depth_limit: int = 100


settings = Settings()
