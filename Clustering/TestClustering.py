
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.decomposition import PCA as sklearnPCA
from sklearn.cluster import KMeans

#from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
#from sklearn.datasets.samples_generator import make_blobs

#from pandas.tools.plotting import parallel_coordinates


'''
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

'''


fileEsp = '/home/aurore/Documents/Code/JS-samples2-malicious/Weka-4clusters/esprima.csv';
fileEspAst = '/home/aurore/Documents/Code/JS-samples2-malicious/Weka-4clusters/esprimaAst.csv';
fileSlimIt = '/home/aurore/Documents/Code/JS-samples2-malicious/Weka-4clusters/slimIt.csv';
fileEspAstSimp = '/home/aurore/Documents/Code/JS-samples2-malicious/Weka-4clusters/esprimaAstSimp.csv';

data = pd.read_csv(fileEsp);

y = data['Label']  # Split off classifications
X = data.ix[:, '0':];  # Split off features


pca = sklearnPCA(n_components=2); #2-dimensional PCA
X_norm = (X - X.min())/(X.max() - X.min());
transformed = pd.DataFrame(pca.fit_transform(X));

plt.scatter(transformed[y==1][0], transformed[y==1][1], label='Class 1', c='red')
plt.scatter(transformed[y==2][0], transformed[y==2][1], label='Class 2', c='blue')
plt.scatter(transformed[y==3][0], transformed[y==3][1], label='Class 3', c='lightgreen')
plt.scatter(transformed[y==4][0], transformed[y==4][1], label='Class 4', c='green')
plt.scatter(transformed[y==5][0], transformed[y==5][1], label='Class 5', c='purple')

for i in range(len(data)):
    plt.annotate(str(i+1), (transformed[0][i],transformed[1][i]));

#plt.scatter(transformed[:][0], transformed[:][1]);

plt.legend();
plt.grid();
plt.show()

#plt.savefig('/home/aurore/Documents/Code/JS-samples2-malicious/Esp.png', dpi = 100);
#plt.clf(); # Otherwise all figures are written on one another