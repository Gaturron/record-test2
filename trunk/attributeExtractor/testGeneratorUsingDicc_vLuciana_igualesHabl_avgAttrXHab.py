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

"""
Idea: 
En el anterior varios atributos de los audios de 1 hablante se promediaban para dar 1 audio
O sea, dado un hablante, varias filas se unian en 1 sola promediando sus atributos 

Ahora la idea mejor es no descartar esos audios y a los valores con ? (o None) promediar 
con los que si estan

Atributos:    A1    A2    A3         .....     AN
H1:  audio1   1     ?     2                    2   
     audio2   ?     ?     1                    ?
     audio3   2     ?     3                    ?

H2:  audio1   1     ?     ?                    ?
     audio2   1     2     ?                    ?

esto pasaría a:
Atributos:    A1    A2    A3         .....     AN
H1:  audio1   1     ?     2                    2   
     audio2   1.5   ?     1                    2
     audio3   2     ?     3                    2

H2:  audio1   1     2     ?                    ?
     audio2   1     2     ?                    ?
"""

path = os.path.abspath(os.getcwd())+'/tests/test_xHablante_igualesHabl_avgAttrXHab'
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
    'SIL_prevSyllableAccent_normhd': 'NUMERIC'
}

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
    
    print '1) ================================================='

    dicc2 = {}
    #ordenar por userId
    for k, v in dicc.items():
        userId = v['userId'] 
        
        if userId in dicc2:
            dicc2[str(userId)] = [v] + dicc2[str(userId)] 
        else:
            dicc2[str(userId)] = [v]
    print str(dicc2['24'])
    print '2) =================================================='

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
    print str(dicc3['24'])
    print '4) =================================================='

    #recorro el diccionario haciendo el promedio de cada valor
    def avg(l):
        sum = 0
        div = 0
        
        for x in l:
            if x != None:
                sum = sum + x
                div = div + 1

        if div != 0:
            return sum / div
        else:
            return None

    # IMPORTANTE
    # Ojo: acá se va a iterar por los valores de los atributos de todos los audios
    # si hay 2 audios: a1, a2. 
    # Para el atributo FON_kt_norm a1 da 2 y en a1 NO SE CONTABILIZA (da None)
    # se debería respetar ese valor y descartar el None

    def allEqual(l):
        elem = None
        for e in l:
            if e == elem:
                elem = e
            else:
                return False

    def allNone(l):
        res = False
        for e in l:
            if e == None:
                res = True
        return res

    dicc4 = {}
    for userId, audios in dicc3.items():
        
        dicc_temp = {}
        for k, att in audios.items():
            if len(att) > 0:
                if isinstance(att[0], basestring):
                    dicc_temp[k] = att[0]
                else:
                    dicc_temp[k] = avg(att)

        dicc4[userId] = dicc_temp
    
    print str(dicc4['24'])
    print 'Fin  ==============================================='

    return dicc4

if __name__ == '__main__':

    # promedio los atributos de los hablantes
    diccAvg = juntandoGrabaciones(dicc)
    
    # si el attr es ? cambiar por supromedio local del hablante
    # dicc2 = {}
    # for k, v in dicc.items():
    #     userId = v['userId'] 
    #     if userId in dicc2:
    #         dicc2[str(userId)] = [v] + dicc2[str(userId)] 
    #     else:
    #         dicc2[str(userId)] = [v] 

    # dicc3 = {}
    # for userId, audios in dicc2.items():
    #     list_temp = []
    #     for audio in audios:

    #         diccAttr = {}
    #         for att, value in audio.items():
    #             if att in att_for_avg:
    #                 if value == None:
    #                     if diccAvg[userId][att] != None:
    #                         diccAttr[att] = diccAvg[userId][att]
    #                     else:
    #                         diccAttr[att] = value    
    #                 else:
    #                     diccAttr[att] = value
            
    #         list_temp = [diccAttr] + list_temp

    #     dicc3[userId] = list_temp

    # dicc = dicc3

    dicc2 = {}
    for audioKey, attrDic in dicc.items():

        userId = attrDic['userId']

        diccAttr = {}
        for att, value in attrDic.items():
            print " att: "+str(att)+" value: "+str(value)
            if att in att_for_avg:
                if value == None:
                    if diccAvg[userId][att] != None:
                        diccAttr[att] = diccAvg[userId][att]
                    else:
                        diccAttr[att] = value    
                else:
                    diccAttr[att] = value

        dicc2[str(audioKey)] = diccAttr

    dicc = dicc2

    print " Agregado el promedio en ? ========================================="

    # obtengo los usuarios
    cantTotal = 8
    cantCba = 0
    cantBsAs = 0
    
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