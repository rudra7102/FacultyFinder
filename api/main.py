from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from embeddings.semantic_search import search_faculty


app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
def search(query: str):

    results = search_faculty(query)

    return {
        "results": results
    }