#!/bin/bash

sudo apt-get install python3
sudo apt install python3-pip
pip3 install slimit # min pip 7
sudo apt-get install python3-matplotlib
pip3 install plotly
pip3 install numpy

sudo apt install nodejs
sudo apt-get install nodejs-legacy
sudo apt install npm # Did not work on Debian testing
npm install esprima

sudo apt-get install cluster3
sudo apt-get install weka
# Get jar files for weka and TreeView

#file '/home/aurore/Documents/Code/MalwareClustering/src/slimitMatrix.txt' 
#less -S '/home/aurore/Documents/Code/MalwareClustering/src/slimitMatrix.txt' 
#wc '/home/aurore/Documents/Code/MalwareClustering/src/slimitMatrix.txt' 
#cut -c1-100 '/home/aurore/Documents/Code/MalwareClustering/src/slimitMatrix.txt' 

java -Xmx12g -jar weka.jar
java -jar TreeView.jar 
