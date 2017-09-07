
'''
    Producing n-grams from tokens by moving a fixed-length window to extract subsequence of
    length n.
'''

from itertools import product # for the cartesian product
import __init__

def nGramsList(numbersList, n=4):
    '''
        Given a list of numbers, produce every possible n-gram (n configurable) and store them
        in a matrix.

        -------
        Parameters:
        - numbersList: List
            Contains integers which represent the tokens extracted from a JS file
            (see TokensProduction.py).
        - n: Integer
            Stands for the size of the sliding-window which goes through the previous list.
            Default value is 4.

        -------
        Returns:
        - Matrix
            Rows: tuples representing every possible n-gram (produced from numbersList);
            Columns: part of the previous tuples
        - or None if numbersList is empty.
    '''

    if numbersList is not None:
        if n < 1 or n > (len(numbersList)):
            print('Error: to display a list of n-grams, n > 0 and n < len(list-of-numbers)')
            print('\nIt means that the file has less tokens than the length n of an n-gram.')
            # TODO: possible that n > (len(numbersList)), e.g. the JS file only contains
            #comments: 1 token < n if n > 1.
            #return

        else:
            matrixAllNGrams = [[] for j in range(len(numbersList) - (n - 1))]
            # "len(numbersList) - (n - 1)" being the number of n-grams that can be obtained
            #from the data of numbersList
            for j in range(len(numbersList) - (n - 1)): # Loop on all the n-grams
                matrixAllNGrams[j] = [numbersList[j + i] for i in range(n)]
                # Loop on the components of a given n-gram

                matrixAllNGrams[j] = tuple(matrixAllNGrams[j])
                # Stored in tuples as they are immutable (lists are not; strings are,
                #but for every op in a string,
                #a new string is created). I needed an immutable type since it will be used
                #as key in a dictionary.

            return matrixAllNGrams


def nGramsCsv(numbersList, n=4, filePath='nGram.csv'):
    '''
        Given a list of numbers, produce every possible n-gram (n configurable) and store
        them in a CSV file.

        -------
        Parameters:
        - numbersList: List
            Contains integers which represent the tokens extracted from a JS file
            (see TokensProduction.py).
        - n: Integer
            Stands for the size of the sliding-window which goes through the previous list.
            Default value is 4.
        - filePath: String
            To choose the location of the CSV file which will be produced. Default: "./nGram.csv".

        -------
        Returns:
        - CSV file
            Contains every possible n-gram (produced from numbersList).
    '''

    if numbersList is not None:
        if n < 1 or n >= (len(numbersList)):
            print('Error: to display a list of n-grams, n > 0 and n < len(list-of-numbers)')
            #return

        else:
            with open(filePath, 'w') as csvFile:
                for j in range(len(numbersList) - (n - 1)):
                    csvFile.write(str(numbersList[j]))
                    for i in range(n - 1):
                        csvFile.write(',' + str(numbersList[j + i + 1]))
                        csvFile.write('\n')


def allPossibleNGrams(dico, n=4):
    '''
        Produce all the possible combinations of n-grams using the values stored either in
        the dictionary DicoOfTokensSlimit.py or DicoOfTokensEsprima.py.
        The values of the dictionary are indeed seen as a list of Integers.

        -------
        Parameters:
        - dico: Dictionary
        - n: Integer
            Stands for the size of the sliding-window which goes through the previous list.
            Default value is 4.

        -------
        Returns:
        - List
            Contains every possible n-grams that can be produced from the values of the
            input "dico".
    '''

    l = [str(dico[key]) for key in dico] # List containing all the numbers associated with a token

    listNGrams = [i for i in product(l, repeat=n)] # Cartesian product
    print('Theorie: ' + str(len(l)**n) + '\nReality: ' + str(len(listNGrams)))
    # Nb of n-grams that can be produced

    return listNGrams
