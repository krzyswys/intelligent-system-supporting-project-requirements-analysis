from pydantic import BaseModel, Field
from typing import List


class Mockups(BaseModel):
    urls: List[str] = Field(default_factory=list)

    class Config:
        extra = "forbid"
