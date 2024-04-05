
from typing import Annotated
from fastapi import Query

from pydantic import BaseModel


class UserSchemas(BaseModel):
    name: Annotated[str, Query(max_length=15, min_length=4)]
    password: Annotated[str, Query(min_length=4, max_length=15)]
