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

    mfcc_len = 33

    attributesFilter = {
        'place': ('bsas', 'cba'), 
        'phrases': 'STRING', 
        'duration': 'NUMERIC', 
        'userId': 'NUMERIC',
        'phraseId': 'NUMERIC',
        'attempt': 'NUMERIC',

        'FON_kt_norm': 'NUMERIC', 
        'FON_kt_normhd': 'NUMERIC',
        'FON_ll_norm': 'NUMERIC', 
        'FON_ll_normhd': 'NUMERIC', 
        'FON_rr_norm': 'NUMERIC',  
        'FON_rr_normhd': 'NUMERIC', 
        'FON_sc_norm': 'NUMERIC',
        'FON_sc_normhd': 'NUMERIC',
        'FON_Sfinal_norm': 'NUMERIC',
        'FON_Sfinal_normhd': 'NUMERIC',
        
        'FON_phoneme': 'NUMERIC',
        'FON_vowel_norm': 'NUMERIC', 
        'FON_vowel_normhd': 'NUMERIC', 
        'FON_consonant_norm': 'NUMERIC',
        'FON_consonant_normhd': 'NUMERIC',
        
        'SIL_syllableAccent_norm': 'NUMERIC',
        'SIL_syllableAccent_normhd': 'NUMERIC',
        'SIL_prevSyllableAccent_norm': 'NUMERIC',
        'SIL_prevSyllableAccent_normhd': 'NUMERIC',
         
        'ACU_AverageKT': ['NUMERIC' for i in range(mfcc_len)],
        'ACU_MaxKT': ['NUMERIC' for i in range(mfcc_len)],
        'ACU_MinKT': ['NUMERIC' for i in range(mfcc_len)],
        'ACU_AverageLL': ['NUMERIC' for i in range(mfcc_len)],
        'ACU_MaxLL': ['NUMERIC' for i in range(mfcc_len)],
        'ACU_MinLL': ['NUMERIC' for i in range(mfcc_len)],
        'ACU_AverageRR': ['NUMERIC' for i in range(mfcc_len)],
        'ACU_MaxRR': ['NUMERIC' for i in range(mfcc_len)],
        'ACU_MinRR': ['NUMERIC' for i in range(mfcc_len)],
        'ACU_AverageSC': ['NUMERIC' for i in range(mfcc_len)],
        'ACU_MaxSC': ['NUMERIC' for i in range(mfcc_len)],
        'ACU_MinSC': ['NUMERIC' for i in range(mfcc_len)]
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

    # Generate tests
    attributesFilter1 = dict(attributesFilter)
    attributesFilter1.pop("userId", None)
    attributesFilter1.pop("phraseId", None)
    attributesFilter1.pop("attempt", None)
    attributesFilter1.pop("phrases", None)
    attributesFilter1.pop("duration", None)

    dTA.diccToArff(res1, path+'/extractionTotal.arff', attributesFilter1)

    testGenerator.generate(res1, path, attributesFilter1)

if __name__ == '__main__':
    extract()