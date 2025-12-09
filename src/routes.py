from src.search_service import SearchService
from src.utils import create_inverted_index
from src.models import SearchRequest
from fastapi import APIRouter, Query
from typing import Annotated
import json


# Load corpus and create inverted index 
with open('src/corpus.json', 'r') as f:
    data = json.load(f)
index = create_inverted_index(data)

# ----------------------------

search_service = SearchService(data, index)

router = APIRouter()
@router.get("/search", tags=["search"])
async def search(request: Annotated[SearchRequest, Query()]):
    return search_service.search(request.query, request.offset, request.limit)
