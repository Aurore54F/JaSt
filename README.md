# MalwareClustering


### Objective
Static analysis (lexical or syntactical) of JavaScript samples to detect malicious executables. This implementation also enables a classification of JavaScript documents into several families.


### Features
Our implementation is divided into three packages with distinct functionalities:
  - *JsDetection* for the detection of JavaScript code;
  - *src* for a static analysis of JavaScript code;
  - *MachineLearning* for the clustering or classification of JavaScript documents.

#### JavaScript Detection Tool
Detection of JavaScript samples respecting the grammar defined by [ECMA-International](http://www.ecma-international.org/ecma-262/8.0/), detection of broken JavaScript, and files not written in JavaScript.   
To use this tool: *python3 <path-of-JsDetection/JsDetection.py> --help*.

#### Static Analysis of JavaScript Executables
Both lexical and syntactical analysis of JavaScript samples can be performed. This study is based on a frequency analysis of the 4-grams present in the considered files.   
To use this tool: *python3 <path-of-src/MainStaticAnalysisJs.py> --help*.

#### Classification and Clustering of JavaScript Executables
- Detection of malicious JavaScript documents.   
To use this tool: *python3 <path-of-MachineLearning/Classification.py> -help*.

- Clustering of JavaScript samples into *k* (configurable) families.   
To use this tool: *python3 <path-of-MachineLearning/Clustering.py> --help*.


### Additional implementations
  - 4 choices of tools to perform a static analysis: the tokenizers Esprima or SlimIt, and the parsers Esprima or our simplified version (with fewer syntactical units);
  - Possibility to train naive Bayes multinomial classifier on a data set, to add a validation and a test sets;
  - Implementation of k-fold cross-validation and possibility to plot ROC curves;
  - Manual clustering with histograms representing the frequency of all 4-grams present in a JavaScript document;
  - Graphical method to get an approximation of the number of clusters present in the data;
  - PCA implementation to graphically represent JavaScript executables onto a two-dimensional surface. With supervised learning, different colours can be attributed to each class or cluster.


### How to use it?
  - The system requirements are given in *install.sh*;
  - To launch the main function of a package, see the previous Section *Features*;
  - The complete documentation can consulted using Python's build-in function *help(\<name-of-the-module>)*, or can be generated in HTML format with pydoc: *python3 \<path-of-pydoc> -w \<name-of-the-module>*.


### External tools
[Esprima](http://esprima.org/), created and maintained by Ariya Hidayat has been used to perform both lexical and syntactical analysis of JavaScript files.
  
"Copyright JS Foundation and other contributors, https://js.foundation/

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
