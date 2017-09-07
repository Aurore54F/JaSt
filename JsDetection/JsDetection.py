#!/usr/bin/python

'''
    Indicate whether given files are either valid JavaScript files,
    malformed JavaScript files or if they are no JavaScript files.
'''

import subprocess # to call Shell commands
import os # for OS dependent functionality
import argparse # to deal with command line arguments

currentPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
OUTPUT_TEXTS = ['valid JavaScript', 'not JavaScript', 'malformed JavaScript']

def isJsFile(givenFile):
    '''
        Given a file path, indicate whether the file is either valid JavaScript,
        malformed JavaScript or no JavaScript. On a system error -1 is returned.

        -------
        Parameter:
        - givenFile: string
            Path of the file to be analysed.

        -------
        Returns:
        - Integer
            Indicates whether the file is either valid JavaScript (0), malformed
            JavaScript (2) or no JavaScript (1).
    '''

    try:
        subprocess.check_output('nodejs '+currentPath+'/src/JsEsprima/parser.js ' + givenFile + \
							' 2> /dev/null', shell=True)
        # TODO The code does not handle errors by esprima well. Popen should be used.
        return 0

    except subprocess.CalledProcessError as e:
        if  e.returncode == 1:
            if str(e.output) == "b''": # The file could not be parsed: not a JS sample
                return 1
            return 2 # The file could partially be parsed: malformed JS
            #print("\n".join(i for i in e.output if i.startwith("Error")))
        elif e.returncode != 0:
            #Something else went wrong, we do not handle this here
            raise

    except OSError: # System-related error
        print("System-related error")
        return -1


def main():
    '''
        A list of files, or of repositories, can be given as command line arguments, for this
        program to indicate whether the files are either valid, malformed or no JavaScript.

        -------
        Returns:
        - Message (stdout) whose format is:
            * For valid JS files: <fileName>: valid JavaScript
            * For malformed JS files: <fileName>: malformed JavaScript
            * For no JS files: <fileName>: not JavaScript
    '''

    parser = argparse.ArgumentParser(description='Given a list of repositories, or of files paths,\
    indicate whether the files are either valid, malformed or if they are no JavaScript.')
    # Creating an ArgumentParser object which holds all the information necessary to parse
    #the command line into Python data types.

    parser.add_argument('--f', metavar='FILE', nargs='+', help='files to be tested')
    parser.add_argument('--d', metavar='DIR', nargs='+', help='directories to be tested')

    args = vars(parser.parse_args())


    if args['f'] != None:
        files2do = args['f']
    else:
        files2do = []
    if args['d'] != None:
        for cdir in args['d']:
            files2do.extend(cdir + '/' + cfile for cfile in os.listdir(cdir))
    results = [isJsFile(cfile) for cfile in files2do]
    for cfile, res in zip(files2do, results):
        print("%s: %s" % (cfile, OUTPUT_TEXTS[res]))
    print('\tNumber of correct files: %d' % len([i for i in results if i == 0]))


if __name__ == "__main__": # Executed only if run as a script
    main()
