from nltk.stem import PorterStemmer
from collections import defaultdict
from unidecode import unidecode
import string


def normalize(s: str) -> str:
    '''
    Normalize a string for inverted indexing
        1. Make lowercase
        2. Remove punctuation
        3. Remove diacritics (ex: résumé -> resume)
        4. Stemming
    '''
    s = s.lower()
    s = s.translate(str.maketrans('', '', f"—’{string.punctuation}"))
    s = unidecode(s)
    ps = PorterStemmer()
    s = " ".join([ps.stem(w) for w in s.split()])
    return s

def create_inverted_index(corpus: list[dict]) -> dict[str, set[int]]:
    '''
    Create an inverted index from a corpus, which stores the 
    array position of document/s where a normalized token appears
    '''
    index = defaultdict(set)  # Using a set to prevent duplicates when a token appears multiple times in a document 
    for i in range(len(corpus)):
        document = corpus[i]
        tokens = [token for token in normalize(document['message']).split()]
        for token in tokens:
            index[token].add(i)
    return index
