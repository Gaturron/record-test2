from __future__ import division

import alignmentFilter as agmntFilter
import diccToArff1 as dTA
from textgridExtractor import textgridExtractor
from acousticExtractor import acousticExtractor
import logging
import os

from sets import Set
from random import randint

Path = os.path.abspath(os.path.join(os.getcwd(), '..', '..'))+'/Prosodylab-Aligner-master/data1.complete/'
PathTests = os.path.abspath(os.getcwd())+'/tests/'
PathTests2 = os.path.abspath(os.getcwd())+'/tests2/'

#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=None)

def extract():

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
        'SIL_prevSyllableAccent_normhd': 'NUMERIC'
        
        #, 
        # 'mfccAverageKT': ['NUMERIC' for i in range(26)],
        # 'mfccMaxKT': ['NUMERIC' for i in range(26)],
        # 'mfccMinKT': ['NUMERIC' for i in range(26)],
        # 'mfccAverageLL': ['NUMERIC' for i in range(26)],
        # 'mfccMaxLL': ['NUMERIC' for i in range(26)],
        # 'mfccMinLL': ['NUMERIC' for i in range(26)],
        # 'mfccAverageRR': ['NUMERIC' for i in range(26)],
        # 'mfccMaxRR': ['NUMERIC' for i in range(26)],
        # 'mfccMinRR': ['NUMERIC' for i in range(26)],
        # 'mfccAverageSC': ['NUMERIC' for i in range(26)],
        # 'mfccMaxSC': ['NUMERIC' for i in range(26)],
        # 'mfccMinSC': ['NUMERIC' for i in range(26)],
    }

    logger = logging.getLogger('Extract')
    logger.info('starting')

    pathList = agmntFilter.filter(Path)
    logger.debug('pathList: (tam. '+str(len(pathList))+') '+ str(pathList))

    tgExtractor = textgridExtractor(attributesFilter.keys())
    tgRes = tgExtractor.textgridsToAtt(pathList)
    #logger.debug('tgRes: '+ str(tgRes))

    #acExtractor = acousticExtractor(attributesFilter.keys())
    #acRes = acExtractor.extracts(pathList)
    #logger.debug('acRes: '+ str(acRes))

    res = {}
    for sample in tgRes.keys():
    	#res[sample] = dict(tgRes[sample].items() + acRes[sample].items())
        res[sample] = dict(tgRes[sample].items())

    res1 = {}
    for key in res.keys():
    	filename = key.split('/')[-1]
    	res[key]['place'] = filename.split('_')[0]
        res[key]['userId'] = filename.split('_')[1][1:]
        res[key]['phraseId'] = filename.split('_')[2][1:]
        res[key]['attempt'] = filename.split('_')[3][1:]
    	res1[filename] = res[key]

    logger.debug('Res: '+ str(res1))

    dTA.diccToArff(res1, PathTests+'testNew.arff', attributesFilter)

    # Vamos a armar los casos de tests
    print "Casos de tests:"
    print "==============="

    for j in range(10):
        train = dict(res1)
        test = {}
        
        usersBsas = list(Set([ v["userId"] for k, v in train.items() if v["place"] == "bsas" ]))
        usersCba = list(Set([ v["userId"] for k, v in train.items() if v["place"] == "cba" ]))
        print str(j)+") usersBsas: "+str(len(usersBsas))+" usersCba:"+str(len(usersCba))

        while (len(test) / len(res1)) < 0.10:

            if len(usersBsas) != 0:
                inxBsas = randint(0, len(usersBsas) - 1)
                userBsas = usersBsas.pop(inxBsas)

                for k, v in train.items():
                    if v["userId"] == userBsas:
                        v1 = dict(v)

                        v1.pop("userId", None)
                        v1.pop("phraseId", None)
                        v1.pop("attempt", None)
                        v1.pop("phrases", None)
                        
                        test[k] = v1
                        train.pop(k, None)

            if len(usersCba) != 0:
                inxCba = randint(0, len(usersCba) - 1)
                userCba = usersCba.pop(inxCba)
                
                for k, v in train.items():
                    if v["userId"] == userCba:
                        v1 = dict(v)    

                        v1.pop("userId", None)
                        v1.pop("phraseId", None)
                        v1.pop("attempt", None)
                        v1.pop("phrases", None)

                        test[k] = v1
                        train.pop(k, None)

            print " - "+str(len(train))+" "+str(len(test))+" - "+str(len(test) / len(res1))

        print len(train)
        print len(test)

        attributesFilter1 = dict(attributesFilter)
        attributesFilter1.pop("userId", None)
        attributesFilter1.pop("phraseId", None)
        attributesFilter1.pop("attempt", None)
        attributesFilter1.pop("phrases", None)
        attributesFilter1.pop("duration", None)
        #dTA.diccToArff(train, PathTests+'train'+str(j)+'.arff', attributesFilter1)
        #dTA.diccToArff(test, PathTests+'test'+str(j)+'.arff', attributesFilter1)

    print "Casos de tests 2:"
    print "================="

    for j in range(10):
        train = dict(res1)
        test = {}

        while (len(test) / len(res1)) < 0.30:

            audioBsas = [ v for k, v in train.items() if v["place"] == "bsas"]
            audioCba = [ v for k, v in train.items() if v["place"] == "cba"]

            if len(audioBsas) < len(audioCba):
                # mayoria cba    

                usersCba = list(Set([ v["userId"] for k, v in train.items() if v["place"] == "cba" ]))
                inxCba = randint(0, len(usersCba) - 1)
                userCba = usersCba.pop(inxCba)
                
                for k, v in train.items():
                    if v["userId"] == userCba:
                        v1 = dict(v)    

                        v1.pop("userId", None)
                        v1.pop("phraseId", None)
                        v1.pop("attempt", None)
                        v1.pop("phrases", None)

                        test[k] = v1
                        train.pop(k, None)

            else:
                # mayoria bsas

                usersBsas = list(Set([ v["userId"] for k, v in train.items() if v["place"] == "bsas" ]))
                inxBsas = randint(0, len(usersBsas) - 1)
                userBsas = usersBsas.pop(inxBsas)

                for k, v in train.items():
                    if v["userId"] == userBsas:
                        v1 = dict(v)

                        v1.pop("userId", None)
                        v1.pop("phraseId", None)
                        v1.pop("attempt", None)
                        v1.pop("phrases", None)
                        
                        test[k] = v1
                        train.pop(k, None)

        attributesFilter1 = dict(attributesFilter)
        attributesFilter1.pop("userId", None)
        attributesFilter1.pop("phraseId", None)
        attributesFilter1.pop("attempt", None)
        attributesFilter1.pop("phrases", None)
        attributesFilter1.pop("duration", None)
        
        dTA.diccToArff(train, PathTests2+'train'+str(j)+'.arff', attributesFilter1)
        dTA.diccToArff(test, PathTests2+'test'+str(j)+'.arff', attributesFilter1)

if __name__ == '__main__':
    extract()