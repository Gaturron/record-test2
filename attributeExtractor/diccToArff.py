import collections

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
        diccAttFilter = collections.OrderedDict(sorted(attributesFilter.items()))
        attFilterKeys = diccAttFilter.keys()
        attFilterKeys.remove('place')
        for att in attFilterKeys:
            file.write('@ATTRIBUTE '+att+' '+diccAttFilter[att]+'\n')
        file.write('@ATTRIBUTE place {bsas, cba}'+'\n')
        file.write('\n')
        
        # firstKey = keys[0]
        # attributes = dicc[firstKey].keys()
        # attributes.remove('place')
        # for att in attributes:
        #     print type(dicc[firstKey][att])
        #     if isinstance(dicc[firstKey][att], float):
        #         file.write('@ATTRIBUTE '+att+' NUMERIC'+'\n')
        #     else:
        #         file.write('@ATTRIBUTE '+att+' STRING'+'\n')
                
        # file.write('@ATTRIBUTE place {bsas, cba}'+'\n')
        # file.write('\n')

    #Data:
    #================================================
        file.write('@DATA'+'\n')
            
        for k in keys:
            sampleDicc = collections.OrderedDict(sorted(dicc[k].items()))
            attributes = sampleDicc.keys()
            attributes.remove('place')
            for att in attributes:
                file.write(str(sampleDicc[att]))
                file.write(',')
            file.write(str(sampleDicc['place']))
            file.write('\n')

    file.close()