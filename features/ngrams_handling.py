
"""
    Mapping a JS file to either:
    - np.array containing the frequency of the n-grams that the file contains (dico mapping);
    - or a CSR matrix containing the frequency of the n-grams that the file contains (hash mapping).
"""


import os
import pickle
import logging
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import HashingVectorizer

import tokens


CURRENT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
DICO_PATH = os.path.join(CURRENT_PATH, 'ngrams2int')


############################################################
#                        DICO MAPPING
############################################################


# Producing n-grams from syntactical units by moving a fixed-length window to extract subsequence
# of length n.
def n_grams_list(numbers_list, n):
    """
        Given a list of numbers, produce every possible n-gram (n configurable) and store them
        in a matrix.

        -------
        Parameters:
        - numbers_list: List
            Contains integers which represent the syntactic units extracted
            from a JS file (see tokens.py).
        - n: Integer
            Stands for the size of the sliding-window which goes through the units contained
            in the files to be analysed.

        -------
        Returns:
        - Matrix
            Rows: tuples representing every possible n-gram (produced from numbers_list);
            Columns: part of the previous tuples
        - or None if numbers_list is empty.
    """

    if numbers_list is not None:
        len_numbers_list = len(numbers_list)
        if n < 1 or n > len_numbers_list:
            logging.warning('The file has less tokens than the length n of an n-gram')
            # Possible that n > (len(numbers_list)), e.g. the JS file only contains
            # comments: 1 token < n if n > 1.

        else:
            range_n = range(n)
            matrix_all_n_grams = []
            range_list = range(len_numbers_list - (n - 1))
            for j in range_list:  # Loop on all the n-grams
                matrix_all_n_grams.append(tuple(numbers_list[j + i] for i in range_n))
            return matrix_all_n_grams
    return None


# Analysing the number of occurrences (probability) of each n-gram in JavaScript files.
def count_sets_of_n_grams(input_file, tolerance, n):
    """
        Given a matrix containing every possible n-gram (for a JavaScript given file), count
        and store (once) the probability of occurrences of each set of
        n-gram in a dictionary.

        -------
        Parameters:
        - input_file: str
            Path of the file to be analysed.
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option).
            The values 'true' and 'false' shall be used to enable this tolerant mode.
        - n: int
            Stands for the size of the sliding-window which goes through the units contained
            in the files to be analysed.

        -------
        Returns:
        - Dictionary
            Key: tuple representing an n-gram;
            Value: probability of occurrences of a given tuple of n-gram.
        - or None if matrix_all_n_grams is empty.
    """

    numbers_list = tokens.tokens_to_numbers(input_file, tolerance)
    matrix_all_n_grams = n_grams_list(numbers_list, n)
    # Each row: tuple representing an n-gram.

    if matrix_all_n_grams is not None:
        dico_of_n_grams = {}
        # Nb of lines in the matrix, i.e. of sets of n-grams
        for j, _ in enumerate(matrix_all_n_grams):
            if matrix_all_n_grams[j] in dico_of_n_grams:
                dico_of_n_grams[matrix_all_n_grams[j]] += 1
            else:
                dico_of_n_grams[matrix_all_n_grams[j]] = 1

        return [dico_of_n_grams, len(matrix_all_n_grams)]
    return [None, None]


# Simplifying the n-grams list and mapping the resulting n-grams to integers.
def import_modules(n):
    """
        Import the dictionary mapping n-grams and int.

        -------
        Parameter:
        - n: Integer
            Stands for the size of the sliding-window which goes through the units contained
            in the files to be analysed.

        -------
        Returns:
        - Nothing
            But creates a global variable containing the dictionary mapping n-grams to int.
    """

    global global_ngram_dict
    global_ngram_dict = pickle.load(open(os.path.join(DICO_PATH, str(n) + '-gram',
                                                      'ast_esprima_simpl'), 'rb'))


def nb_features(n):
    """
        Number of n-grams considered.

        -------
        Parameter:
        - n: Integer
            Stands for the size of the sliding-window which goes through the units contained
            in the files to be analysed.

        -------
        Returns:
        - int
            The number of n-grams that will be considered, depending on the value of n.
    """

    ns_features = [19, 361, 1000, 4000, 15000, 40000, 100000]
    if n < 8:
        n_features = ns_features[n - 1]
    else:
        n_features = 200000
    return n_features


