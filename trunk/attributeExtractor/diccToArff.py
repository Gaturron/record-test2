
title = 'Buenos Aires - Cordoba Extraction Database'
sources = 'http://fabula2.exp.dc.uba.ar/'
author = 'Fernando Bugni'
databaseName = 'bsas-cba_DB'

def diccToArff(dicc, filename):

    file = open(filename, 'w')

    #Header:
    #================================================
    file.writeln('% 1. Title: '+title)
    file.writeln('%')
    file.writeln('% 2. Sources: '+sources)
    file.writeln('%')
    file.writeln('% 3. Author: '+author)
    file.writeln('%')
    #file.writeln('% 4. Date: '+date)
    file.writeln('%')

    file.writeln('@RELATION '+databaseName)

    keys = dicc.keys()
    print keys
    
    if (len(keys) == 0):
        error = 'NO DATA IN DICC'
        file.writeln(error)
        print error
    else:
        firstKey = keys[0]
        attributes = dicc[firstKey].keys()
        for att in attributes:
            file.writeln('@ATTRIBUTE '+att+' NUMERIC')
        
        file.writeln('@ATTRIBUTE place {buenos-aires, cordoba}')

    #Data:
    #================================================
        file.writeln('@DATA')
            
    #    for k in keys:
    #        for att in k.keys():
    #            file.writeln(k[att])
    #            file.writeln(',')
    #        file.writeln('\n')

    file.close()