from functools import lru_cache

from fishare.models.settings import Settings


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.environment}.")
    return settings
