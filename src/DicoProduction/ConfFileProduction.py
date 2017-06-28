
import os # To create repositories


# Storage of the dictionary in a configuration file

def dicoStorage(directoryName, fileName, description, orderedDico):
	
	if not os.path.exists(directoryName):
		os.makedirs(directoryName);
	
	dicoFile = open(directoryName + '/' + fileName,'w');
	dicoFile.write(description);
	for el in orderedDico:
		dicoFile.write("\t'" + str(el) + "'" + ' : ' + str(orderedDico[el]) + ', \n');
	dicoFile.write('}');
	dicoFile.close();
	


def prettyPrintDico(dico):
	'''
		Print a human-readable content of a dictionary.
		-------
		Parameter:
		- dico: Dictionary
	'''
	
	print('================================');
	for el in dico:
		print(str(el) + '\t : ' + str(dico[el]) + '\n');
	print('================================');