import sys
import numpy as np
from numpy.linalg import norm
from graphtovector import GraphtoVector

def cosine_similarity(a, b):
    """Returns cosine similarity of two numpy vectors."""
    return np.dot(a, b) / (norm(a) * norm(b))

def vectorize(graph_files):
    """Converts provenance graph files into numpy vectors.

    Generates a list of vectors from a set of files by reducing the
    graphs based on edge frequency counts.

    Args:
        graph_files: A list of json files describing provenance graphs.

    Returns:
        A list of numpy arrays containing a vector representation of
        provenance graphs.

    Raises:
        N/A
    """
    return GraphtoVector(graph_files).genVectorSet()

def calculate_similarity(train_set, test_set):
    """Generates similarity scores from two lists of provenance graph files.

    Calculates the cosine similarity for each file in the test_set
    compared against every file in train_set.

    Args:
        train_set: A list of json files describing provenance graphs.
        test_set: A list of json files describing provenance graphs.

    Returns:
        A list-of-lists containing the similarity scores using the same
        indices as test_set.

    Raises:
        N/A
    """
    scores = []

    vectors = vectorize(train_set + test_set)
    train_count = len(train_set)
    test_count = len(test_set)
    train_vec = vectors[0:train_count]
    test_vec = vectors[train_count:train_count+test_count]

    for test in test_vec:
        test_scores = []
        for train in train_vec:
            cs = cosine_similarity(np.array(train), np.array(test))
            test_scores.append(cs)
        scores.append(test_scores)
    return scores

