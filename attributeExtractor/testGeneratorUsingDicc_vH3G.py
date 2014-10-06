# -*- coding: utf-8 -*-
from __future__ import division

from sets import Set

import diccToArff1 as dTA

import os
import pickle
import operator

import multiprocessing
import time
import random
import sys

path = os.path.abspath(os.getcwd())+'/tests/test_xH3G'
dicc = pickle.load(open(path+"/extractionTotalDicc.p", "rb"))

mfcc_len = 33
attributesFilter = {
    'place': ('bsas', 'cba'), 

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

def resPairedToArff(resultsPaired, attributesFilter, folder):

    """
    Vamos a generar los grupos de la siguiente forma:
    hay 27 hablantes, los dividimos en 9 folds donde test tiene 3 hablantes cada uno
    entonces:
    F1: {test: [h1, h2, h3], train: lo demas}
    F2: {test: [h4, h5, h6], train: lo demas}
    ...
    F9: {test: [h25, h26, h27], train: lo demas}
    """

    if not os.path.exists(path+'/'+folder):
        os.makedirs(path+'/'+folder)

    i = 0
    for (train, test) in resultsPaired:
        dTA.diccToArff(train, path+'/'+folder+'/train'+str(i)+'.arff', attributesFilter)
        dTA.diccToArff(test, path+'/'+folder+'/test'+str(i)+'.arff', attributesFilter)        
        i = i+1

if __name__ == '__main__':

    # obtengo los usuarios
    users = set([])
    for k, v in dicc.items():
        userId = v['userId']
        users.add(userId)
    users = list(users)

    # armamos los tests de la forma <train, test>
    resultsPaired = []

    print "users "+str(users)

    d = int(len(users) / 3)

    for u in range(d):
        idUsersInTest = users[(u*3) : (u*3)+3]
        idUsersInTrain = [u for u in users if u not in idUsersInTest]

        print "idUsersInTest: "+str(idUsersInTest)+" idUsersInTrain: "+str(idUsersInTrain)

        test = dict((k,v) for k, v in dicc.items() if v["userId"] in idUsersInTest)
        train = dict((k,v) for k, v in dicc.items() if v["userId"] in idUsersInTrain)

        #print "test "+str(len([k for k, v in test.items()]))+" userId"+str([v["userId"] for k, v in test.items()])
        #print "train "+str(len([k for k, v in train.items()]))
        print "----------------------------------------------"

        resultsPaired = resultsPaired + [(train, test)]

    resPairedToArff(resultsPaired, attributesFilter, "version1")