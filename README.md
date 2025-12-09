# simple search engine

Simple search engine on a dummy data corpus from [fakery.dev ](https://fakery.dev/?fields=string.uuid%2Chacker.phrase&rows=200)

![FastAPI](https://img.shields.io/badge/FastAPI-%23009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)


## Pipeline

> INDEX -> SEARCH -> RANK -> PAGINATE

1. Create inverted index
2. Normalize query
    - *lowercasing*
    - *removing punctuation*
    - *handling diacritics (“résumé” → “resume”)*
    - *[stemming](https://www.geeksforgeeks.org/machine-learning/introduction-to-stemming/)*
3. Search for documents in inverted index that match query keyword/s
4. Rank results
    - *[BM25](https://medium.com/@sany2k8dev/tf-idf-vs-bm25-in-elasticsearch-whats-the-difference-96c126d47394) algorithm*
5. Paginate results



Example: 
```
GET /search?query=program&offset=0&limit=5
```

## Contents
```
src/
│
├── main.py            # FastAPI entrypoint
├── routes.py          # API endpoint definition
├── search_service.py  # Search logic (indexing, ranking, pagination)
├── models.py          # Data models
├── corpus.json        # Dummy dataset
└── utils.py           # Helper functions
```

## Running Locally

via Conda *(or virtual env tool of choice)*:
1. Create the virtual env - `conda env create -f env.yml`
2. Activate the virtual env - `conda activate simple-search-engine`
3. Run the FastAPI app - `uvicorn src.main:app --host 0.0.0.0 --port 8000`
4. Visit `127.0.0.1:8000/docs`

via Docker
1. `docker build -t search-engine .`
2. `docker run -p 8000:8000 --name search-engine search-engine`
3. Visit `127.0.0.1:8000/docs`
4. Run `docker {{start|stop}} search-engine` as needed
