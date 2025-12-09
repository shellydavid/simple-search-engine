from pydantic import BaseModel, Field
from fastapi import Query


class SearchRequest(BaseModel):
    model_config = {"extra": "forbid"}
    query: str = Query(min_length=1)
    offset: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=50)  # set cap on pagination limit to prevent client requesting too much data
