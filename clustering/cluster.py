
"""
    Clustering JavaScript files into k (configurable) families.
"""

import os
import argparse  # To parse command line arguments
import logging
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import utility
import static_analysis


src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def nb_clusters(attributes, fig_dir=os.path.join(src_path, 'Clustering'),
                fig_name='NumberOfClusters.png', min_a=1, max_a=5):
    """
        Given an np.array of attributes respecting the structure defined in our module features/
        and containing a static analysis of JavaScript executables, display the evolution of the
        error rate (Total squared distance inside clusters) as the number of clusters increases.

        -------
        Parameters:
        - attributes: np.array
            Features of the data to cluster.
        - fig_dir: str
            Path to store the figure displaying the evolution of the error rate as the
            number of clusters increases.
            Default value being the folder JS-Analysis/Clustering/.
        - fig_name: str
            Name of the previous figure.
            Default value being 'NumberOfClusters.png'.
        - min_a: int
            Minimum number of cluster. Default value: 1.
        - max_a: int
            Maximum number of clusters. Default value: 5.

        -------
        Returns:
        - .png file
            Displaying the evolution of the error rate as the number of clusters increases
            (from min_a to max_a included).
    """

    try:
        # Directory to store the clustering related files
        if not os.path.exists(fig_dir):
            os.makedirs(fig_dir)

        '''
        X, y = make_blobs(n_samples = 150, n_features = 30, centers = 3, cluster_std = 0.5,\
        shuffle = True, random_state = 0) # Test with 3 clusters
        '''

        distorsions = []
        for i in range(min_a, max_a+1):
            kmeans = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=300, random_state=0)
            # n_init: with 10 different centroids, little SSE
            kmeans.fit(attributes)  # k-means++ algorithm
            distorsions.append(kmeans.inertia_)  # Total squared distance inside clusters

        plt.plot(range(min_a, max_a+1), distorsions, marker='x')
        plt.grid()
        plt.xlabel('Number of clusters')
        plt.ylabel('Total squared distance inside clusters')
        plt.savefig(os.path.join(fig_dir, fig_name), dpi=100)
        plt.clf()  # Otherwise all figures are written on one another

    except ValueError as error:
        logging.exception('Unable to produce more clusters than there is data available: '
                          + str(error))


