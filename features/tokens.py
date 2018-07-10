
"""
    Extracting syntactic units from a JavaScript file and converting them into integers.
"""

import sys
import os

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(SRC_PATH, 'features', 'tokens2int'))
sys.path.insert(0, os.path.join(SRC_PATH, 'js'))

import parser_esprima_simpl
import is_js

DICO_TOKENS_INT = parser_esprima_simpl.ast_units_dico


def ast_used_esprima(input_file, tolerance):
    """
        Given an input JavaScript file, create a list containing the esprima syntactic
        units present in the file.
        The order of the units stored in the previous list resembles a tree traversal using
        the depth-first algorithm post-order.

        -------
        Parameters:
        - input_file: str
            Path of the file to be analysed. Should it be malformed or no JS file,
            then an exception will be raised
            (see js.is_js_file).
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option).
            The value 'true' shall be used to enable this tolerant mode.

        -------
        Returns:
        - List
            Contains the esprima syntactic units present in the input file.
        - or None if the file either is no JS or malformed.
    """

    units = is_js.is_js_file(input_file, syntactical_units=True, tolerance=tolerance)
    if isinstance(units, list):  # otherwise an error code could be returned
        # instead of a list of syntactic units
        return units
    return None


def tokens_to_numbers(input_file, tolerance):
    """
        Convert a list of syntactic units in their corresponding numbers
        (as indicated in the corresponding units dictionary).

        -------
        Parameters:
        - input_file: str
            Path of the file to be analysed.
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option).
            The values 'true' and 'false' shall be used to enable this tolerant mode.
        -------
        Returns:
        - List
            Contains the Integers which correspond to the units given in tokens_list.
        - or None if tokens_list is empty (cases where the JS file considered either is no JS,
        malformed or empty).
    """

    tokens_list = ast_used_esprima(input_file, tolerance)  # List of syntactic units

    if tokens_list is not None and tokens_list != []:
        return list(map(lambda x: DICO_TOKENS_INT[x], tokens_list))
    return None
