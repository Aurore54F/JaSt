#!/usr/bin/python


"""
    Syntactic analysis of JavaScript files.
"""

import os
import sys
import pickle
import logging

import ngrams_handling


CURRENT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
DICO_PATH = os.path.join(CURRENT_PATH, 'ngrams2int')


def main_analysis(js_dirs, js_files, labels_files, labels_dirs, n, tolerance, dict_not_hash):
    """
        Main function, performs a static analysis (syntactic using the AST)
        of JavaScript files given in input.

        -------
        Parameters:
        - js_dirs: list of strings
            Directories containing the JS files to be analysed.
        - js_files: list of strings
            Files to be analysed.
        - labels_files: list of strings
            True label's name of the current data: either benign or malicious.
            One label for one file.
        - labels_dirs: list of strings
            True label's name of the current data: either benign or malicious.
            One label for one directory.
        - n: int
            Stands for the size of the sliding-window which goes through the units contained
            in the files to be analysed.
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option).
            The values 'true' and 'false' shall be used to enable this tolerant mode.
        - dict_not_hash: boolean
            True if a dictionary is used to map n-grams to int, False if hashes are used.

        -------
        Returns:
        -list:
            Contains the results of the static analysis of the files given as input.
            * 1st element: list containing valid files' name (i.e. files that could be parsed);
            * 2nd element: list / csr_matrix representing the analysis results (n-grams frequency)
            with one line per valid JS file;
            * 3rd element: list containing the true labels of the valid JS files.

    """

    if js_dirs is None and js_files is None:
        logging.error('Please, indicate a directory or a JS file to be studied')

    else:
        if dict_not_hash:
            ngrams_handling.import_modules(n)

        if js_files is not None:
            files2do = js_files
            if labels_files is None:
                labels_files = ['?' for _, _ in enumerate(js_files)]
            labels = labels_files
        else:
            files2do, labels = [], []
        if js_dirs is not None:
            i = 0
            if labels_dirs is None:
                labels_dirs = ['?' for _, _ in enumerate(js_dirs)]
            for cdir in js_dirs:
                for cfile in os.listdir(cdir):
                    files2do.append(os.path.join(cdir, cfile))
                    if labels_dirs is not None:
                        labels.append(labels_dirs[i])
                i += 1

        tab_res = [[], [], []]

        if not dict_not_hash:
            csr_res = None
            n_features = ngrams_handling.nb_features(n)

        for j, _ in enumerate(files2do):
            if dict_not_hash:
                res = ngrams_handling.vect_proba_of_n_grams(files2do[j], tolerance, n,
                                                            ngrams_handling.global_ngram_dict)
            else:  # hashes
                res = ngrams_handling.csr_proba_of_n_grams_hash_storage(files2do[j], tolerance,
                                                                        n, n_features)
            if res is not None:
                tab_res[0].append(files2do[j])
                if dict_not_hash:
                    tab_res[1].append(res)
                else:  # hashes
                    csr_res = ngrams_handling.concatenate_csr_matrices(csr_res, res, n_features)
                if labels and labels != []:
                    tab_res[2].append(labels[j])
        if dict_not_hash:
            sys.path.insert(0, os.path.join(DICO_PATH, str(n) + '-gram'))
            pickle.dump(ngrams_handling.global_ngram_dict,
                        open(os.path.join(DICO_PATH, str(n) + '-gram', 'ast_esprima_simpl'), 'wb'))
        else:
            tab_res[1].append(csr_res)
            tab_res[1] = tab_res[1][0]

        return tab_res
