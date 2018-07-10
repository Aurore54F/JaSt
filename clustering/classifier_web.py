
"""
    Main module to classify HTML pages (based on an analysis of their JS snippets)
    using a given model.
"""

import os
import logging

import utility
import classifier
import static_analysis


def classify_websites(js_dir, model, dict_not_hash=True, tolerance='false', n=4, threshold=0.29):
    """
        Test of a classification model to detect malicious web pages.
        A web page is defined as malicious if at least one of its JS snippet is malicious.
        Otherwise it is labeled as benign.

        -------
        Parameters:
        - js_dirs: str
            Directory containing directories representing the web pages to be analysed
            (the JS snippets of the page considered are stored in the corresponding subdirectory).
        - model: str
            Path to the model used to classify the new files.
         dict_not_hash: Boolean
            True if a dictionary is used to map n-grams to int, False if hashes are used.
            Default: True.
        - tolerance: str
            Indicates whether esprima should tolerate a few cases of syntax errors
            (corresponds to esprima's tolerant option). Default: 'false'.
            The values 'true' and 'false' shall be used to enable this tolerant mode.
        - n: Integer
            Stands for the size of the sliding-window which goes through the units contained in the
            files to be analysed. Default: 4.
        - threshold: int
            Threshold over which all samples are considered malicious. Default: 0.29.
    """

    len_malicious = 0
    len_benign = 0

    res_names = []
    res_predict = []

    for html in os.listdir(js_dir):
        html = os.path.join(js_dir, html)

        names, attributes, labels = static_analysis.main_analysis \
            (js_dirs=[html], labels_dirs=None, js_files=None, labels_files=None,
             tolerance=tolerance, n=n, dict_not_hash=dict_not_hash)

        # Uncomment to save the analysis results in pickle objects.
        """
        utility.save_analysis_results(os.path.join(html, "Analysis-n" + str(n) + "-dict"
                                                   + str(dict_not_hash)), names, attributes, labels)
        """

        try:
            labels_predicted_test = classifier.test_model(names, labels, attributes, model,
                                                          print_res=False, print_score=False,
                                                          threshold=threshold)
            if 'malicious' in labels_predicted_test:
                len_malicious += len(names)
                res_names.append(html)
                res_predict.append('malicious')
            else:
                len_benign += len(names)
                res_names.append(html)
                res_predict.append('benign')

        except ValueError:
            logging.exception('No valid JS files could be found in ' + html)
            # shutil.rmtree(html)

    utility.get_classification_results(res_names, res_predict)

    print('Recognised as malicious: ' + str(len([i for i in res_predict if i == 'malicious']))
          + ' Total size: ' + str(len_malicious) + ' scripts')
    print('Recognised as benign: ' + str(len([i for i in res_predict if i == 'benign']))
          + ' Total size: ' + str(len_benign) + ' scripts')
