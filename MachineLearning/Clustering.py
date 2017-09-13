
'''
    Clustering of JavaScript files into k (configurable) families.
'''

import os
import argparse # To parse command line arguments
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#import pickle # to save figure to disk

from sklearn.decomposition import PCA as sklearnPCA
from sklearn.cluster import KMeans

import sys
import os

currentPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, currentPath+'/src') #To add a directory to import modules from
sys.path.insert(0, currentPath+'/src/Dico_MapTokens-Int')
sys.path.insert(0, currentPath+'/JsDetection')
sys.path.insert(0, currentPath+'/src/Dico_MapNGrams-Int')
sys.path.insert(0, currentPath+'/src/DicoProduction')

#from StaticAnalysisJs import mainS
import ConfFileProduction
import TokensProduction
import NGramsProduction
import NGramsAnalysis
import NGramsRepresentation
import PreprocessingJsData
import FilesForJsClustering
import StaticAnalysisJs

import DicoIntToNGramsSlimit
import DicoNGramsToIntSlimit
import DicoIntToNGramsEsprima
import DicoNGramsToIntEsprima
import DicoIntToNGramsEsprimaAst
import DicoNGramsToIntEsprimaAst
import DicoIntToNGramsEsprimaAstSimplified
import DicoNGramsToIntEsprimaAstSimplified

import DicoOfTokensSlimit
import DicoOfTokensEsprima
import DicoOfAstEsprima
import DicoOfAstEsprimaSimplified

import JsDetection


def nbClusters(dataFile, figDir=currentPath+'/Clustering/', figName='NumberOfClusters.png',\
               minA=1, maxA=5):
    '''
        Given a CSV file respecting the structure defined in our module src/ and containing
        a static analysis of JavaScript executables, display the evolution of the error rate
        (Total squared distance inside clusters) as the number of clusters increases.

        -------
        Parameters:
        - dataFile: string
            Path of the CSV file containing a static analysis of JavaScript executables.
        - figDir: string
            Path to stored the figure displaying the evolution of the error rate as the
            number of clusters increases.
            Default value being the folder MalwareClustering/Clustering/.
        - figName: string
            Name of the previous figure.
            Default value being 'NumberOfClusters.png'.
        - minA: int
            Minimum number of cluster. Default value: 1.
        - maxA: int
            Maximum number of clusters. Default value: 5.

        -------
        Returns:
        - .png file
            Displaying the evolution of the error rate as the number of clusters increases
            (from minA to maxA included).
    '''

    # Directory to store the clustering related files
    if not os.path.exists(figDir):
        os.makedirs(figDir)

    data = pd.read_csv(dataFile) # Read the CSV file
    X = data.ix[:, '0':] # 2D vector containing all the attributes of the samples considered

    '''
    X, y = make_blobs(n_samples = 150, n_features = 30, centers = 3, cluster_std = 0.5,\
    shuffle = True, random_state = 0) # Test with 3 clusters
    '''

    distorsions = []
    for i in range(minA, maxA+1):
        kmeans = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=300, random_state=0)
        # n_init: with 10 different centroids, little SSE
        kmeans.fit(X) # k-means++ algorithm
        distorsions.append(kmeans.inertia_) # Total squared distance inside clusters

    plt.plot(range(minA, maxA+1), distorsions, marker='x')
    plt.grid()
    plt.xlabel('Number of clusters')
    plt.ylabel('Total squared distance inside clusters')
    #pickle.dump(fig,open(figPath,'wb')) # Python's format
    #plt.show()
    plt.savefig(figDir+figName, dpi=100)
    plt.clf() # Otherwise all figures are written on one another



