import alignmentFilter as agmntFilter
import diccToArff1 as dTA
from textgridExtractor import textgridExtractor
from acousticExtractor import acousticExtractor
import logging
import time
import os

import testGenerator as testGenerator

from sets import Set
from random import randint

Path = os.path.abspath(os.path.join(os.getcwd(), '..', '..'))+'/Prosodylab-Aligner-master/data1.complete/'
PathTests = os.path.abspath(os.getcwd())+'/tests'

logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=None)

def extract():

    mfcc_len = 13

    attributesFilter = {
        'place': ('bsas', 'cba'), 
        'phrases': 'STRING', 
        'duration': 'NUMERIC', 
        'userId': 'NUMERIC',
        'phraseId': 'NUMERIC',
        'attempt': 'NUMERIC',

        'PHO_kt_norm': 'NUMERIC', 
        'PHO_kt_normhd': 'NUMERIC',
        'PHO_ll_norm': 'NUMERIC', 
        'PHO_ll_normhd': 'NUMERIC', 
        'PHO_rr_norm': 'NUMERIC',  
        'PHO_rr_normhd': 'NUMERIC', 
        'PHO_sc_norm': 'NUMERIC',
        'PHO_sc_normhd': 'NUMERIC',
        'PHO_Sfinal_norm': 'NUMERIC',
        'PHO_Sfinal_normhd': 'NUMERIC',
        
        'PHO_phoneme': 'NUMERIC',
        'PHO_vowel_norm': 'NUMERIC', 
        'PHO_vowel_normhd': 'NUMERIC', 
        'PHO_consonant_norm': 'NUMERIC',
        'PHO_consonant_normhd': 'NUMERIC',
        
        'SIL_syllableAccent_norm': 'NUMERIC',
        'SIL_syllableAccent_normhd': 'NUMERIC',
        'SIL_prevSyllableAccent_norm': 'NUMERIC',
        'SIL_prevSyllableAccent_normhd': 'NUMERIC',
         
        'MFCC_AverageKT': ['NUMERIC' for i in range(mfcc_len)],
        'MFCC_MaxKT': ['NUMERIC' for i in range(mfcc_len)],
        'MFCC_MinKT': ['NUMERIC' for i in range(mfcc_len)],
        'MFCC_AverageLL': ['NUMERIC' for i in range(mfcc_len)],
        'MFCC_MaxLL': ['NUMERIC' for i in range(mfcc_len)],
        'MFCC_MinLL': ['NUMERIC' for i in range(mfcc_len)],
        'MFCC_AverageRR': ['NUMERIC' for i in range(mfcc_len)],
        'MFCC_MaxRR': ['NUMERIC' for i in range(mfcc_len)],
        'MFCC_MinRR': ['NUMERIC' for i in range(mfcc_len)],
        'MFCC_AverageSC': ['NUMERIC' for i in range(mfcc_len)],
        'MFCC_MaxSC': ['NUMERIC' for i in range(mfcc_len)],
        'MFCC_MinSC': ['NUMERIC' for i in range(mfcc_len)]
    }

    logger = logging.getLogger('Extract')
    logger.info('starting')

    pathList = agmntFilter.filter(Path)
    logger.debug('pathList: (tam. '+str(len(pathList))+') '+ str(pathList))

    tgExtractor = textgridExtractor(attributesFilter.keys())
    tgRes = tgExtractor.textgridsToAtt(pathList)
    #logger.debug('tgRes: '+ str(tgRes))

    acExtractor = acousticExtractor(attributesFilter.keys())
    acRes = acExtractor.extracts(pathList)
    #logger.debug('acRes: '+ str(acRes))

    res = {}
    for sample in tgRes.keys():
    	res[sample] = dict(tgRes[sample].items() + acRes[sample].items())
        #res[sample] = dict(tgRes[sample].items())

    res1 = {}
    for key in res.keys():
    	filename = key.split('/')[-1]
    	res[key]['place'] = filename.split('_')[0]
        res[key]['userId'] = filename.split('_')[1][1:]
        res[key]['phraseId'] = filename.split('_')[2][1:]
        res[key]['attempt'] = filename.split('_')[3][1:]
    	res1[filename] = res[key]

    logger.debug('Res: '+ str(res1))

    # Creamos los archivos de test

    path = PathTests+'/test'+time.strftime("%Y-%m-%e %H:%M:%S")

    os.makedirs(path)

    dTA.diccToArff(res1, path+'/extractionTotal.arff', attributesFilter)

    # Generate tests
    attributesFilter1 = dict(attributesFilter)
    attributesFilter1.pop("userId", None)
    attributesFilter1.pop("phraseId", None)
    attributesFilter1.pop("attempt", None)
    attributesFilter1.pop("phrases", None)
    attributesFilter1.pop("duration", None)

    testGenerator.generate(res1, path, attributesFilter1)

if __name__ == '__main__':
    extract()