from __future__ import division

from sets import Set
from random import randint

import diccToArff1 as dTA

def generate(res1, attributesFilter, PathTests):

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

        dTA.diccToArff(train, PathTests+'train'+str(j)+'.arff', attributesFilter)
        dTA.diccToArff(test, PathTests+'test'+str(j)+'.arff', attributesFilter)