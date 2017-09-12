
# DRAFT
# TODO, comments, reorganise and improve functionalities + remove code duplicate

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import pickle # to save figure to disk

from sklearn.decomposition import PCA as sklearnPCA
from sklearn.cluster import KMeans

currentPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def nbClusters(dataFile, figDir=currentPath+'/Clustering/', figName='NumberOfClusters.png',\
               minA=1, maxA=5):
    
    # Directory to store the clustering related files
    if not os.path.exists(figDir):
        os.makedirs(figDir)
    
    data = pd.read_csv(dataFile)
    X = data.ix[:, '0':] # 2D vector containing all the attributes of the samples considered
    
    #X, y = make_blobs(n_samples = 150, n_features = 30, centers = 3, cluster_std = 0.5, shuffle = True, random_state = 0)
    distorsions = []
    for i in range (minA, maxA+1):
        kmeans = KMeans(n_clusters = i, init = 'k-means++', n_init = 10, max_iter = 300, random_state = 0)
        kmeans.fit(X)
        # k-means++ algorithm
        distorsions.append(kmeans.inertia_) # Total squared distance inside clusters
    
    plt.plot(range(minA,maxA+1), distorsions, marker = 'x')
    plt.grid()
    plt.xlabel('Number of clusters')
    plt.ylabel('Total squared distance inside clusters')
    #pickle.dump(fig,open(figPath,'wb')) # Python's format
    #plt.show()
    plt.savefig(figDir+figName, dpi = 100)
    plt.clf() # Otherwise all figures are written on one another

    
    
def clustering(dataFile, nbCluster=4, figDir=currentPath+'/Clustering/',\
               figName='ClusteringPca.png', title='Projection of the 4-grams frequency of\
               JavaScript files', annotate=False):

    # Directory to store the clustering related files
    if not os.path.exists(figDir):
        os.makedirs(figDir)

    data = pd.read_csv(dataFile)
    names = data['Outlook']
    X = data.ix[:, '0':] # 2D vector containing all the attributes of the samples considered
    X = np.asarray(X)
    
    km = KMeans(n_clusters = nbCluster, init = 'k-means++', n_init = 10, max_iter = 300, tol = 1e-04, random_state = 0)
    labelsPredicted = km.fit_predict(X)
    # n_init: with 10 different centroids, little SSE

    colors = ['orange', 'lightblue', 'red', 'lightgreen', 'lightpink', 'darkgoldenrod', 'deepskyblue', 'seagreen', 'darkslateblue', 'gainsboro', 'khaki', 'slategray', 'darkcyan', 'darkslategrey', 'lawngreen', 'deeppink', 'thistle', 'sandybrown', 'mediumorchid', 'orangered', 'paleturquoise', 'coral', 'navy', 'slateblue', 'rebeccapurple', 'darkslategray', 'limegreen', 'magenta', 'skyblue', 'forestgreen', 'blue', 'lavender', 'mediumslateblue', 'aqua', 'mediumvioletred', 'lightsteelblue', 'cyan', 'mistyrose', 'darkorchid', 'gold', 'chartreuse', 'bisque', 'olive', 'darkmagenta', 'darkviolet', 'lightgrey', 'mediumblue', 'indigo', 'papayawhip', 'powderblue', 'aquamarine', 'wheat', 'hotpink', 'mediumseagreen', 'royalblue', 'pink', 'mediumaquamarine', 'goldenrod', 'peachpuff', 'darkkhaki', 'silver', 'mediumspringgreen', 'yellowgreen', 'cadetblue', 'olivedrab', 'darkgray', 'chocolate', 'palegoldenrod', 'darkred', 'peru', 'fuchsia', 'darkturquoise', 'cornsilk', 'lightgoldenrodyellow', 'lightslategray', 'dimgray', 'white', 'sienna', 'orchid', 'darkorange', 'darkseagreen', 'steelblue', 'darkgreen', 'violet', 'slategrey', 'lightsalmon', 'palegreen', 'yellow', 'lemonchiffon', 'antiquewhite', 'green', 'lightslategrey', 'tan', 'honeydew', 'whitesmoke', 'blueviolet', 'navajowhite', 'darkblue', 'mediumturquoise', 'dodgerblue', 'lightskyblue', 'crimson', 'snow', 'brown', 'indianred', 'palevioletred', 'plum', 'linen', 'cornflowerblue', 'saddlebrown', 'springgreen', 'lightseagreen', 'greenyellow', 'ghostwhite', 'rosybrown', 'darkgrey', 'grey', 'lime', 'teal', 'gray', 'mediumpurple', 'darkolivegreen', 'burlywood', 'tomato', 'lightcoral', 'purple', 'salmon', 'darksalmon', 'dimgrey', 'moccasin', 'maroon', 'ivory', 'turquoise', 'firebrick']
    markers = ['s', 'v', 'o', 'd', 'p', '^', '<', '>', '1', '2', '3', '4', '8', 'h', '.', 'H', '+', 'x', 'D', '|', '_', 's', 'v', 'o', 'd', 'p', '^', '<', '>', '1', '2', '3', '4', '8', 'h', '.', 'H', '+', 'x', 'D', '|', '_']

    for i in range(nbCluster):
        pca = sklearnPCA(n_components=2) # 2-dimensional PCA
        X = pd.DataFrame(pca.fit_transform(X))
        X = np.asarray(X)
        plt.scatter(X[labelsPredicted == i,0], X[labelsPredicted == i,1], c = colors[i], marker = markers[i], label = 'Cluster ' + str(i + 1))
    
    if annotate is True:
        for i in range(len(data)):
            plt.annotate(str(i+1), (X[0][i], X[1][i]))

    for i in range(0, len(names)):
        print(str(names[i]) + ': ' + str(labelsPredicted[i]))

    plt.legend()
    plt.grid()
    plt.title(title)
    #pickle.dump(fig,open(figPath,'wb')) # Python's format
    #plt.show()
    plt.savefig(figDir+figName, dpi = 100)
    plt.clf() # Otherwise all figures are written on one another
 