def clustering(dataFile, nbCluster, figDir=currentPath+'/Clustering/',\
               figName='ClusteringPca.png', displayFig=False, annotate=False,\
               title='Projection of the 4-grams frequency of JavaScript files'):
    '''
        Given a CSV file respecting the structure defined in our module src/ and containing
        a static analysis of JavaScript executables, clusters the JavaScript documents
        in k families.

        -------
        Parameters:
        - dataFile: string
            Path of the CSV file containing a static analysis of JavaScript executables.
        - nbCluster: int
            Number of clusters whished.
        - figDir: string
            Path to stored the figure displaying the evolution of the error rate as the
            number of clusters increases.
            Default value being the folder MalwareClustering/Clustering/.
        - figName: string
            Name of the previous figure.
            Default value being 'NumberOfClusters.png'.
        - displayFig: boolean
            PCA projection of the PCA files studied, with several colours standing for
            several clusters. Default value: false.
        - annotate: boolean
            Indicates whether each file, will be given a unique id. Default value: false.
        - title: String
            Title of the PCA figure.
            Default value: 'Projection of the 4-grams frequency of JavaScript files'

        -------
        Returns:
        - In stdout:
            List of the files studied with the associated cluster's number.
        - .png file (if displayFig is True):
            Displaying the repartition of the files studied on a plane.
    '''

    # Directory to store the clustering related files
    if not os.path.exists(figDir):
        os.makedirs(figDir)

    data = pd.read_csv(dataFile) # Read the CSV file
    names = data['Outlook'] # Vector containing all the names of the samples considered
    X = data.ix[:, '0':] # 2D vector containing all the attributes of the samples considered
    X = np.asarray(X)

    km = KMeans(n_clusters=nbCluster, init='k-means++', n_init=10, max_iter=300,\
                tol=1e-04, random_state=0)
    # n_init: with 10 different centroids, little SSE

    labelsPredicted = km.fit_predict(X) # Perform k-means++ algorithm on an array of test
    #vectors X and predict the target values

    colors = ['orange', 'lightblue', 'red', 'lightgreen', 'lightpink', 'darkgoldenrod', 'deepskyblue', 'seagreen', 'darkslateblue', 'gainsboro', 'khaki', 'slategray', 'darkcyan', 'darkslategrey', 'lawngreen', 'deeppink', 'thistle', 'sandybrown', 'mediumorchid', 'orangered', 'paleturquoise', 'coral', 'navy', 'slateblue', 'rebeccapurple', 'darkslategray', 'limegreen', 'magenta', 'skyblue', 'forestgreen', 'blue', 'lavender', 'mediumslateblue', 'aqua', 'mediumvioletred', 'lightsteelblue', 'cyan', 'mistyrose', 'darkorchid', 'gold', 'chartreuse', 'bisque', 'olive', 'darkmagenta', 'darkviolet', 'lightgrey', 'mediumblue', 'indigo', 'papayawhip', 'powderblue', 'aquamarine', 'wheat', 'hotpink', 'mediumseagreen', 'royalblue', 'pink', 'mediumaquamarine', 'goldenrod', 'peachpuff', 'darkkhaki', 'silver', 'mediumspringgreen', 'yellowgreen', 'cadetblue', 'olivedrab', 'darkgray', 'chocolate', 'palegoldenrod', 'darkred', 'peru', 'fuchsia', 'darkturquoise', 'cornsilk', 'lightgoldenrodyellow', 'lightslategray', 'dimgray', 'white', 'sienna', 'orchid', 'darkorange', 'darkseagreen', 'steelblue', 'darkgreen', 'violet', 'slategrey', 'lightsalmon', 'palegreen', 'yellow', 'lemonchiffon', 'antiquewhite', 'green', 'lightslategrey', 'tan', 'honeydew', 'whitesmoke', 'blueviolet', 'navajowhite', 'darkblue', 'mediumturquoise', 'dodgerblue', 'lightskyblue', 'crimson', 'snow', 'brown', 'indianred', 'palevioletred', 'plum', 'linen', 'cornflowerblue', 'saddlebrown', 'springgreen', 'lightseagreen', 'greenyellow', 'ghostwhite', 'rosybrown', 'darkgrey', 'grey', 'lime', 'teal', 'gray', 'mediumpurple', 'darkolivegreen', 'burlywood', 'tomato', 'lightcoral', 'purple', 'salmon', 'darksalmon', 'dimgrey', 'moccasin', 'maroon', 'ivory', 'turquoise', 'firebrick']
    markers = ['s', 'v', 'o', 'd', 'p', '^', '<', '>', '1', '2', '3', '4', '8', 'h', '.', 'H', '+', 'x', 'D', '|', '_', 's', 'v', 'o', 'd', 'p', '^', '<', '>', '1', '2', '3', '4', '8', 'h', '.', 'H', '+', 'x', 'D', '|', '_']
    # Different markers and colours for legibility reasons

    if displayFig:
        for i in range(nbCluster):
            pca = sklearnPCA(n_components=2) # 2-dimensional PCA
            X = pd.DataFrame(pca.fit_transform(X))
            X = np.asarray(X)
            plt.scatter(X[labelsPredicted == i, 0], X[labelsPredicted == i, 1], c=colors[i],\
                        marker=markers[i], label='Cluster ' + str(i + 1))

        if annotate:
            for i in range(len(data)):
                plt.annotate(str(i+1), (X[0][i], X[1][i]))
    
        plt.legend()
        plt.grid()
        plt.title(title)
        #pickle.dump(fig,open(figPath,'wb')) # Python's format
        #plt.show()
        plt.savefig(figDir+figName, dpi=100)
        plt.clf() # Otherwise all figures are written on one another

    for i in range(0, len(names)):
        print(str(names[i]) + ': ' + str(labelsPredicted[i]))


