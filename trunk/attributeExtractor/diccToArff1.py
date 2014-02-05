import collections
import time
import numpy as np
import arff

title = 'Buenos Aires - Cordoba Extraction Database'
sources = 'http://fabula2.exp.dc.uba.ar/'
author = 'Fernando Bugni'
databaseName = 'bsas-cba_DB'

def diccToArff(dicc, filename, attributesFilter):

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
                attributes += [ (key+'_'+str(i), attributesFilter[key][0])for i in range(len(attributesFilter[key]))]
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

        #fabrico el arff y escribo
        string = arff.dumps(datalist)

        file = open(filename, 'w')
        file.write('% 1. Title: '+title+'\n')
        file.write('%'+'\n')
        file.write('% 2. Sources: '+sources+'\n')
        file.write('%'+'\n')
        file.write('% 3. Author: '+author+'\n')
        file.write('%'+'\n')
        file.write('% 4. Date: '+time.strftime("%c")+'\n')
        file.write('%'+'\n\n')
        file.write(string)
        file.close()