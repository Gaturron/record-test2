from features import mfcc
from features import logfbank
from banyan import *
import scipy.io.wavfile as wav
import scikits.talkbox.features as features
import os

#parametros MFCC
nwin=256 
nfft=512
nceps=33#13

winstep = 0.01

def wavsToMfcc(pathFolder):

    print 'Directorio a analizar: '+str(pathFolder)
    filenames = os.listdir(pathFolder)

    dicMfcc = {}
    for filename in filenames:
        if (filename.endswith('.wav')):
            pathFile = pathFolder+'/'+filename
            dicFeatures = wavToMfcc(pathFile)
            dicMfcc[str(filename)] = dicFeatures

    return dicMfcc

def wavToMfcc(pathFile):

    print 'Wav a analizar: '+str(pathFile)
    (rate,sig) = wav.read(pathFile)
    print ' samplerate: '+str(rate)

    #=====================================================================
    #implementacion 1:
    mfcc_feat = mfcc(sig, samplerate= rate, winstep= winstep, numcep= nceps)

    #implementacion 2: 
    #mfcc_feat = features.mfcc(sig, fs= rate, nwin= nwin, nfft= nfft, nceps= nceps)
    #mfcc_feat = mfcc_feat[0]

    #=====================================================================

    print ' cantidad de features: '+str(len(mfcc_feat))
    print ' debe cumplirse: cantidad de features * winstep (en seg) = duracion del audio (en seg)'
    print '                 '+str(len(mfcc_feat))+' * '+str(winstep) +' = '+str(len(mfcc_feat) * winstep)

    #calculo de delta y delta-delta
    #asumo que ya lo calcula pidiendo mas nceps (chequear)

    #decoracion de los tiempos de cada vector
    #guardamos en un diccionario

    dicFeatures = SortedDict()
    time = winstep
    for i, feature in enumerate(mfcc_feat):
        dicFeatures[time] = feature
        #print 'Feat.Nro '+str(i)+' time:'+str(time)
        time = round(time + winstep, 3)

    # El diccionario va acorde al tamano de la ventana: o sea si winstep es de 0.01
    # va de 0.01 0.02 0.03 0.04 ...
    # Para consultar por un intervalo hacer
    #(ojo con las inclusiones, creo que incluye el 4.5 pero no el 4.19): 
    #print dicFeatures[4.19:4.5]
    # Solo anda para intervalos: no anda dicFeatures[1]

    return dicFeatures

if __name__ == '__main__':
    print 'Prueba MFCC: prueba wav'
    wavToMfcc('/home/fernando/Tesis/Prosodylab-Aligner-master/data/bsas_u2_t44_a1.wav')
    # 490 cantidad de features * 0.01 seg = 4.90 segundos de duracion
    
    wavToMfcc('/home/fernando/Descargas/FeatureExtraction/sp10.wav')
    # 266 cantidad de features * 0.01 seg = 2.66 segundos de duracion

    #print 'Prueba MFCC: prueba de directorio'
    wavsToMfcc('/home/fernando/Tesis/Prosodylab-Aligner-master/data')

    print 'Fin de prueba'