
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.decomposition import PCA as sklearnPCA
from sklearn.cluster import KMeans

#from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
#from sklearn.datasets.samples_generator import make_blobs

#from pandas.tools.plotting import parallel_coordinates


fileEsp = '/home/aurore/Documents/Code/JS-samples2-malicious/Weka-4clusters/esprima.csv';
fileEspAST = '/home/aurore/Documents/Code/JS-samples2-malicious/Weka-4clusters/esprimaAst.csv';
fileSlimIt = '/home/aurore/Documents/Code/JS-samples2-malicious/Weka-4clusters/slimIt.csv';

file = '/home/aurore/Documents/Code/MatrixFiles/esprima.csv';

data = pd.read_csv(file);

y = data['Label']      # Split off classifications
X = data.ix[:, '0':];  # Split off features


distorsions = [];
for i in range (1, 200):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', n_init = 10, max_iter = 300, random_state = 0);
    kmeans.fit(X);
    distorsions.append(kmeans.inertia_)

plt.plot(range(1,200), distorsions, marker = 'x');
plt.show();