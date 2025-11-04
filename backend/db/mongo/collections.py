from datetime import datetime, timezone
from functools import partial
import typing as t

from beanie import (
    Document,
    init_beanie,
    before_event,
    Insert,
    Update,
    SaveChanges,
    Replace,
)
from pydantic import BaseModel, Field
from pymongo import AsyncMongoClient

import schemas as sc
from settings import Settings


class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))
    updated_at: datetime | None = None

    @before_event(Insert)
    def set_created_at(self):
        self.created_at = datetime.now(timezone.utc)

    @before_event(Update, SaveChanges, Replace)
    def set_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)


class Conversation(TimestampMixin, Document):
    query: str
    response: str

    class Settings:
        name = "conversation"
        validate_on_save = True


class ScrapedUrls(Document):
    url: str

    class Settings:
        name = "scraped_urls"
        validate_on_save = True


async def init():
    client = AsyncMongoClient(Settings.MONGODB_CONN)
    await init_beanie(
        database=client.households,
        document_models=[Conversation, ScrapedUrls],
    )