def clustering(names, attributes, nb_cluster, fig_dir=os.path.join(src_path, 'Clustering'),
               fig_name='ClusteringPca.png', true_labels=None, display_fig=False, annotate=False,
               title='Projection of the n-grams frequency of JavaScript files'):
    """
        Given an np.array of attributes respecting the structure defined in our module features/
        and containing a static analysis of JavaScript executables, clusters the JavaScript
        documents in k families.

        -------
        Parameters:
        - names: list
            Name of the data files to cluster.
        - attributes: np.array
            Features of the data to cluster.
        - nb_cluster: int
            Number of clusters wished.
        - fig_dir: str
            Path to store the figure displaying the different clusters contained in the data (PCA).
            Default value being the folder JS-Analysis/Clustering/.
        - fig_name: str
            Name of the previous figure.
            Default value being 'ClusteringPca.png'.
        - true_labels: list
            True labels of the data to cluster.
        - display_fig: bool
            PCA projection of the PCA files studied, with several colours standing for
            several clusters. Default value: false.
        - annotate: bool
            Indicates whether each file, will be given a unique id on the fig. Default value: false.
        - title: str
            Title of the PCA figure.
            Default value: 'Projection of the 4-grams frequency of JavaScript files'

        -------
        Returns:
        - In stdout:
            List of the files studied with the associated cluster's number.
        - .png file (if display_fig is True):
            Displaying the repartition of the files studied on a plane.
    """

    try:
        # Directory to store the clustering related files
        if not os.path.exists(fig_dir):
            os.makedirs(fig_dir)

        km = KMeans(n_clusters=nb_cluster, init='k-means++', n_init=10, max_iter=300,
                    tol=1e-04, random_state=0)
        # n_init: with 10 different centroids, little SSE

        labels_predicted = km.fit_predict(attributes)  # Perform k-means++ algorithm
        # vectors attributes and predict the target values

        # Prints the clustering results
        utility.get_classification_results(names, labels_predicted)

        # PCA does not support sparse input. See TruncatedSVD for a possible alternative.
        if display_fig:
            if true_labels is not None and true_labels and all(isinstance(elt, int)
                                                               for elt in true_labels):
                labels_predicted = true_labels

            colors = ['orange', 'lightblue', 'red', 'lightgreen', 'lightpink', 'darkgoldenrod',
                      'deepskyblue', 'seagreen', 'darkslateblue', 'gainsboro', 'khaki', 'slategray',
                      'darkcyan', 'darkslategrey', 'lawngreen', 'deeppink', 'thistle', 'sandybrown',
                      'mediumorchid', 'orangered', 'paleturquoise', 'coral', 'navy', 'slateblue',
                      'rebeccapurple', 'darkslategray', 'limegreen', 'magenta', 'skyblue',
                      'forestgreen',
                      'blue', 'lavender', 'mediumslateblue', 'aqua', 'mediumvioletred',
                      'lightsteelblue',
                      'cyan', 'mistyrose', 'darkorchid', 'gold', 'chartreuse', 'bisque', 'olive',
                      'darkmagenta', 'darkviolet', 'lightgrey', 'mediumblue', 'indigo',
                      'papayawhip',
                      'powderblue', 'aquamarine', 'wheat', 'hotpink', 'mediumseagreen', 'royalblue',
                      'pink',
                      'mediumaquamarine', 'goldenrod', 'peachpuff', 'darkkhaki', 'silver',
                      'mediumspringgreen', 'yellowgreen', 'cadetblue', 'olivedrab', 'darkgray',
                      'chocolate',
                      'palegoldenrod', 'darkred', 'peru', 'fuchsia', 'darkturquoise', 'cornsilk',
                      'lightgoldenrodyellow', 'lightslategray', 'dimgray', 'white', 'sienna',
                      'orchid',
                      'darkorange', 'darkseagreen', 'steelblue', 'darkgreen', 'violet', 'slategrey',
                      'lightsalmon', 'palegreen', 'yellow', 'lemonchiffon', 'antiquewhite', 'green',
                      'lightslategrey', 'tan', 'honeydew', 'whitesmoke', 'blueviolet',
                      'navajowhite',
                      'darkblue', 'mediumturquoise', 'dodgerblue', 'lightskyblue', 'crimson',
                      'snow',
                      'brown', 'indianred', 'palevioletred', 'plum', 'linen', 'cornflowerblue',
                      'saddlebrown', 'springgreen', 'lightseagreen', 'greenyellow', 'ghostwhite',
                      'rosybrown', 'darkgrey', 'grey', 'lime', 'teal', 'gray', 'mediumpurple',
                      'darkolivegreen', 'burlywood', 'tomato', 'lightcoral', 'purple', 'salmon',
                      'darksalmon', 'dimgrey', 'moccasin', 'maroon', 'ivory', 'turquoise',
                      'firebrick']
            markers = ['s', 'v', 'o', 'd', 'p', '^', '<', '>', '1', '2', '3', '4', '8', 'h', '.',
                       'H',
                       '+',
                       'x', 'D', '|', '_', 's', 'v', 'o', 'd', 'p', '^', '<', '>', '1', '2', '3',
                       '4',
                       '8',
                       'h', '.', 'H', '+', 'x', 'D', '|', '_']
            # Different markers and colours for legibility reasons
            for i in range(nb_cluster):
                pca = PCA(n_components=2)  # 2-dimensional PCA
                attributes = pd.DataFrame(pca.fit_transform(attributes))
                attributes = np.asarray(attributes)
                plt.scatter(attributes[labels_predicted == i, 0],
                            attributes[labels_predicted == i, 1],
                            c=colors[i], marker=markers[i], label='Cluster ' + str(i))

            if annotate:
                for i in range(len(names)):
                    plt.annotate(str(i+1), (attributes[i][0], attributes[i][1]))

            plt.legend()
            plt.grid()
            plt.title(title)
            fig_path = os.path.join(fig_dir, fig_name)
            plt.savefig(fig_path, dpi=100)
            plt.clf()  # Otherwise all figures are written on one another
            logging.info('The graphical representation of the clusters has been successfully '
                         + 'stored in ' + fig_path)

    except ValueError as error:
        logging.exception('Unable to produce more clusters than there is data available: '
                          + str(error))


