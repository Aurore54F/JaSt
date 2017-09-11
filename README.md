# MalwareClustering

#### Objective
Static analysis (lexical or syntactical) of JavaScript samples to detect malicious executables. This implementation also enables a classification of JavaScript documents into several families.



#### Features
  - Detection of JavaScript samples respecting the grammar defined by ECMA-International <http://www.ecma-international.org/ecma-262/8.0/>, detection of broken JavaScript, and files not written in JavaScript;
  - Static analysis (lexical or syntactical) of JavaScript executables, based on a frequency analysis of their 4-grams;
  - Detection of valid malicious JavaScript documents;
  - Clustering of valid JavaScript samples into k families.


#### Additional implementations
  - 4 choices of tools to perform a static analysis: the tokenizers Esprima or SlimIt, and the parsers Esprima or our simplified version (with fewer syntactical units);
  - Possibility to train naive Bayes multinomial classifier on a data set, to add a validation and a test sets;
  - Implementation of k-fold cross-validation and possibility to plot ROC curves;
  - Manual clustering with histograms representing the frequency of all 4-grams present in a JavaScript document;
  - Graphical method to get an approximation of the number of clusters present in the data;
  - PCA implementation to graphically represent JavaScript executables onto a two-dimensional surface. With supervised learning, different colours can be attributed to each class or cluster.
