from pydantic import (
    PostgresDsn
)

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_dsn: PostgresDsn = 'postgresql://postgres:root@127.0.0.1:5432/to_do_list'


settings = Settings()
