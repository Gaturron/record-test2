#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint
from collections import deque
from collections import Counter
import itertools, csv

rules = {   "1" : "", 
            "2" : "", 
            "3" : "", 
            "4" : "", 
            "5" : "",
            "6" : ""  }

phrases = { "1" : "No hay dos sin tres",
            "2" : "La tercera es la vencida",
            "3" : "Perro que ladra no muerde",
            "4" : "El pez por la boca muere",
            "5" : "En boca cerrada no entran moscas",
            "6" : "Más vale pájaro en mano que 100 volando",
            "7" : "La curiosidad mató al gato",
            "8" : "Río revuelto, ganancia de pescadores",
            "9" : "No hay que pedirle peras al olmo",
            "10" : "Más difícil que encontrar una aguja en un paja",
            "11" : "Más perdido que turco en la neblina",
            "12" : "No le busques la quinta pata al gato",
            "13" : "Todo bicho que camina va al asador",
            "14" : "Caminante no hay camino, se hace camino al andar",
            "15" : "Se te escapó la tortuga",
            "16" : "Todos los caminos conducen a Roma",
            "17" : "No hay mal que dure 100 años ",
            "18" : "Siempre que llovió par",
            "19" : "Cría cuervos, que te sacarán los ojos ",
            "20" : "Calavera no chilla",
            "21" : "La gota que rebasó el vaso",
            "22" : "La suegra y el doctor, cuanto más lejos, mejor",
            "23" : "A la mujer picaresca, cualquiera la pesca.",
            "24" : "Quien siembra vientos recoge tempestades  ",
            "25" : "Un grano no hace granero, pero ayuda a su compañer",
            "26" : "La arquitectura es el arte de organizar el espacio",
            "27" : "El amor actúa con el corazón y no con la cabeza. ",
            "28" : "No dudes, actúa.",
            "29" : "El niño es realista; el muchacho, idealista; el hombre, escéptico, y el viejo, místico",
            "30" : "La música es sinónimo de libertad, de tocar lo que quieras y como quieras", 
            "31" : "La belleza que atrae rara vez coincide con la belleza que enamora",
            "32" : "No está mal ser bella; lo que está mal es la obligación de serlo",
            "33" : "La batalla más difícil la tengo todos los días conmigo mismo",
            "34" : "El que no llora, no mama",
            "35" : "En la pelea, se conoce al soldado; sólo en la victoria, se conoce al caballero",
            "36" : "La lectura es a la mente lo que el ejercicio al cuerpo"}

phrasesXrules = { 
            "1" : [2],
            "2" : [2],
            "3" : [6],
            "4" : [2],
            "5" : [2,3],
            "6" : [2],
            "7" : [6],
            "8" : [2,3],
            "9" : [2],
            "10" : [2],
            "11" : [2],
            "12" : [2],
            "13" : [],
            "14" : [],
            "15" : [3],
            "16" : [2, 6],
            "17" : [],
            "18" : [5],
            "19" : [2],
            "20" : [5],
            "21" : [6],
            "22" : [2,4],
            "23" : [3],
            "24" : [2,6],
            "25" : [],
            "26" : [2,4],
            "27" : [4],
            "28" : [2,4],
            "29" : [],
            "30" : [2],
            "31" : [5],
            "32" : [5],
            "33" : [2,5],
            "34" : [5],
            "35" : [4,5],
            "36" : [2,4] }

count = 10000
#print "Traces Generator"

def setAccum():
      # Cantidad de frases que le pegan a cada regla
      keys = phrasesXrules.keys()
      usedRules = []
      for key in keys:
          usedRules = usedRules + phrasesXrules[key]

      rulesTotal = {}
      for i in usedRules:
          if i in rulesTotal:
              rulesTotal[i] = rulesTotal[i] + 1
          else:
              rulesTotal[i] = 1

      for i in rulesTotal:
          rulesTotal[i] = {"count" : 0, "total" : rulesTotal[i]}

      return rulesTotal

# Saco sus porcentajes
def percentages(accum):
      amount = []
      for k in accum.keys():
            amount.append({"rule" : k, "pct": 100 * accum[k]["count"] / accum[k]["total"]})
      return amount

# Saco la regla que menos esta cubierta
def getMinPctRule(accum): 
      #print "getMinPctRule:"
      pcts = percentages(accum)
      accumPct = sorted(pcts, key=lambda a: a["pct"])

      minsRules = []
      for k in pcts:
            if k["pct"] == accumPct[0]["pct"]:
                  minsRules = minsRules + [ k["rule"]]

      #print minsRules
      return minsRules[ randint(0, len(minsRules) - 1 ) ]

