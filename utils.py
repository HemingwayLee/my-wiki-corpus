#!/usr/bin/env python3
# coding: utf-8

import logging
import time
from multiprocessing import cpu_count

from mywiki import MyWikiCorpus

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def process_wiki_data(input_filename, article_count, callback):
    start = time.time()
    intermediary_time = None
    count = 0

    wiki = MyWikiCorpus(input_filename, lemmatize=False, dictionary={}, processes=cpu_count())
    wiki.metadata = True
    texts = wiki.get_texts()

    for i, article in enumerate(texts):
        if i > article_count:
            break
        
        title = article[1]
        text = article[0]  
        count += len(text)

        callback(title, text)

        # logging
        if i % (100 - 1) == 0 and i != 0:
            if intermediary_time is None:
                intermediary_time = time.time()
            else:
                new_time = time.time()
                intermediary_time = new_time
            
            logging.info(f'Saved {i+1} articles containing {count} text.')

    logging.info('Finished process_wiki_data(). It took {0:.2f} s to execute.'.format(round(time.time() - start, 2)))

