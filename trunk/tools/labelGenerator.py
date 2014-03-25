#!/usr/bin/python
# -*- coding: utf-8 -*-

import unicodedata
import sys

phrases = { "1" : u"No hay dos sin tres",
            "2" : u"La tercera es la vencida",
            "3" : u"Perro que ladra no muerde",
            "4" : u"El pez por la boca muere",
            "5" : u"En boca cerrada no entran moscas",
            "6" : u"Más vale pájaro en mano que cien volando",
            "7" : u"La curiosidad mató al gato",
            "8" : u"Río revuelto, ganancia de pescadores",
            "9" : u"No hay que pedirle peras al olmo",
            "10" : u"Más difícil que encontrar una aguja en un paja",
            "11" : u"Más perdido que turco en la neblina",
            "12" : u"No le busques la quinta pata al gato",
            "13" : u"Todo bicho que camina va al asador",
            "14" : u"Caminante no hay camino, se hace camino al andar",
            "15" : u"Se te escapó la tortuga",
            "16" : u"Todos los caminos conducen a Roma",
            "17" : u"No hay mal que dure cien años",
            "18" : u"Siempre que llovió par",
            "19" : u"Cría cuervos, que te sacarán los ojos",
            "20" : u"Calavera no chilla",
            "21" : u"La gota que rebalsó el vaso",
            "22" : u"La suegra y el doctor, cuanto más lejos, mejor",
            "23" : u"A la mujer picaresca, cualquiera la pesca",
            "24" : u"Quien siembra vientos recoge tempestades",
            "25" : u"Un grano no hace granero, pero ayuda a su compañero",
            "26" : u"La arquitectura es el arte de organizar el espacio",
            "27" : u"El amor actúa con el corazón y no con la cabeza",
            "28" : u"No dudes, actúa",
            "29" : u"El niño es realista; el muchacho, idealista; el hombre, escéptico, y el viejo, místico",
            "30" : u"La música es sinónimo de libertad, de tocar lo que quieras y como quieras", 
            "31" : u"La belleza que atrae rara vez coincide con la belleza que enamora",
            "32" : u"No está mal ser bella; lo que está mal es la obligación de serlo",
            "33" : u"La batalla más difícil la tengo todos los días conmigo mismo",
            "34" : u"El que no llora, no mama",
            "35" : u"En la pelea, se conoce al soldado; sólo en la victoria, se conoce al caballero",
            "36" : u"La lectura es a la mente lo que el ejercicio al cuerpo",
            "40" : u"El Canapé salió espectacular",
            "41" : u"El Canapé salió delicioso",
            "42" : u"El Canapé salió riquísimo",
            "43" : u"El Repollo salió espectacular",
            "44" : u"El Repollo salió delicioso",
            "45" : u"El Repollo salió riquísimo",
            "46" : u"El Espárrago salió espectacular",
            "47" : u"El Espárrago salió delicioso",
            "48" : u"El Espárrago salió riquísimo"
        }

def elimina_tildes(string):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(string)) if unicodedata.category(c) != 'Mn'))
    return s.decode()

def elimina_puntuacion(string):
    return string.replace(",", "").replace(";", "")
    
for filename in sys.argv[1:]:
    file = open(filename, "w+")
    i = filename.split("_")[2].replace("t", "")
    text = elimina_puntuacion(elimina_tildes(phrases[i])).upper()
    file.write(text+"\n")
    file.close()
