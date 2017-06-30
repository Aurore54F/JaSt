
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.decomposition import PCA as sklearnPCA
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

#from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
#from sklearn.datasets.samples_generator import make_blobs

#from pandas.tools.plotting import parallel_coordinates


def nbClusters(file, figPath):

    data = pd.read_csv(file);
    
    y = data['Label']      # Split off classifications
    X = data.ix[:, '0':];  # Split off features
    
    distorsions = [];
    for i in range (1, 40):
        kmeans = KMeans(n_clusters = i, init = 'k-means++', n_init = 10, max_iter = 300, random_state = 0);
        kmeans.fit(X);
        distorsions.append(kmeans.inertia_)
    
    plt.plot(range(1,40), distorsions, marker = 'x');
    plt.grid();
    
    #plt.show();
    plt.savefig(figPath, dpi = 100);
    plt.clf(); # Otherwise all figures are written on one another
    
    
def clustering(nbCluster = 5, file ='', filePath = ''):
    
    
    data = pd.read_csv(file);
        
    y = data['Label']      # Split off classifications
    X = data.ix[:, '0':];  # Split off features
    X = np.asarray(X);
    
    #X, y = make_blobs(n_samples = 150, n_features = 30, centers = 3, cluster_std = 0.5, shuffle = True, random_state = 0);
        
    km = KMeans(n_clusters = nbCluster, init = 'k-means++', n_init = 10, max_iter = 300, tol = 1e-04, random_state = 0);
    y_km = km.fit_predict(X);
    labels = km.labels_;
    # n_init: with 10 different centroids, little SSE
    
    X1 = X[labels == 0, :];
    X2 = X[labels == 1, :];
    X3 = X[labels == 2, :];
    X4 = X[labels == 3, :];
    X5 = X[labels == 4, :];
        
    pca = sklearnPCA(n_components=2); #2-dimensional PCA
    X = pd.DataFrame(pca.fit_transform(X));
    X = np.asarray(X);
    X1 = pd.DataFrame(pca.fit_transform(X1));
    X2 = pd.DataFrame(pca.fit_transform(X2));
    X3 = pd.DataFrame(pca.fit_transform(X3));
    X4 = pd.DataFrame(pca.fit_transform(X4));
    #X5 = pd.DataFrame(pca.fit_transform(X5));
    
    #print(pca.get_covariance());
    #print(pca.get_precision());
    
    colors = ['orange', 'lightblue', 'red', 'lightgreen', 'lightpink', 'darkgoldenrod', 'deepskyblue', 'seagreen', 'darkslateblue', 'gainsboro', 'khaki', 'slategray', 'darkcyan', 'darkslategrey', 'lawngreen', 'deeppink', 'thistle', 'sandybrown', 'mediumorchid', 'orangered', 'paleturquoise', 'coral', 'navy', 'slateblue', 'rebeccapurple', 'darkslategray', 'limegreen', 'magenta', 'skyblue', 'forestgreen', 'blue', 'lavender', 'mediumslateblue', 'aqua', 'mediumvioletred', 'lightsteelblue', 'cyan', 'mistyrose', 'darkorchid', 'gold', 'chartreuse', 'bisque', 'olive', 'darkmagenta', 'darkviolet', 'lightgrey', 'mediumblue', 'indigo', 'papayawhip', 'powderblue', 'aquamarine', 'wheat', 'hotpink', 'mediumseagreen', 'royalblue', 'pink', 'mediumaquamarine', 'goldenrod', 'peachpuff', 'darkkhaki', 'silver', 'mediumspringgreen', 'yellowgreen', 'cadetblue', 'olivedrab', 'darkgray', 'chocolate', 'palegoldenrod', 'darkred', 'peru', 'fuchsia', 'darkturquoise', 'cornsilk', 'lightgoldenrodyellow', 'lightslategray', 'dimgray', 'white', 'sienna', 'orchid', 'darkorange', 'darkseagreen', 'steelblue', 'darkgreen', 'violet', 'slategrey', 'lightsalmon', 'palegreen', 'yellow', 'lemonchiffon', 'antiquewhite', 'green', 'lightslategrey', 'tan', 'honeydew', 'whitesmoke', 'blueviolet', 'navajowhite', 'darkblue', 'mediumturquoise', 'dodgerblue', 'lightskyblue', 'crimson', 'snow', 'brown', 'indianred', 'palevioletred', 'plum', 'linen', 'cornflowerblue', 'saddlebrown', 'springgreen', 'lightseagreen', 'greenyellow', 'ghostwhite', 'rosybrown', 'darkgrey', 'grey', 'lime', 'teal', 'gray', 'mediumpurple', 'darkolivegreen', 'burlywood', 'tomato', 'lightcoral', 'purple', 'salmon', 'darksalmon', 'dimgrey', 'moccasin', 'maroon', 'ivory', 'turquoise', 'firebrick'];
    markers = ['s', 'v', 'o', 'd', 'p', '^', '<', '>', '1', '2', '3', '4', '8', 'h', '.', 'H', '+', 'x', 'D', '|', '_', 's', 'v', 'o', 'd', 'p', '^', '<', '>', '1', '2', '3', '4', '8', 'h', '.', 'H', '+', 'x', 'D', '|', '_'];
    
    
    plt.scatter(X[y_km == 0,0], X[y_km == 0,1], c = 'orange', marker = 's', label = 'Cluster 1');
    plt.scatter(X[y_km == 1,0], X[y_km == 1,1], c = 'lightblue', marker = 'v', label = 'Cluster 2');
    plt.scatter(X[y_km == 2,0], X[y_km == 2,1], c = 'red', marker = 'o', label = 'Cluster 3');
    plt.scatter(X[y_km == 3,0], X[y_km == 3,1], c = 'lightgreen', marker = 'd', label = 'Cluster 4');
    plt.scatter(X[y_km == 4,0], X[y_km == 4,1], c = 'lightpink', marker = 'p', label = 'Cluster 5');
    '''
    
    plt.scatter(X1[0], X1[1], c = 'orange', marker = 's', label = 'Cluster 1');
    plt.scatter(X2[0], X2[1], c = 'lightblue', marker = 'v', label = 'Cluster 2');
    plt.scatter(X3[0], X3[1], c = 'red', marker = 'o', label = 'Cluster 3');
    plt.scatter(X4[0], X4[1], c = 'lightgreen', marker = 'd', label = 'Cluster 4');
    #plt.scatter(X5[0], X5[1], c = 'lightpink', marker = 'p', label = 'Cluster 5');
    '''
    
    '''
    for i in range(nbCluster):
        plt.scatter(X[y_km == i,0], X[y_km == i,1], c = colors[i], marker = markers[i], label = 'Cluster ' + str(i + 1));
    '''
    
    #plt.scatter(km.cluster_centers_[:,0], km.cluster_centers_[:,1], c = 'black', marker = '*', label = 'Cendroid');

    plt.legend();
    plt.grid();
    plt.show();

    

def prettyPrintClusters(file, figPath = '/home/aurore/Documents/Code/JS-samples2-malicious/esprima.png', nbClusters = 4, annotate = False):

    data = pd.read_csv(file);
    
    y = data['Label']  # Split off classifications
    X = data.ix[:, '0':];  # Split off features
    
    
    pca = sklearnPCA(n_components=2); #2-dimensional PCA
    X_norm = (X - X.min())/(X.max() - X.min());
    transformed = pd.DataFrame(pca.fit_transform(X));
    
    colors = ['red', 'blue', 'lightgreen', 'green', 'purple'];
    
    if nbClusters > 0:
        for i in range (nbClusters + 1):
            plt.scatter(transformed[y==i+1][0], transformed[y==i+1][1], label='Class ' + str(i+1), c = colors[i]);
    else:
        plt.scatter(transformed[:][0], transformed[:][1]);
   
    if annotate == True:
        for i in range(len(data)):
            plt.annotate(str(i+1), (transformed[0][i],transformed[1][i]));
    
    plt.legend();
    plt.grid();
    #plt.show()
    
    plt.savefig(figPath, dpi = 100);
    plt.clf(); # Otherwise all figures are written on one another