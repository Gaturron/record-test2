
title = 'Buenos Aires - Cordoba Extraction Database'
sources = 'http://fabula2.exp.dc.uba.ar/'
author = 'Fernando Bugni'
databaseName = 'bsas-cba_DB'

def diccToArff(dicc, filename):

    file = open(filename, 'w')

    #Header:
    #================================================
    file.write('% 1. Title: '+title+'\n')
    file.write('%'+'\n')
    file.write('% 2. Sources: '+sources+'\n')
    file.write('%'+'\n')
    file.write('% 3. Author: '+author+'\n')
    file.write('%'+'\n')
    #file.write('% 4. Date: '+date+'\n')
    file.write('%'+'\n\n')

    file.write('@RELATION '+databaseName+'\n')

    keys = dicc.keys()
    
    if (len(keys) == 0):
        error = 'NO DATA IN DICC'
        file.write(error+'\n')
        print error
    else:
        firstKey = keys[0]
        attributes = dicc[firstKey].keys()
        for att in attributes:
            file.write('@ATTRIBUTE '+att+' NUMERIC'+'\n')
        
        #file.write('@ATTRIBUTE place {buenos-aires, cordoba}'+'\n')
        file.write('\n')

    #Data:
    #================================================
        file.write('@DATA'+'\n')
            
        for k in keys:
            for att in dicc[k].keys():
                file.write(str(dicc[k][att]))
                file.write(',')
            file.write('\n')

    file.close()