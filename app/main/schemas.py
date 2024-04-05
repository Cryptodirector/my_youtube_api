from typing import Annotated

from pydantic import BaseModel
from fastapi import Query


class AddVideoSchemas(BaseModel):
    title: str
    descriptions: Annotated[str, Query(max_length=1000)]
    link: str


class UpdateVideoSchemas(BaseModel):
    id: int
    title: str | None = None
    description: str | None = None


class AddCommentSchemas(BaseModel):
    text: Annotated[str, Query(max_length=1000)]

