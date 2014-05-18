from __future__ import division

from sets import Set
from random import randint

import diccToArff1 as dTA

import os
import pickle
import operator

path = os.path.abspath(os.getcwd())+'/tests/test2014-05-17'
dicc = pickle.load(open(path+"/extractionTotalDicc.p", "rb"))

def generate(attributesFilter):

    #print dicc

    # Vamos a armar los casos de tests
    print "Casos de tests:"
    print "==============="

    #ordenar por usuario y mayor aparicion
    users = {} 
    for k, v in dicc.items():
        userId = v['userId']
        if userId in users.keys(): 
            users[userId] = users[userId] + 1
        else:
            users[userId] = 1

    print users

    resultsPaired = []

    while len(resultsPaired) < 10:

        sorted_users = sorted(users.iteritems(), key=operator.itemgetter(1))
        #print sorted_users

        train = {}
        test = {}

        while sorted_users:

            #sacar los 4 mayores y sacar al azar uno de ellos
            biggersUsers = sorted_users[-4:]
            userRandom = biggersUsers[randint(0, len(biggersUsers) - 1)]

            #print 'userRandom: '+str(userRandom)

            #obtener todas su informacion
            userRandomDicc = dict((k,v) for k, v in dicc.items() if v["userId"] == userRandom[0])
            
            if (len(train) < len(test)):
                insertInBestDicc(userRandomDicc, train, test)
            else:
                insertInBestDicc(userRandomDicc, test, train)

            sorted_users.remove(userRandom)

        statusTrain = "train: ( bsas: "+str(len(bsas(train)))+" cba: "+str(len(cba(train)))+")"
        statusTest =  "test: ( bsas: "+str(len(bsas(test)))+" cba: "+str(len(cba(test)))+")"
        print statusTrain+" "+statusTest

        #me fijo que ese train test no lo tenga ya
        if (train, test) not in resultsPaired:
            resultsPaired = resultsPaired + [(train, test)]

    #resultsPaired tiene los test generados
    resPairedToArff(resultsPaired, attributesFilter)

def bsas(dicc):
    return dict((k,v) for k, v in dicc.items() if v["place"] == "bsas")

def cba(dicc):
    return dict((k,v) for k, v in dicc.items() if v["place"] == "cba")

def insertInBestDicc(i, dicc1, dicc2):
    "Inserta i en donde mejor quepa"
    balanceRatio = {"bsas": 60, "cba": 40}

    place = [ v["place"] for k, v in i.items() ][0]

    if(( len(bsas(dicc1)) * balanceRatio["cba"] < len(cba(dicc1)) * balanceRatio["bsas"] and place == "bsas")
    or ( len(bsas(dicc1)) * balanceRatio["cba"] > len(cba(dicc1)) * balanceRatio["bsas"] and place == "cba")):
        dicc1.update(i)
    elif(( len(bsas(dicc2)) * balanceRatio["cba"] < len(cba(dicc2)) * balanceRatio["bsas"] and place == "bsas")
    or   ( len(bsas(dicc2)) * balanceRatio["cba"] > len(cba(dicc2)) * balanceRatio["bsas"] and place == "cba")):
        dicc2.update(i)
    else:
        dicc1.update(i)

def resPairedToArff(resultsPaired, attributesFilter):
    items = ["userId", "phraseId", "attempt", "phrases"]

    # for (train, test) in resultsPaired:
    #     for k, v in train.items():
    #         for i in items:
    #             #v.pop(i)
    #             pass
    #     for k, v in test.items():
    #         for i in items:
    #             #v.pop(i)
    #             pass

    i = 0
    for (train, test) in resultsPaired:
        dTA.diccToArff(train, path+'/train'+str(i)+'.arff', attributesFilter)
        dTA.diccToArff(test, path+'/test'+str(i)+'.arff', attributesFilter)        
        i = i+1

if __name__ == '__main__':

    #prueba
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

    generate(attributesFilter)