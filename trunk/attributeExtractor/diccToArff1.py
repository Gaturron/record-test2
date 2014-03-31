import collections
import time
import numpy as np
import arff
import logging

title = 'Buenos Aires - Cordoba Extraction Database'
source = 'http://fabula2.exp.dc.uba.ar/'
author = 'Fernando Bugni'
databaseName = 'bsas-cba_DB'

def diccToArff(dicc, filename, attributesFilter):

    logger = logging.getLogger('Extract')

    orderedKeys = sorted(attributesFilter.keys())
    
    if (len(dicc.keys()) == 0):
        print 'NO DATA IN DICC'    	
    else:

        datalist = {}

        datalist['relation'] = databaseName

        # Preparo el encabezado
        attributes = []
        for key in orderedKeys:
            if  isinstance(attributesFilter[key], list):
                attributes += [ (key+'_'+str(i), nan_to_num(attributesFilter[key][0]))for i in range(len(attributesFilter[key]))]
            elif isinstance(attributesFilter[key], tuple):
                attributes.append((key, list( attributesFilter[key])))
            else:
                attributes.append((key, attributesFilter[key]))

        datalist['attributes'] = attributes

        # Preparo los datos
        data = []

        for sampleKey in dicc.keys():
            sample = dicc[sampleKey]
    
            samplelist = []
            for key in orderedKeys:
                if isinstance(sample[key], np.ndarray):
                    samplelist += sample[key].tolist() 
                else:
                    samplelist.append(sample[key])

            data += [ samplelist ]

        datalist['data'] = data
        logger.debug('\n\n\n\n\n data: '+str(datalist))

        #fabrico el arff y escribo
        string = arff.dumps(datalist)

        file = open(filename, 'w')
        file.write('% 1. Title: '+title+'\n')
        file.write('%'+'\n')
        file.write('% 2. Source: '+source+'\n')
        file.write('%'+'\n')
        file.write('% 3. Author: '+author+'\n')
        file.write('%'+'\n')
        file.write('% 4. Date: '+time.strftime("%c")+'\n')
        file.write('%'+'\n\n')
        file.write(string)
        file.close()