def selectPhraseUsingRule(ruleId, phrasesXrules):
      #print "selectPhraseUsingRule: "+str(ruleId)
      res = []
      for k in phrasesXrules:
            if ruleId in phrasesXrules[k]:
                  res = res + [ k ]
      #print res
      return res[ randint(0, len(res) - 1 ) ]

def addPhraseToAccum(phraseId, accum, phrasesXrules):
      rules = phrasesXrules[phraseId]
      for r in rules:
            accum[r]["count"] += 1

def isFull(accum):
      res = True
      pct = percentages(accum)
      for k in pct:
            if (k["pct"] < 100): res = False
      return res


# Creo el acumulador
accum = setAccum()
#print "accum: "+str(accum)

#print "percentages: "+str(percentages(accum))
#print "getMinPctRule: "+str(getMinPctRule(accum))

#print "==========================="
# Hagamos el algoritmo
phrasesTotal = {}

for i in range(0,count):
      phrasesRes = []
      accum = setAccum()
      phrasesXrulesTMP = phrasesXrules.copy()
      while not(isFull(accum)):
            ruleId = getMinPctRule(accum)
            phraseId = selectPhraseUsingRule(ruleId, phrasesXrulesTMP)
            #print " RuleId elegida:  "+str(ruleId)+" PhraseId elegida:"+str(phraseId)+" ("+str(phrasesXrules[str(phraseId)])+") "
            
            #phrasesRes = phrasesRes + [phrasesXrules[str(phraseId)]]
            phrasesRes = phrasesRes + [str(phraseId)]
            
            addPhraseToAccum(phraseId, accum, phrasesXrulesTMP)
            del phrasesXrulesTMP[phraseId]
            #print "*** percentages: "+ str(percentages(accum))
            #print "-------------------------------------------"

      #print phrasesRes
      phrasesTotal[i] = phrasesRes

#print "#========================================================================================="
#=========================================================================================
#=========================================================================================
#Amper
amperTotal = {}

noun = ["El Canapé", "El Repollo", "El Espárrago"] 
obj = ["espectacular", "delicioso", "riquísimo"]

amperPhrases = []
index = 40
for n in noun:
      for o in obj:
            amperPhrases = amperPhrases + [ { "noun": n, "obj": o, "index": index } ]
            phrases[index] = n+" salió "+o
            
            if n == "El Repollo":
                  phrasesXrules[str(index)] = [1, 5, 6]
            elif n == "El Espárrago":
                  phrasesXrules[str(index)] = [1, 6]
            else:
                  phrasesXrules[str(index)] = [1] 
            index += 1

#generamos las frases Amper
for i in range(0,count):
      amperPhrasesTMP = list(amperPhrases)
      amper = []
      lastNouns = deque([])
      while amperPhrasesTMP != []:
            phraseDic = amperPhrasesTMP[ randint(0, len(amperPhrasesTMP) - 1 ) ]
            
            if not phraseDic["noun"] in lastNouns:
                  amperPhrasesTMP.remove(phraseDic)
                  
                  amper = amper + [ phraseDic["index"] ] 
                  #amper = amper + [ phrasesXrules[str(phraseDic["index"]) ] ]
                  
                  if len(lastNouns) > 1: lastNouns.popleft()
                  lastNouns.append(phraseDic["noun"])

      #print amper
      amperTotal[i] = amper

#print "#========================================================================================="
#print "#========================================================================================="
#print "Traza total:"
#print phrasesTotal
#print amperTotal
#print "mezclar"

trazasReales = []
for phraseKey, amperKey in itertools.izip_longest(phrasesTotal.keys(), amperTotal.keys()):
      trazaReal = []
      phraseTraza = deque(phrasesTotal[phraseKey])
      amperTraza = deque(amperTotal[amperKey])
      
      while phraseTraza or amperTraza:
            #veo cuantas frases comunes saco:
            numbPh = randint(1, 3)
            while numbPh > 0 and phraseTraza:
                  trazaReal.append(phraseTraza.popleft())
                  numbPh -=1

            if amperTraza: trazaReal.append(amperTraza.popleft())            

      #print trazaReal
      trazasReales.append(trazaReal)

#print trazasReales

# #print "#========================================================================================="
# #print "Hagamos los calculos: "
# #print "cortamos hasta diez"

# tmp = []
# for x in trazasReales:
#       tmp.append(x[:10])

# trazasReales = tmp
# #print trazasReales

# #print "juntar"
# f = (lambda l: reduce(lambda x,y: x+y,l))
# tmp = []
# for x in trazasReales:
#       tmp.append(Counter(f(x)))

# trazasReales = tmp
# #print trazasReales

ofile  = open('ttest.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

l = []
for k in phrases.keys():
      print l.append([k, phrases[k]])
 
for phrase in l:
      writer.writerow(phrase)

writer.writerow(["Fin phrases"])

for row in trazasReales:
      writer.writerow(row)
 
ofile.close()
