import collections

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

    dicc = collections.OrderedDict(sorted(dicc.items()))
    keys = dicc.keys()
    
    if (len(keys) == 0):
        error = 'NO DATA IN DICC'
        file.write(error+'\n')
        print error
    else:
        firstKey = keys[0]
        attributes = dicc[firstKey].keys()
        attributes.remove('place')
        for att in attributes:
            print type(dicc[firstKey][att])
            if isinstance(dicc[firstKey][att], float):
                file.write('@ATTRIBUTE '+att+' NUMERIC'+'\n')
            else:
                file.write('@ATTRIBUTE '+att+' STRING'+'\n')
                
        file.write('@ATTRIBUTE place {bsas, cba}'+'\n')
        file.write('\n')

    #Data:
    #================================================
        file.write('@DATA'+'\n')
            
        for k in keys:
            attributes = dicc[k].keys()
            attributes.remove('place')
            for att in attributes:
                file.write(str(dicc[k][att]))
                file.write(',')
            file.write(str(dicc[k]['place']))
            file.write('\n')

    file.close()