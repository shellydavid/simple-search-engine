from fastapi import HTTPException, status
from rank_bm25 import BM25Okapi
from src.utils import *
import math



class SearchService:
    
    def __init__(self, data, inverted_index):
        self.data = data
        self.index = inverted_index
        
        
    def search(self, query: str, offset: int, limit: int) -> dict:
        '''Main public-facing function to execute the search
            1. Query documents that match provided keywords via inverted index
            2. BM25 rank results
            3. Paginate response
        '''
        matching_docs = self._query_matches(query)
        if not matching_docs:
            return self._empty_response(offset, limit)
        else:
            ranked_results = self._rank_results(query, matching_docs)
            return self._paginate(ranked_results, offset, limit)
    
    
    def _query_matches(self, query: str) -> list[dict]:
        '''Query documents in the inverted index that match the provided keyword/s'''
        
        results = []
        if len(query.split()) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid query')
        elif len(query.split()) == 1:
            # Single keyword query
            keyword = normalize(query)
            for pos in self.index[keyword]:
                results.append(self.data[pos])
        else:
            # Multiple keyword query
            # Get the intersection (logical AND) of the documents for each keyword
            keywords = [keyword for keyword in normalize(query).split()]
            positions = []
            for i in range(len(keywords)-1):
                positions = list(set(self.index[keywords[i]]) & set(self.index[keywords[i+1]]))
            for pos in positions:
                results.append(self.data[pos])
                
        return results
    
    
    def _rank_results(self, query: str, results: list[dict]) -> list[dict]:
        '''Rank results based on BM25 algorithm'''
        
        corpus = [normalize(doc['message']).split() for doc in results]
        bm25 = BM25Okapi(corpus)
        tokenized_query = normalize(query).split()
        scores = bm25.get_scores(tokenized_query)
        
        # For stable pagination, sort results based on score first and UUID second (for tie-breakers)
        # create a list of tuples (score, id) to support the above
        scores = [(float(scores[i]), results[i]['id']) for i in range(len(scores))]
        scores.sort(reverse=True)
        
        data = {d['id']:d for d in results}  # Create a dict of {'id': document} to support O(1) lookup of the full document based on UUID
        ranked_results = []
        for i in range(len(scores)):
            uuid = scores[i][1]
            ranked_results.append(data[uuid])
            
        return ranked_results
    
    
    def _paginate(self, results: list[dict], offset: int, limit: int) -> dict:
        '''Paginate results + include metadata for client to navigate across pages'''
        
        total_items = len(results)
        current_page = math.floor(offset / limit) + 1
        total_pages = math.ceil(total_items / limit)
        
        return {
            'items': results[offset: offset+limit],
            'pagination': {
                'offset': offset,
                'limit': limit,
                'total_items': total_items,
                'total_pages': total_pages,
                'current_page': current_page
            },
            'links': {
                'self': f'/search?offset={offset}&limit={limit}',
                'first': f'/search?offset=0&limit={limit}',
                'prev': None if current_page == 1 else f'/search?offset={offset-limit}&limit={limit}',
                'next': None if current_page == total_pages or offset >= total_items else f'/search?offset={offset+limit}&limit={limit}',
                'last': f'/search?offset={total_items-(total_items%limit)}&limit={limit}'  # total_items - (num_items on last page)
            }
        }
    

    def _empty_response(self, offset: int, limit: int) -> dict:
        '''Default response to return if no query results found'''
        
        return {
            'items': [],
            'pagination': {
                'offset': offset,
                'limit': limit,
                'total_items': 0,
                'total_pages': 0,
                'current_page': 1
            },
            'links': {
                "self": f'/search?offset={offset}&limit={limit}',
                "first": f'/search?offset=0&limit={limit}',
                "prev": None,
                "next": None,
                "last": f'/search?offset=0&limit={limit}'
            }
        }
