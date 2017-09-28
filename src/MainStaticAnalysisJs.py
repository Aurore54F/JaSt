
'''
    Main module to launch the analysis of JS files.
'''

import StaticAnalysisJs

if __name__ == "__main__": # Executed only if run as a script
    argObj = StaticAnalysisJs.parsingCommands()
    StaticAnalysisJs.mainS(jsDirs=argObj['d'], jsFiles=argObj['f'], labels=argObj['l'],\
    parser=argObj['p'][0], n=argObj['n'][0], sep=argObj['s'][0], updateDico=argObj['u'][0],\
    histo=argObj['h'][0], fileProd=argObj['e'][0], pcaProd=argObj['g'][0],\
    pathHisto=argObj['hp'][0], pathFile=argObj['ep'][0], pathPca=argObj['gp'][0])