def vect_proba_of_n_grams(input_file, tolerance, n, dico_ngram_int):
    """
        Vector representing the probability of each n-grams for input_file.

        -------
        Parameter:
        - input_file: str
            Path of the file to be analysed.
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option).
            The values 'true' and 'false' shall be used to enable this tolerant mode.
        - n: int
            Stands for the size of the sliding-window which goes through the units contained
            in the files to be analysed.
        - dico_ngram_int: Dictionary
            Key: N-gram;
            Value: Unique integer.

        -------
        Returns:
        - np.array
            Dimension: integer representing an n-gram;
            Value: probability of occurrences of a given tuple of n-gram.
        - or None if matrix_all_n_grams is empty.
    """

    dico_of_n_grams, nb_n_grams = count_sets_of_n_grams(input_file, tolerance, n)
    if dico_of_n_grams is not None:
        n_features = nb_features(n)
        vect_n_grams_proba = np.zeros(n_features)
        # Bigger vector on purpose, to have space for new n-grams
        for key, proba in dico_of_n_grams.items():
            map_ngram_int = n_gram_to_int(dico_ngram_int, key, n_features)
            if map_ngram_int is not None:
                vect_n_grams_proba[map_ngram_int] = proba / nb_n_grams

        return vect_n_grams_proba
    return None


def n_gram_to_int(dico_ngram_int, n_gram, n_features):
    """
        Convert an n-gram into an int.

        -------
        Parameters:
        - dico_ngram_int: Dictionary
            Key: N-gram;
            Value: Unique integer.
        - n_gram: Tuple
            Represents the n-gram to be converted into an int.
        - n_features: int
            The number of n-grams that will be considered, depending on the value of n.

        -------
        Returns:
        - Integer
            Note that the operation that transforms an n-gram to an int is a bijection.
        - or None if the vector space's size is exceeded.
    """

    try:
        i = dico_ngram_int[str(n_gram)]
    except KeyError:  # Key not in dico, we add it. Beware dico referenced as global variable.
        dico_ngram_int[str(n_gram)] = len(dico_ngram_int)
        i = dico_ngram_int[str(n_gram)]
    if i < n_features:
        return i
    else:
        logging.warning('The vector space size of ' + str(n_features) + ' is too small.'
                        + ' Tried to access element ' + str(i)
                        + '. This can be changed in ngrams_handling.nb_features(n)')
        return None


def int_to_n_gram(dico_ngram_int, i):
    """
        Convert an int into an n-gram.

        -------
        Parameters:
        - dico_ngram_int: Dictionary
            Key: int;
            Value: Unique n-gram.
        - i: Integer
            Represents the int to be converted into an n-gram.

        -------
        Returns:
        - Tuple
            Corresponds to an n-gram.
            Note that the operation that transforms an int to an n-gram is a bijection.
        - or None if i is not in dico.
    """

    try:
        ngram = dico_ngram_int[str(i)]
        return ngram
    except KeyError as err:
        logging.warning('The key ' + str(err) + ' is not in the n-gram - int mapping dictionary')


############################################################
#                        HASH MAPPING
############################################################


# Mapping a JS file to a CSR matrix containing the frequency of the n-grams it contains.
def csr_proba_of_n_grams_hash_storage(input_file, tolerance, n, n_features):
    """
        Maps an input file to a CSR matrix containing the frequency of its n-grams.
        - Production of n-grams and analysis of their frequency (+ normalization);
        - Each n-grams is mapped to a consistent dimension of a vector space (with an hash,
        collision possible if n_features is to small)
        - Storage of the results in a CSR matrix.

        -------
        Parameters:
        - input_file: str
            Path of the file to be analysed.
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option).
            The values 'true' and 'false' shall be used to enable this tolerant mode.
        - n: int
            Stands for the size of the sliding-window which goes through the units contained
            in the files to be analysed.
        - n_features: int
            Size of the resulting vector space. This can be changed in nb_features(n).

        -------
        Returns:
        - csr_matrix
            Non-compacted dimension: 1 x n_features;
            Value: probability of occurrences of an n-gram.
        - or None if the file could not be parsed.
    """

    tokens_int = tokens.tokens_to_numbers(input_file, tolerance)
    if tokens_int is not None:
        corpus = [str(tokens_int)]
        vectorizer = HashingVectorizer(token_pattern=r"(?u)\b\w+\b", ngram_range=(n, n), norm='l1',
                                       alternate_sign=False, n_features=n_features)
        res = vectorizer.fit_transform(corpus)

        return res
    return None


def concatenate_csr_matrices(matrix1, matrix2, nb_col):
    """
        Horizontal concatenation of 2 CSR matrices.

        -------
        Parameters:
        - matrix1: csr_matrix
        - matrix2: csr_matrix
        - nb_col: int
            Number of non-compacted columns the resulting matrix will have.

        -------
        Returns:
        - csr_matrix
            Concatenation of matrix1 on top followed by matrix2 below.
            Nb of lines: nb_lines(matrix1) + nb_lines(matrix2);
            Nb of columns (non-compacted): nb_col.
    """

    if matrix1 is None:
        return matrix2
    elif matrix2 is None:
        return matrix1
    res = csr_matrix((matrix1.shape[0] + matrix2.shape[0], nb_col))
    res.data = np.concatenate((matrix1.data, matrix2.data))
    res.indices = np.concatenate((matrix1.indices, matrix2.indices))
    new_ind_ptr = matrix2.indptr + len(matrix1.data)
    new_ind_ptr = new_ind_ptr[1:]
    res.indptr = np.concatenate((matrix1.indptr, new_ind_ptr))
    return res
