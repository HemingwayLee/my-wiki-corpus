#!/usr/bin/env python3
# coding: utf-8

import logging
import os
import time
from multiprocessing import cpu_count
import wget
import json

from mywiki import MyWikiCorpus

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def process_wiki_to_ngram(input_filename, output_ngram_filename, depth):
    start = time.time()
    intermediary_time = None
    count = 0

    wiki = MyWikiCorpus(input_filename, lemmatize=False, dictionary={}, processes=cpu_count())
    wiki.metadata = True
    texts = wiki.get_texts()

    for i, article in enumerate(texts):
        if i > 10:
            break
        
        title = article[1]
        text = article[0]  
        count += len(text)

        print(title)
        print(text)

        # This is just for the logging
        if i % (100 - 1) == 0 and i != 0:
            if intermediary_time is None:
                intermediary_time = time.time()
            else:
                new_time = time.time()
                intermediary_time = new_time
            
            logging.info(f'Saved {i+1} articles containing {count} text.')
                


    # with open(output_ngram_filename, 'w') as out:
    #     logging.info(
    #         'Finished process_wiki_to_text(). It took {0:.2f} s to execute.'.format(round(time.time() - start, 2)))


if __name__ == '__main__':
    INPUT_FILENAME = "jawiki-latest-pages-articles.xml.bz2"
    JA_WIKI_LATEST_URL = "https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2"
    OUTPUT_FILENAME = "2gram.json"
    
    if not os.path.isfile(INPUT_FILENAME):
        wget.download(JA_WIKI_LATEST_URL)

    process_wiki_to_ngram(INPUT_FILENAME, OUTPUT_FILENAME, 3)
