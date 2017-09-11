
'''
    Counting the number of occurrences (probability) of each n-gram in JavaScript files.
'''

import pickle # to save figure to disk
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA as sklearnPCA

import __init__

def countSetsOfNGrams(matrixAllNGrams):
    '''
        Given a matrix containing every possible n-gram (for a JavaScript given file), count
        and store (once) the probability of occurrences of each set of
        n-gram in a dictionary.

        -------
        Parameter:
        - matrixAllNGrams: matrix
            Contains in each row a tuple representing an n-gram.

        -------
        Returns:
        - Dictionary
            Key: tuple representing an n-gram;
            Value: probability of occurrences of a given tuple of n-gram.
        - or None if matrixAllNGrams is empty.
    '''

    if matrixAllNGrams is not None:
        dicoOfNGrams = {}
        setsNGrams = len(matrixAllNGrams) # Number of lines in the matrix, i.e. of sets of n-grams.
        for j in range(setsNGrams):
            if matrixAllNGrams[j] in dicoOfNGrams:
                dicoOfNGrams[matrixAllNGrams[j]] = dicoOfNGrams[matrixAllNGrams[j]] + 1/setsNGrams
                # Normalization to enable future comparisons
            else:
                dicoOfNGrams[matrixAllNGrams[j]] = 1/setsNGrams

        return dicoOfNGrams
    #else:
        #print('Matrix of type NoneType')


def histoFromDico(orderedDico, figPath='histo.png', title='4-grams frequency in a given\
                  JavaScript document', xlabel='4-grams', ylabel='Frequency'):
    '''
        Histogram displaying the probability of apparition of each n-gram as stored in the
        dictionary in input.

        -------
        Parameters:
        - orderedDico: Dictionary
            Key: tuple representing an n-gram;
            Value: probability of occurrences of a given tuple of n-gram.
        - figPath:
            Histogram location. Default: "./histo.png".
        - title: String
            Title of the histogram. Default: '4-grams frequency in a given JavaScript document'.
        - xlabel: String
            Xlabel of the histogram. Default: '4-grams'.
        - ylabel: String
            Ylabel of the histogram. Default: 'Frequency'.

        -------
        Returns:
        - File
            Displays the histogram.
    '''

    #fig = plt.figure()
    plt.bar(range(len(orderedDico)), orderedDico.values(), align='center')
    plt.xticks(range(len(orderedDico)), (orderedDico.keys()), rotation=90)
    # n-gram labels are vertical
    #plt.title("\n".join(wrap(title, 60))) # Title written in several line if necessary
    plt.title(title[-44:])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout() # Otherwise the xlabel does not fit in the figure
    #plt.show() # To display the histogram

    # Manage the histogram size
    fig = plt.gcf() # uncomment for slimit and esprimaAst
    fig.set_size_inches(25, 10) # uncomment for slimit and esprimaAst

    plt.savefig(figPath, dpi=100)
    pickle.dump(fig, open(figPath, 'wb'))
    plt.clf() # Otherwise all figures are written on one another



