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
import types

#path = os.path.abspath(os.getcwd())+'/tests/test_xHablante_igualesHabl'
path = os.path.abspath(os.getcwd())+'/tests/test_xHablante_igualesHabl_avgAttr'
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

#sacar    
#    'ACU_AverageKT': ['NUMERIC' for i in range(mfcc_len)],
#    'ACU_MaxKT': ['NUMERIC' for i in range(mfcc_len)],
#    'ACU_MinKT': ['NUMERIC' for i in range(mfcc_len)],
#    'ACU_AverageLL': ['NUMERIC' for i in range(mfcc_len)],
#    'ACU_MaxLL': ['NUMERIC' for i in range(mfcc_len)],
#    'ACU_MinLL': ['NUMERIC' for i in range(mfcc_len)],
#    'ACU_AverageRR': ['NUMERIC' for i in range(mfcc_len)],
#    'ACU_MaxRR': ['NUMERIC' for i in range(mfcc_len)],
#    'ACU_MinRR': ['NUMERIC' for i in range(mfcc_len)],
#    'ACU_AverageSC': ['NUMERIC' for i in range(mfcc_len)],
#    'ACU_MaxSC': ['NUMERIC' for i in range(mfcc_len)],
#    'ACU_MinSC': ['NUMERIC' for i in range(mfcc_len)]
}

def resPairedToArff(resultsPaired, attributesFilter, folder):

    """
    La idea es tener 8 hablantes de Córdoba y 8 de Buenos Aires
    y hacer los fold dejando 1 hab para test y los demás para train
    """

    if not os.path.exists(path+'/'+folder):
        os.makedirs(path+'/'+folder)

    i = 0
    for (train, test) in resultsPaired:
        dTA.diccToArff(train, path+'/'+folder+'/train'+str(i)+'.arff', attributesFilter)
        dTA.diccToArff(test, path+'/'+folder+'/test'+str(i)+'.arff', attributesFilter)        
        i = i+1

def juntandoGrabaciones(dicc):
    """
    La idea es iterar en el dicc y si hay varias grabaciones de 1 hablante juntar 
    todas las metricas en 1 grabacion
    """
    att_for_avg = [
        'userId',
        'place', 

        'FON_kt_norm',
        'FON_kt_normhd',
        'FON_ll_norm',
        'FON_ll_normhd',
        'FON_rr_norm',
        'FON_rr_normhd',
        'FON_sc_norm',
        'FON_sc_normhd',
        'FON_Sfinal_norm',
        'FON_Sfinal_normhd',
        
        'FON_phoneme',
        'FON_vowel_norm',
        'FON_vowel_normhd', 
        'FON_consonant_norm',
        'FON_consonant_normhd',

        'SIL_syllableAccent_norm',
        'SIL_syllableAccent_normhd',
        'SIL_prevSyllableAccent_norm',
        'SIL_prevSyllableAccent_normhd'
    ]

    dicc2 = {}
    #ordenar por userId
    for k, v in dicc.items():
        userId = v['userId'] 
        
        if userId in dicc2:
            dicc2[str(userId)] = [v] + dicc2[str(userId)] 
        else:
            dicc2[str(userId)] = [v]

    dicc3 = {}
    #recorro el diccionario juntando en cada atributo una lista con sus valores
    for userId, audios in dicc2.items():
        
        dicc_temp = {}
        for audio in audios:
            for k, att in audio.items():
                if k in att_for_avg and k in dicc_temp:
                    dicc_temp[k] = dicc_temp[k] + [ att ] 
                if k in att_for_avg and k not in dicc_temp:
                    dicc_temp[k] = [ att ]

        dicc3[userId] = dicc_temp

    print dicc3

    #recorro el diccionario haciendo el promedio de cada valor
    #avg = (lambda l: reduce(lambda x, y: x + y, l) / float(len(l)))

    def avg(l):
        sum = 0
        for x in l:
            if x != None:
                sum = sum + x
        return sum / float(len(l))

    dicc4 = {}
    for userId, audios in dicc3.items():
        
        dicc_temp = {}
        for k, att in audios.items():
            if len(att) > 0 and isinstance(att[0], basestring):
                dicc_temp[k] = att[0]
            if len(att) > 0 and isinstance(att[0], types.FloatType):
                dicc_temp[k] = avg(att)

        dicc4[userId] = dicc_temp

    return dicc4

if __name__ == '__main__':

    # obtengo los usuarios
    cantTotal = 8
    cantCba = 0
    cantBsAs = 0

    #opcional: 
    dicc = juntandoGrabaciones(dicc)   
    
    users = set([])
    for k, v in dicc.items():

        if v['place'] == 'cba' and v['userId'] not in users and cantCba < cantTotal:
            cantCba = cantCba + 1
            userId = v['userId']
            users.add(userId)
        
        if v['place'] == 'bsas' and v['userId'] not in users and cantBsAs < cantTotal:
            cantBsAs = cantBsAs + 1
            userId = v['userId']
            users.add(userId)

    print "Cantidad de hablantes de Córdoba "+str(cantCba)     
    print "Cantidad de hablantes de Buenos Aires "+str(cantBsAs)

    # armamos los tests de la forma <train, test>
    resultsPaired = []

    print str(users)

    for u in users:
        test = dict((k,v) for k, v in dicc.items() if v["userId"] == u)
        train = dict((k,v) for k, v in dicc.items() if v["userId"] != u)

        print "test "+str(len([k for k, v in test.items()]))+" userId"+str([v["userId"] for k, v in test.items()])
        print "train "+str(len([k for k, v in train.items()]))
        print "----------------------------------------------"

        resultsPaired = resultsPaired + [(train, test)]

    resPairedToArff(resultsPaired, attributesFilter, "version1")