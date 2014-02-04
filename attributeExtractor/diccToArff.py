import collections
import time
import numpy as np

title = 'Buenos Aires - Cordoba Extraction Database'
sources = 'http://fabula2.exp.dc.uba.ar/'
author = 'Fernando Bugni'
databaseName = 'bsas-cba_DB'

def diccToArff(dicc, filename, attributesFilter):

    file = open(filename, 'w')

    #Header:
    #================================================
    file.write('% 1. Title: '+title+'\n')
    file.write('%'+'\n')
    file.write('% 2. Sources: '+sources+'\n')
    file.write('%'+'\n')
    file.write('% 3. Author: '+author+'\n')
    file.write('%'+'\n')
    file.write('% 4. Date: '+time.strftime("%c")+'\n')
    file.write('%'+'\n\n')

    file.write('@RELATION '+databaseName+'\n')

    dicc = collections.OrderedDict(sorted(dicc.items()))
    keys = dicc.keys()
    
    if (len(keys) == 0):
        error = 'NO DATA IN DICC'
        file.write(error+'\n')
        print error
    else:

        orderedKeys = sorted(attributesFilter.keys())
        orderedKeys.remove('place')
        
        for att in orderedKeys:
            if isinstance(attributesFilter[att], list):
                for i in range(len(att)):
                    file.write('@ATTRIBUTE '+str(att)+'_'+str(i)+' '+str(attributesFilter[att][0])+'\n')                    
            else:
                file.write('@ATTRIBUTE '+str(att)+' '+str(attributesFilter[att])+'\n')
        file.write('@ATTRIBUTE place {bsas, cba}'+'\n')
        file.write('\n')

    #Data:
    #================================================
        file.write('@DATA'+'\n')
            
        for k in keys:
            sampleDicc = dicc[k]

            for att in orderedKeys:
                
                print 'type: '+str(att)+' '+str(type(sampleDicc[att]).__name__)
                print 'isinstance: '+str(isinstance(sampleDicc[att], np.ndarray))

                if isinstance(sampleDicc[att], str) and ' ' in sampleDicc[att]:
                    file.write('\'')                    
                    file.write(str(sampleDicc[att]))
                    file.write('\'')
                
                if isinstance(sampleDicc[att], np.ndarray):
                    print 'hola' 
                    for i in sampleDicc[att]:
                        file.write(str(i))
                        file.write(', ')
                else:
                    file.write(str(sampleDicc[att]))
                
                file.write(', ')
            file.write(str(sampleDicc['place']))
            file.write('\n')

    file.close()