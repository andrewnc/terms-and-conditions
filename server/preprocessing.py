from __future__ import print_function
from threading import Thread
import numpy as np
import string
import sys


if sys.version_info >= (3, 0):
    from queue import Queue, Empty
else:
    from Queue import Queue, Empty


def _python2_clean_sentences(pure_sentences):
    clean_sentences = []
    for x in pure_sentences:
        clean_sentences.append(' '.join(x.lower().translate(None, string.punctuation).split()))
    return clean_sentences


def _python3_clean_sentences(pure_sentences):
    clean_sentences = []
    translator=str.maketrans('','',string.punctuation)
    for x in pure_sentences:
        clean_sentences.append(' '.join(x.lower().translate(translator).split()))
    return clean_sentences


def prepare_for_regex(input_str, delimiter="."):
    pure_sentences = input_str.strip().split(delimiter)
    if pure_sentences[-1] == "":
        pure_sentences.pop()

    # Remove leading/trailing whitespace and end with period.
    for i, x in enumerate(pure_sentences):
        pure_sentences[i] = x.strip() + "."

    if sys.version_info >= (3, 0):
        clean_sentences = _python3_clean_sentences(pure_sentences)
    else:
        clean_sentences = _python2_clean_sentences(pure_sentences)

    return clean_sentences, pure_sentences


def bow(input_str, vocab, delimiter="\n", num_threads=1):
    # NOT FINISHED
    """Converts text into a bag of words

    parameters:
        input_str : and input string (str)
        vocab : the vocabulary (dict{str:ing} including UNK token)
        delimiter : the delimiter for different entries (str)
        num_threads : how many threads should be run to do this (int)
    """
    lines = input_str.split(delimiter)
    num_lines = len(lines)
    vocab_size = len(vocab)
    result = np.zeros([num_lines, vocab_size], dtype=np.uint32)

    threads = []
    q = Queue()
    for i, x in enumerate(lines):
        q.put((x, i))

    for i in range(num_threads):
        threads.append(Thread(target=__prepare_bow__, args=[q, vocab, result]))
        threads[-1].start()

    for i in range(num_threads):
        threads[i].join()


def __prepare_bow__(q, vocab, result_matrix):
    while not q.empty():
        try:
            data, i = q.get(block=False)
            # process data here
            print(data, i)
            # result_matrix[i, :] = result
        except Empty:
            return
