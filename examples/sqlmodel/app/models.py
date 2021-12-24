from datetime import datetime
from enum import Enum

from sqlmodel import Field

from fastack_sqlmodel import models


class Book(models.Model, table=True):
    class Status(str, Enum):
        DRAFT = "draft"
        PUBLISH = "publish"

    title: str = Field(max_length=255, nullable=False)
    status: Status = Field(max_length=7, nullable=False)
    published_date: datetime = Field(default=None, nullable=True)

    def serialize(self) -> dict:
        data = super().serialize()
        data["title"] = self.title
        data["status"] = self.status
        data["published_date"] = self.published_date
        return data
