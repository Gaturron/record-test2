# -*- coding: utf-8 -*-

import os
import sys
import pickle
import diccToArff1 as dTA

def pickleToArff(path_pickle, path_arff):
    """
    Idea: tomar el extractionTotalDicc.p y armar el .arff a partir de él
    """

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

    dicc = pickle.load(open(path_pickle, "rb"))

    # Generate tests
    attributesFilter1 = dict(attributesFilter)
    #attributesFilter1.pop("userId", None)
    #attributesFilter1.pop("phraseId", None)
    #attributesFilter1.pop("attempt", None)
    #attributesFilter1.pop("phrases", None)
    #attributesFilter1.pop("duration", None)

    dTA.diccToArff(dicc, path_arff, attributesFilter1)

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print "Pasar como parametro el path de los tests"
        print "Por ejemplo: /home/fernando/Tesis/record-test2/attributeExtractor/tests/extractionTotalDicc.p"
        sys.exit(0)

    path = sys.argv[1]
    drive, path_and_file = os.path.splitdrive(path)
    path, file = os.path.split(path_and_file)

    pickleToArff(path_and_file, path+'/'+file+'.arff')