def pcaPlotting(file='/home/aurore/Documents/Code/MatrixFiles/esprima.csv',\
			figPath='pcaPlotting.png', title='Projection of the 4-grams frequency of JavaScript\
			files', annotate=False, label=None):
    '''
        Graph representing each file features (i.e. list of n-grams with their associated
        probability) in 2D (using a PCA 2-dimensional transformation).
        <http://www.apnorton.com/blog/2016/12/19/Visualizing-Multidimensional-Data-in-Python/>.

        -------
        Parameters:
        - file: File
            Contains for each JS file studied (row) the probability of occurrences of all the
            n-gram (column) encountered in the JS corpus considered.
        - figPath:
            Figure location. Default: "./pcaPlotting.png".
        - title: String
            Title of the histogram. Default: 'Projection of the 4-grams frequency of
            JavaScript files'.
        - annotate: Boolean
            Indicates whether each file, represented by a circle on the figure, will be given a
            unique id. Default value is True.
        - label: String
            Indicates the label's name of the current data (if any), useful for supervised
            classification. Default value is None.

        -------
        Returns:
        - File
            Plots the multi dimensional vector representing the n-grams, using a 2-dimensional PCA.
    '''

    data = pd.read_csv(file)

    X = data.ix[:, '0':]  # Split off features

    pca = sklearnPCA(n_components=2) #2-dimensional PCA
    #X_norm = (X - X.min())/(X.max() - X.min())
    transformed = pd.DataFrame(pca.fit_transform(X))

    fig = plt.figure()

    if label is not None and label != []:
        '''
        colors = []
        for name,hex in matplotlib.colors.cnames.items():
            colors.append(name)
        '''
        j = 0
        colors = ['red', 'deepskyblue', 'seagreen', 'sandybrown', 'lightpink', 'darkslateblue', 'khaki', 'lightgray', 'slategray', 'mintcream', 'darkcyan', 'darkslategrey', 'lightyellow', 'gainsboro', 'midnightblue', 'lawngreen', 'deeppink', 'thistle', 'aliceblue', 'oldlace', 'mediumorchid', 'lavenderblush', 'lightblue', 'orangered', 'floralwhite', 'paleturquoise', 'coral', 'navy', 'slateblue', 'rebeccapurple', 'darkslategray', 'limegreen', 'blanchedalmond', 'lightcyan', 'seashell', 'beige', 'magenta', 'darkgoldenrod', 'skyblue', 'forestgreen', 'blue', 'lavender', 'mediumslateblue', 'aqua', 'mediumvioletred', 'lightsteelblue', 'azure', 'cyan', 'mistyrose', 'darkorchid', 'orange', 'gold', 'chartreuse', 'bisque', 'olive', 'darkmagenta', 'lightgreen', 'darkviolet', 'lightgrey', 'mediumblue', 'indigo', 'papayawhip', 'powderblue', 'black', 'aquamarine', 'wheat', 'hotpink', 'mediumseagreen', 'royalblue', 'pink', 'mediumaquamarine', 'goldenrod', 'peachpuff', 'darkkhaki', 'silver', 'mediumspringgreen', 'yellowgreen', 'cadetblue', 'olivedrab', 'darkgray', 'chocolate', 'palegoldenrod', 'darkred', 'peru', 'fuchsia', 'darkturquoise', 'cornsilk', 'lightgoldenrodyellow', 'lightslategray', 'dimgray', 'white', 'sienna', 'orchid', 'darkorange', 'darkseagreen', 'steelblue', 'darkgreen', 'violet', 'slategrey', 'lightsalmon', 'palegreen', 'yellow', 'lemonchiffon', 'antiquewhite', 'green', 'lightslategrey', 'tan', 'honeydew', 'whitesmoke', 'blueviolet', 'navajowhite', 'darkblue', 'mediumturquoise', 'dodgerblue', 'lightskyblue', 'crimson', 'snow', 'brown', 'indianred', 'palevioletred', 'plum', 'linen', 'cornflowerblue', 'saddlebrown', 'springgreen', 'lightseagreen', 'greenyellow', 'ghostwhite', 'rosybrown', 'darkgrey', 'grey', 'lime', 'teal', 'gray', 'mediumpurple', 'darkolivegreen', 'burlywood', 'tomato', 'lightcoral', 'purple', 'salmon', 'darksalmon', 'dimgrey', 'moccasin', 'maroon', 'ivory', 'turquoise', 'firebrick']
        y = data['Label']      # Split off classifications
        uniqueLabel = []
        for el in y:
            if el not in uniqueLabel:
                uniqueLabel.append(el)
        for l in uniqueLabel:
            plt.scatter(transformed[y == l][0], transformed[y == l][1], label=l, marker='o',\
					facecolors='none', edgecolors=colors[j])
            j += 1
    else:
        plt.scatter(transformed[:][0], transformed[:][1])

    if annotate is True:
        for i in range(len(data)):
            fig.annotate(str(i+1), (transformed[0][i], transformed[1][i]))

    #fig = plt.gcf()
    #fig.set_size_inches(25, 10)

    plt.title(title)
    #plt.xlabel(xlabel)
    #plt.ylabel(ylabel)
    plt.legend()
    plt.grid()

    #fig.show()
    pickle.dump(fig, open(figPath, 'wb'))
    plt.savefig(figPath, dpi=100)
    fig.clf() # Otherwise all figures are written on one another
