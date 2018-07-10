# JaSt - JS AST-Based Analysis

This repository contains the code for the [DIMVA'18 paper: "JaSt: Fully Syntactic Detection of Malicious (Obfuscated) JavaScript"](https://swag.cispa.saarland/papers/fass2018jast.pdf).  
Please note that in its current state, the code is a Poc and not a fully-fledged production-ready API.


## Features
Our implementation, which aims at detecting malicious JavaScript samples, is divided into several packages with distinct functionalities:
  - *js* for the detection of valid JavaScript code;
  - *features* for the extraction of specific features from JavaScript inputs;
  - *clustering* for the classification and clustering of JavaScript documents.

### JavaScript Detection Tool
Detection of JavaScript samples respecting the grammar defined by [ECMA-International](http://www.ecma-international.org/ecma-262/8.0/), detection of broken JavaScript, and files not written in JavaScript.   
To use this tool: *python3 \<path-of-js/is_js.py\> --help*.

### Classification and Clustering of JavaScript Inputs
An AST-based analysis of JavaScript samples can be performed. This study is based on a frequency analysis of the n-grams present in the considered files.

- Detection of malicious JavaScript documents.   
To use this tool:  
1) *python3 \<path-of-clustering/learner.py\> --help*;  
2) *python3 \<path-of-clustering/updater.py\> --help*;  
3) *python3 \<path-of-clustering/classifier.py\> --help*.

- Clustering of JavaScript samples into *k* (configurable) families.   
To use this tool: *python3 \<path-of-clustering/cluster.py\> --help*.


## How to use it?
  - The system requirements are given in *install.sh*;
  - To launch the main function of a package, see the previous Section *Features*;
  - Application examples of our modules are given in *examples.pdf*;
  - The complete documentation can be consulted using Python's build-in function *help(\<name-of-the-module\>)*, or can be generated in HTML format with pydoc: *python3 \<path-of-pydoc\> -w \<name-of-the-module\>*.


## Cite this work
If you use JaSt for academic research, you are highly encouraged to cite the following [paper](https://swag.cispa.saarland/papers/fass2018jast.pdf):
```
@inproceedings{fass2018jast,
    author="Fass, Aurore and Krawczyk, Robert P. and Backes, Michael and Stock, Ben",
    title="{\textsc{JaSt}: Fully Syntactic Detection of Malicious (Obfuscated) JavaScript}",
    booktitle="Proceedings of the International Conference on Detection of Intrusions and Malware, and Vulnerability Assessment~(DIMVA)",
    year="2018"
}
```

### Abstract:

JavaScript is a browser scripting language initially created to enhance the interactivity of web sites and to improve their user-friendliness. However, as it offloads the work to the user's browser, it can be used to engage in malicious activities such as Crypto Mining, Drive-by Download attacks, or redirections to web sites hosting malicious software. Given the prevalence of such nefarious scripts, the anti-virus industry has increased the focus on their detection. The attackers, in turn, make increasing use of obfuscation techniques, so as to hinder analysis and the creation of corresponding signatures. Yet these malicious samples share syntactic similarities at an abstract level, which enables to bypass obfuscation and detect even unknown malware variants.

In this paper, we present JaSt, a low-overhead solution that combines the extraction of features from the abstract syntax tree with a random forest classifier to detect malicious JavaScript instances. It is based on a frequency analysis of specific patterns, which are either predictive of benign or of malicious samples. Even though the analysis is entirely static, it yields a high detection accuracy of almost 99.5% and has a low false-negative rate of 0.54%.


## Disclaimer

Die von dem Benutzer auf GitHub bereitgestellten Inhalte spiegeln nicht die 
Meinung des BSI wider.  
Die Verwendung der bereitgestellten Inhalte geschieht auf eigene Gefahr des 
Anwenders. Eine Haftung für die Richtigkeit, Vollständigkeit und Aktualität 
dieser Inhalte kann seitens des BSI nicht übernommen werden.  
Das BSI ist nicht verantwortlich und übernimmt keinerlei Haftung für Schäden, 
unter anderem für direkte, indirekte, zufällige, vorab konkret zu bestimmende 
oder Folgeschäden, die angeblich durch die Verwendung der Inhalte aufgetreten 
sind.



## External tools
[Esprima](http://esprima.org/), created and maintained by Ariya Hidayat has been used to perform both lexical and syntactic analysis of JavaScript files.
  
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
