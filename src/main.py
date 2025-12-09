from src.routes import router
from fastapi import FastAPI


app = FastAPI(
    title='Simple Search Engine', 
    summary='simple search engine on a dummy data corpus courtesy of fakery.dev'
)
app.include_router(router)
