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

path = os.path.abspath(os.getcwd())+'/tests/test_temp'
dicc = pickle.load(open(path+"/extractionTotalDicc.p", "rb"))

def generate(attributesFilter, commonPct = 0.2, numGroups = 5, balanceRatio = {"bsas": 60, "cba": 40}, balanceGroup = {"train": 75, "test": 25}):

    #print dicc

    # Vamos a armar los casos de tests
    print "Casos de tests:"
    print "==============="
    print "Parametros: "+str(commonPct)+" "+str(numGroups)+" "+str(balanceRatio)+" "+str(balanceGroup)

    #ordenar por usuario y mayor aparicion
    users = {} 
    for k, v in dicc.items():
        userId = v['userId']
        if userId in users.keys(): 
            users[userId] = users[userId] + 1
        else:
            users[userId] = 1

    #print users

    resultsPaired = []

    usersInTests = []

    while len(resultsPaired) < numGroups:

        train = {}
        test = {}

        #Armo test: una parte de usados + una parte nueva
        balance = commonPct
        size = int(len(users.keys()) * 0.01 * balanceGroup["test"])
        testUsers = []

        usersNotInTests = [ x for x in users.keys() if x not in usersInTests]
        #print "size: "+str(size)+"usersInTests: "+str(len(usersInTests))+" usersNotInTests "+str(len(usersNotInTests))
        if len(usersInTests) > int(balance * size) and len(usersNotInTests) > int((1 - balance) * size):
            testUsers = testUsers + random.sample( usersInTests, int(balance * size))
            testUsers = testUsers + random.sample( usersNotInTests, int((1 - balance) * size))
            #print " usados: "+ str(int(balance * size))+" nuevos: "+ str(int((1 - balance) * size))
        elif len(usersNotInTests) > int(size):
            testUsers = testUsers + random.sample(usersNotInTests, int(size))
            #print " nuevos: "+ str(int((1 - balance) * size))
        else: 
            sys.exit("No hay mas instancias en usersInTests o en usersNotInTests")

        test = dict((k,v) for k, v in dicc.items() if v["userId"] in testUsers)

        #Armo train
        trainUsers = [ x for x in users.keys() if x not in testUsers]
        train = dict((k,v) for k, v in dicc.items() if v["userId"] in trainUsers)

        #me fijo que ese train test no lo tenga ya... y si las instancias son el 50% distintas
        pct = greaterCommonInstancesPct(test, resultsPaired)

        if ((train, test) not in resultsPaired) and (pct < commonPct) and balanceCheck(train, balanceRatio) and balanceCheck(test, balanceRatio):
            resultsPaired = resultsPaired + [(train, test)]
            usersInTests = usersInTests + testUsers
            statusTrain = "train: ( bsas: "+str(len(bsas(train)))+" cba: "+str(len(cba(train)))+" => Tot: "+str(len(cba(train))+len(bsas(train)))+")"
            statusTest =  "test: ( bsas: "+str(len(bsas(test)))+" cba: "+str(len(cba(test)))+" => Tot: "+str(len(cba(test))+len(bsas(test)))+")"
            print statusTrain+" "+statusTest+" - "+str(pct)

    #resultsPaired tiene los test generados
    resPairedToArff(resultsPaired, attributesFilter, "conf_pct"+str(commonPct)+"_numGroups"+str(numGroups)+"_bsas"+str(balanceRatio["bsas"])+"cba"+str(balanceRatio["cba"]))

def greaterCommonInstancesPct(testInstance, resultsPaired):
    "Saca para test el mayor porcentaje de instancias que comparte con los demás"
    def commonInstancesPct(d1, d2):
        common = set(d1.keys()) & set(d2.keys())
        return len(common) / len(d1.keys())

    pct = 0
    for (train, test) in resultsPaired:
        if pct < commonInstancesPct(testInstance, test):
            pct = commonInstancesPct(testInstance, test)
    return pct

def bsas(dicc):
    "Cantidad de instancias de bsas"
    return dict((k,v) for k, v in dicc.items() if v["place"] == "bsas")

def cba(dicc):
    "Cantidad de instancias de cba"
    return dict((k,v) for k, v in dicc.items() if v["place"] == "cba")

def balanceCheck(dicc, balanceRatio = {"bsas": 60, "cba": 40}):
    size = len(dicc)
    bsas = len(dict((k,v) for k, v in dicc.items() if v["place"] == "bsas"))
    cba = len(dict((k,v) for k, v in dicc.items() if v["place"] == "cba"))

    ckBsas = size * balanceRatio["bsas"] * 0.006 <= bsas <= size * balanceRatio["bsas"] * 0.014
    ckCba = size * balanceRatio["cba"] * 0.006 <= cba <= size * balanceRatio["cba"] * 0.014
    ckBoth = cba < bsas

    return ckBsas and ckCba and ckBoth

def resPairedToArff(resultsPaired, attributesFilter, folder):

    if not os.path.exists(path+'/'+folder):
        os.makedirs(path+'/'+folder)

    i = 0
    for (train, test) in resultsPaired:
        dTA.diccToArff(train, path+'/'+folder+'/train'+str(i)+'.arff', attributesFilter)
        dTA.diccToArff(test, path+'/'+folder+'/test'+str(i)+'.arff', attributesFilter)        
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

    #Varias ejecuciones:
    # def lotsOfExecutions():
    #     for balanceRatio in [{"bsas": 60, "cba": 40}, {"bsas": 55, "cba": 45}, {"bsas": 50, "cba": 50}]:
    #         for numGroups in [5]:
    #             for commonPct in [0.5, 0.45, 0.4, 0.38, 0.36, 0.35, 0.32, 0.3, 0.28, 0.25, 0.2, 0.1]:

    #                 p = multiprocessing.Process(target= generate, name="generate", args=(attributesFilter, commonPct, numGroups, balanceRatio,))
    #                 p.start()

    #                 p.join(900)

    #                 if p.is_alive():
    #                     print "Paso el tiempo ... a matarlo"

    #                     p.terminate()
    #                     p.join()

    #lotsOfExecutions()

    generate(attributesFilter, commonPct=0.3)