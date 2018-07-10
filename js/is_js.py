#!/usr/bin/python

"""
    Indicate whether given files are either valid JavaScript files,
    malformed JavaScript files or if they are no JavaScript files.
"""

import subprocess  # to call Shell commands
import os  # for OS dependant functionality
import argparse  # to deal with command line arguments
import logging

OUTPUT_TEXTS = ['valid JavaScript', 'not JavaScript', 'malformed JavaScript']
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def is_js_file(given_file, syntactical_units=False, tolerance='false'):
    """
        Given a file path, indicate whether the file is either valid JavaScript,
        malformed JavaScript or no JavaScript. On a system error -1 is returned.

        -------
        Parameter:
        - given_file: str
            Path of the file to be analysed.
        - syntactical_units: bool
            Instead of returning the error code 0, the list of syntactical units
            obtained can be returned. Default value is False.
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option). Default value is 'false'.
            The value 'true' shall be used to enable this tolerant mode.

        -------
        Returns:
        - int
            Indicates whether the file is either valid JavaScript (0), malformed
            JavaScript (2) or no JavaScript (1).
        - or List of syntactical units
            If given_file is valid and syntactical_units true.
    """

    with open(os.path.join(SRC_PATH, 'is_js.log'), 'w') as my_log:
        try:
            result = subprocess.check_output('nodejs '
                                             + os.path.join(SRC_PATH, 'features',
                                                            'parsing', 'parser.js')
                                             + ' ' + given_file
                                             + ' ' + tolerance, stderr=my_log, shell=True)
            # result is a string containing the syntactical units (as found by esprima) of
            # the given JS script, separated by '\n'.
            # Structure of a token: "b'Literal\n'"
            if syntactical_units:
                syntax_part = str(result).split("b'")[1].split('\\n')  # Keyword as used in JS
                del syntax_part[len(syntax_part) - 1]  # As last one = ''
                return syntax_part  # The order of the units returned resembles a tree traversal
                # using the depth-first algorithm post-order.
            return 0

        except subprocess.CalledProcessError as err:
            if err.returncode == 1 or err.returncode == 8:
                if str(err.output) == "b''":  # The file could not be parsed: not a JS sample
                    return 1
                return 2  # The file could partially be parsed: malformed JS
            elif err.returncode != 0:
                # Something else went wrong, we do not handle this here
                logging.exception("Something went wrong with the file <" + given_file + ">: "
                                  + str(err))

        except OSError:  # System-related error
            logging.exception("System-related error")
            return -1


def main():
    """
        A list of files, or of repositories, can be given as command line arguments, for this
        program to indicate whether the files are either valid, malformed or no JavaScript.

        -------
        Returns:
        - Message (stdout) whose format is:
            * For valid JS files: <fileName>: valid JavaScript
            * For malformed JS files: <fileName>: malformed JavaScript
            * For no JS files: <fileName>: not JavaScript
    """

    parser = argparse.ArgumentParser(description='Given a list of directory, or of file paths,\
    indicates whether the files are either\n\
    valid (\'<fileName>: valid JavaScript\'),\n\
    malformed (\'<fileName>: malformed JavaScript\'),\n\
    or no JavaScript (\'<fileName>: not JavaScript\').')
    # Creating an ArgumentParser object which holds all the information necessary to parse
    # the command line into Python data types.

    parser.add_argument('--f', metavar='FILE', nargs='+', help='files to be tested')
    parser.add_argument('--d', metavar='DIR', nargs='+', help='directories to be tested')
    parser.add_argument('--v', metavar='VERBOSITY', type=int, nargs=1, choices=[0, 1, 2, 3, 4, 5],
                        default=[2], help='controls the verbosity of the output, from 0 (verbose) '
                                          + 'to 5 (less verbose)')

    args = vars(parser.parse_args())
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.getLevelName(args['v'][0] * 10))

    if args['f'] is not None:
        files2do = args['f']
    else:
        files2do = []
    if args['d'] is not None:
        for cdir in args['d']:
            files2do.extend(os.path.join(cdir, cfile) for cfile in os.listdir(cdir))
    results = [is_js_file(cfile) for cfile in files2do]
    for cfile, res in zip(files2do, results):
        print("%s: %s" % (cfile, OUTPUT_TEXTS[res]))
    logging.info('\tNumber of correct files: %d', len([i for i in results if i == 0]))


if __name__ == "__main__":  # Executed only if run as a script
    main()