def parsingCommandsClustering():
    '''
        Creation of an ArgumentParser object, holding all the information necessary to parse
        the command line into Python data types.

        -------
        Returns:
        - ArgumentParser such as:
          * jsDirs=args['d'],
          * jsFiles=args['f'],
          * labels=args['l'],
          * parser=args['p'][0],
          * n=args['n'][0],
          * separator=args['s'][0],
          * updateDico=args['u'][0],
          * histo=args['h'][0],
          * fileProd=args['e'][0],
          * pcaProd=args['g'][0],
          * pathHisto=args['hp'][0],
          * pathFile=args['ep'][0],
          * pathPca=args['gp'][0]
          A more thorough description can be obtained:
            >$ python3 <path-of-src/StaticAnalysis.py> -help
    '''

    parser = argparse.ArgumentParser(description='GGGiven a list of repositories or files paths,\
    analyse whether the JS files are either benign or malicious.')

    parser.add_argument('--f', metavar='FILE', type=str, nargs='+', help='files to be analysed')
    parser.add_argument('--d', metavar='DIR', type=str, nargs='+', help='directories containing\
    the JS files to be analysed')
    parser.add_argument('--p', metavar='PARSER', type=str, nargs=1, choices=['esprimaAst',\
                        'esprimaAstSimp', 'esprima', 'slimIt'], default=['esprimaAstSimp'],\
                    help='parser\'s name')
    parser.add_argument('--n', metavar='INTEGER', type=int, nargs=1, default=[4],\
                    help='stands for the size of the sliding-window which goes through\
                    the previous list')
    parser.add_argument('--c', metavar='INTEGER', type=int, nargs=1, help='number of clusters')
    parser.add_argument('--g', metavar='BOOL', type=bool, nargs=1, default=[False],\
                    help='produce a graphical 2D representation of the files from the JS corpus')

    args = vars(parser.parse_args())

    return args


argObjC = parsingCommandsClustering()


def mainC(jsDirs=argObjC['d'], jsFiles=argObjC['f'], parser=argObjC['p'][0], n=argObjC['n'][0],
         nbCluster=argObjC['c'][0], displayFig=argObjC['g'][0]):
    
    if jsDirs is None and jsFiles is None:
        print('Please, indicate a directory or a JS file to be studied')

    else:
        csvFile = StaticAnalysisJs.mainS(jsDirs=jsDirs, jsFiles=jsFiles,\
                                        parser=parser, n=n)
        print(csvFile)
        
        clustering(csvFile, nbCluster=nbCluster, displayFig=displayFig)


if __name__ == "__main__": # Executed only if run as a script
    mainC()
    
 