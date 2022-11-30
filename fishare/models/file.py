from datetime import datetime, timedelta
import secrets
from pydantic import HttpUrl, validator
from sqladmin import ModelView

from sqlmodel import Field, SQLModel

from fishare.dependencies import get_settings


settings = get_settings()


class File(SQLModel, table=True, validate=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str | None = None
    filename: str
    url: HttpUrl | None = None
    expires: datetime | None = None
    downloads = 0
    max_downloads = 1
    size: int
    mime_type: str = "application/octet-stream"
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator("mime_type")
    def mime_type_must_contain_slash(cls, v):
        if "/" not in v:
            raise ValueError('must contain "/"')
        else:
            return v.lower()

    @validator("created_at", always=True)
    def set_created_at_to_now(cls, v):
        return datetime.now()

    @validator("slug", always=True)
    def set_secret_slug(cls, v):
        return secrets.token_urlsafe(settings.slug_length)

    @validator("expires", always=True)
    def set_expiration_for_one_day(cls, v):
        return datetime.now() + timedelta(days=1)

    @validator("filename")
    def filename_cant_be_empty(cls, v):
        if v == "":
            raise ValueError("can't be empty")
        return v


class FileAdmin(ModelView, model=File):
    column_list = [
        File.filename,
        File.slug,
        File.size,
        File.downloads,
        File.max_downloads
    ]
