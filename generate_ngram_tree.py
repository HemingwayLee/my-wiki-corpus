import MeCab
import os
import wget
import json
from utils import process_wiki_data

MECAB = MeCab.Tagger("-Owakati")

def generate_ngram_callback(title, text, depth=3, tokenization=True):
    print(title)
    
    if tokenization:
        tokens = MECAB.parse(text).split(" ")
        print(tokens)
    else:
        print(text)

if __name__ == '__main__':
    INPUT_FILENAME = "jawiki-latest-pages-articles.xml.bz2"
    JA_WIKI_LATEST_URL = "https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2"
    OUTPUT_FILENAME = "2gram.json"
    ARTICLE_COUNT = 10
    
    if not os.path.isfile(INPUT_FILENAME):
        wget.download(JA_WIKI_LATEST_URL)

    process_wiki_data(INPUT_FILENAME, ARTICLE_COUNT, generate_ngram_callback)

