
# DRAFT
# TODO, comments, reorganise and improve functionalities + remove code duplicate

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle # to save figure to disk

from sklearn.decomposition import PCA as sklearnPCA
from sklearn.cluster import KMeans

#from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.datasets.samples_generator import make_blobs

#from pandas.tools.plotting import parallel_coordinates


def nbClusters(file, figPath = '', minA = 1, maxA = 5, epsilon = 1):
    
    data = pd.read_csv(file)
    fig = plt.figure()
        
    #y = data['Label']      # Split off classifications
    X = data.ix[:, '0':]  # Split off features
    
    #X, y = make_blobs(n_samples = 150, n_features = 30, centers = 3, cluster_std = 0.5, shuffle = True, random_state = 0)
    distorsions = []
    for i in range (minA, maxA+1):
        kmeans = KMeans(n_clusters = i, init = 'k-means++', n_init = 10, max_iter = 300, random_state = 0)
        kmeans.fit(X)
        distorsions.append(kmeans.inertia_)
    
    plt.plot(range(minA,maxA+1), distorsions, marker = 'x')
    plt.grid()
    plt.xlabel('Number of clusters')
    plt.ylabel('Total squared distance inside clusters')
    #pickle.dump(fig,open(figPath,'wb'))
    #plt.show()
    plt.savefig(figPath, dpi = 100)
    plt.clf() # Otherwise all figures are written on one another

    
    
def clustering(nbCluster = 4, file ='', figPath = ''):
    
    fig = plt.figure()
    data = pd.read_csv(file)
    
    names = data['Outlook']    
    #labels = data['Label']      # Split off classifications
    X = data.ix[:, '0':]  # Split off features
    X = np.asarray(X)
    
    #X, y = make_blobs(n_samples = 150, n_features = 30, centers = 3, cluster_std = 0.5, shuffle = True, random_state = 0)
        
    km = KMeans(n_clusters = nbCluster, init = 'k-means++', n_init = 10, max_iter = 300, tol = 1e-04, random_state = 0)
    labelsPredicted = km.fit_predict(X)
    #labels = km.labels_ # y_km
    # n_init: with 10 different centroids, little SSE
    
    colors = ['orange', 'lightblue', 'red', 'lightgreen', 'lightpink', 'darkgoldenrod', 'deepskyblue', 'seagreen', 'darkslateblue', 'gainsboro', 'khaki', 'slategray', 'darkcyan', 'darkslategrey', 'lawngreen', 'deeppink', 'thistle', 'sandybrown', 'mediumorchid', 'orangered', 'paleturquoise', 'coral', 'navy', 'slateblue', 'rebeccapurple', 'darkslategray', 'limegreen', 'magenta', 'skyblue', 'forestgreen', 'blue', 'lavender', 'mediumslateblue', 'aqua', 'mediumvioletred', 'lightsteelblue', 'cyan', 'mistyrose', 'darkorchid', 'gold', 'chartreuse', 'bisque', 'olive', 'darkmagenta', 'darkviolet', 'lightgrey', 'mediumblue', 'indigo', 'papayawhip', 'powderblue', 'aquamarine', 'wheat', 'hotpink', 'mediumseagreen', 'royalblue', 'pink', 'mediumaquamarine', 'goldenrod', 'peachpuff', 'darkkhaki', 'silver', 'mediumspringgreen', 'yellowgreen', 'cadetblue', 'olivedrab', 'darkgray', 'chocolate', 'palegoldenrod', 'darkred', 'peru', 'fuchsia', 'darkturquoise', 'cornsilk', 'lightgoldenrodyellow', 'lightslategray', 'dimgray', 'white', 'sienna', 'orchid', 'darkorange', 'darkseagreen', 'steelblue', 'darkgreen', 'violet', 'slategrey', 'lightsalmon', 'palegreen', 'yellow', 'lemonchiffon', 'antiquewhite', 'green', 'lightslategrey', 'tan', 'honeydew', 'whitesmoke', 'blueviolet', 'navajowhite', 'darkblue', 'mediumturquoise', 'dodgerblue', 'lightskyblue', 'crimson', 'snow', 'brown', 'indianred', 'palevioletred', 'plum', 'linen', 'cornflowerblue', 'saddlebrown', 'springgreen', 'lightseagreen', 'greenyellow', 'ghostwhite', 'rosybrown', 'darkgrey', 'grey', 'lime', 'teal', 'gray', 'mediumpurple', 'darkolivegreen', 'burlywood', 'tomato', 'lightcoral', 'purple', 'salmon', 'darksalmon', 'dimgrey', 'moccasin', 'maroon', 'ivory', 'turquoise', 'firebrick']
    markers = ['s', 'v', 'o', 'd', 'p', '^', '<', '>', '1', '2', '3', '4', '8', 'h', '.', 'H', '+', 'x', 'D', '|', '_', 's', 'v', 'o', 'd', 'p', '^', '<', '>', '1', '2', '3', '4', '8', 'h', '.', 'H', '+', 'x', 'D', '|', '_']
    
    
    for i in range(nbCluster):
        pca = sklearnPCA(n_components=2) #2-dimensional PCA
        X = pd.DataFrame(pca.fit_transform(X))
        X = np.asarray(X)
        #centers = pd.DataFrame(pca.fit_transform(km.cluster_centers_))
        #centers = np.asarray(centers)
        #plt.scatter(X[y_km == i,0], X[y_km == i,1], facecolors='none', edgecolors = colors[i], marker = markers[i], label = 'Cluster ' + str(i + 1))
        plt.scatter(X[labelsPredicted == i,0], X[labelsPredicted == i,1], c = colors[i], marker = markers[i], label = 'Cluster ' + str(i + 1))
        
        #plt.scatter(centers[:,0], centers[:,1], c = 'black', marker = '*', label = 'Cendroid')
    
    for i in range(0, len(names)):
        print(str(names[i]) + ': ' + str(labelsPredicted[i]))
    
    
    plt.legend()
    plt.grid()
    #pickle.dump(fig,open(figPath,'wb'))
    #plt.show()
    plt.savefig(figPath, dpi = 100)
    plt.clf() # Otherwise all figures are written on one another
 