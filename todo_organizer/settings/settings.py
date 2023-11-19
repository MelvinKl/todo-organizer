from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_connection_string: str = Field('postgres://user:pass@localhost:5432/foobar')
