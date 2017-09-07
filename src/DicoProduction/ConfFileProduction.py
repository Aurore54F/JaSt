
'''
    Basis for storing dictionaries in a configuration file.
'''

import os # for OS dependent functionality


def dicoStorage(directoryName, fileName, description, orderedDico):
    '''
        Storing a given dictionary in a configuration file.

        -------
        Parameters:
        - directoryName: String
            Indicates where the configuration file will be stored.
        - fileName: String
            Indicates the configuration file name.
        - description: String
            Provides a short description for the configuration file.
        - orderedDico: Dictionary
            Dictionary to be stored in a configuration file

        -------
        Returns:
        - Configuration file
            Stores the previous dictionary.
    '''

    if not os.path.exists(directoryName):
        os.makedirs(directoryName)

    with open(directoryName + '/' + fileName, 'w') as dicoFile:
        dicoFile.write(description)
        for el in orderedDico:
            dicoFile.write("    '" + str(el) + "'" + ' : ' + str(orderedDico[el]) + ',\n')
        dicoFile.write('}')


def prettyPrintDico(dico):
    '''
        Print a human-readable content of a dictionary.
        -------
        Parameter:
        - dico: Dictionary
    '''

    print('================================')
    for el in dico:
        print(str(el) + '    : ' + str(dico[el]) + '\n')
    print('================================')