def parsing_commands_clustering():
    """
        Creation of an ArgumentParser object, holding all the information necessary to parse
        the command line into Python data types.

        -------
        Returns:
        - ArgumentParser such as:
          * js_dirs=args['d'],
          * js_files=args['f'],
          * tolerance=args['t'][0],
          * n=args['n'][0],
          * nb_cluster=args['c'][0],
          * display_fig=args['g'][0].
          A more thorough description can be obtained:
            >$ python3 <path-of-clustering/cluster.py> -help
    """

    parser = argparse.ArgumentParser(description='Given a list of repository or file paths,\
    clusters the JS inputs into several families.')

    parser.add_argument('--d', metavar='DIR', type=str, nargs='+',
                        help='directories containing the JS files to be clustered')
    parser.add_argument('--f', metavar='FILE', type=str, nargs='+', help='files to be analyzed')
    parser.add_argument('--c', metavar='INTEGER', type=int, nargs=1, help='number of clusters')
    parser.add_argument('--g', metavar='BOOL', type=bool, nargs=1, default=[False],
                        help='produces a 2D representation of the files from the JS corpus')
    utility.parsing_commands(parser)

    return vars(parser.parse_args())


arg_obj = parsing_commands_clustering()
utility.control_logger(arg_obj['v'][0])


def main_clustering(js_dirs=arg_obj['d'], js_files=arg_obj['f'], tolerance=arg_obj['t'][0],
                    nb_cluster=arg_obj['c'], n=arg_obj['n'][0], display_fig=arg_obj['g'][0],
                    dict_not_hash=arg_obj['dnh'][0]):
    """
        Main function, uses a static analysis (lexical or syntactical)
        of JavaScript files given in input to cluster them into k (configurable) families.

        -------
        Parameters:
        - js_dirs: list of strings
            Directories containing the JS files to be analysed.
        - js_files: list of strings
            Files to be analysed.
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option). Default value is 'false'.
            The value 'true' shall be used to enable this tolerant mode.
        - n: Integer
            Stands for the size of the sliding-window which goes through the units contained in the
            files to be analysed.
        - nb_cluster: int
            Number of clusters wished.
        - display_fig: bool
            Production of a 2D representation of the files from the JS corpus.
        - dict_not_hash: Boolean
            True if a dictionary is used to map n-grams to int, False if hashes are used.
        Default values are the ones given in the command lines or in the
        ArgumentParser object (function parsing_commands()).
    """

    if js_dirs is None and js_files is None:
        logging.error('Please, indicate a directory or a JS file to be analysed')

    elif nb_cluster is None:
        logging.error('Please, indicate a number of clusters')

    else:
        names, attributes, labels = static_analysis.main_analysis \
            (js_dirs=js_dirs, labels_dirs=None, js_files=js_files, labels_files=None,
             tolerance=tolerance, n=n, dict_not_hash=dict_not_hash)

        if names:
            # Uncomment to save the analysis results in pickle objects.
            """
            utility.save_analysis_results(os.path.join("Clustering", "Analysis-n" + str(n) + "-dict"
                                                       + str(dict_not_hash)),
                                          names, attributes, labels)
            """

            clustering(names=names, attributes=attributes, nb_cluster=nb_cluster[0],
                       display_fig=display_fig, true_labels=labels)

        else:
            logging.warning('No file found for the analysis.\n'
                            + '(see >$ python3 <path-of-js/is_js.py> -help)'
                            + ' to check your files correctness.\n'
                            + 'Otherwise they may not contain enough n-grams)')


if __name__ == "__main__":  # Executed only if run as a script
    main_clustering()
