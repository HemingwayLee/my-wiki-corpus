#!/usr/bin/env python3
# coding: utf-8

import logging
import os
import time
from multiprocessing import cpu_count
import wget
import json

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def process_wiki_to_ngram(input_filename, output_text_filename, depth):

    if os.path.isfile(output_text_filename) and os.path.isfile(output_sentences_filename):
        logging.info('Skipping process_wiki_to_text(). Files already exist: {} {}'.format(output_text_filename,
                                                                                          output_sentences_filename))
        return

    start = time.time()
    intermediary_time = None
    sentences_count = 0

    with open(output_text_filename, 'w') as out:
        with open(output_sentences_filename, 'w') as out_sentences:

            # Open the Wiki Dump with gensim
            wiki = WikiCorpus(input_filename, lemmatize=False, dictionary={}, processes=cpu_count())
            wiki.metadata = True
            texts = wiki.get_texts()

            for i, article in enumerate(texts):
                # article[1] refers to the name of the article.
                text_list = article[0]  
                sentences = text_list
                sentences_count += len(sentences)

                # Write sentences per line
                for sentence in sentences:
                    out_sentences.write((sentence + '\n'))

                # Write each page in one line
                text = ' '.join(sentences) + '\n'
                out.write(text)

                # This is just for the logging
                if i % (100 - 1) == 0 and i != 0:
                    if intermediary_time is None:
                        intermediary_time = time.time()
                        elapsed = intermediary_time - start
                    else:
                        new_time = time.time()
                        elapsed = new_time - intermediary_time
                        intermediary_time = new_time
                    sentences_per_sec = int(len(sentences) / elapsed)
                    logging.info('Saved {0} articles containing {1} sentences ({2} sentences/sec).'.format(i + 1,
                                                                                                           sentences_count,
                                                                                                           sentences_per_sec))
        logging.info(
            'Finished process_wiki_to_text(). It took {0:.2f} s to execute.'.format(round(time.time() - start, 2)))


if __name__ == '__main__':
    INPUT_FILENAME = "jawiki-latest-pages-articles.xml.bz2"
    JA_WIKI_LATEST_URL = "https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2"
    OUTPUT_FILENAME = "2gram.json"
    
    if not os.path.isfile(INPUT_FILENAME):
        wget.download(JA_WIKI_LATEST_URL)

    process_wiki_to_ngram(INPUT_FILENAME, OUTPUT_FILENAME, 3)
