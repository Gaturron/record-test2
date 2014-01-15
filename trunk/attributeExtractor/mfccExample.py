from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav
import scikits.talkbox.features as features

#parametros MFCC
nwin=256 
nfft=512
nceps=13

def wavToMfcc(path):

    (rate,sig) = wav.read(path)

    #implementacion 1:
    #mfcc_feat = mfcc(sig,rate)

    #implementacion 2: 
    mfcc_feat = features.mfcc(sig, fs= rate, nwin= nwin, nfft= nfft, nceps= nceps)

    print mfcc_feat[0]

    #calculo de delta y delta-delta

    #decoracion de los tiempos de cada vector
    #guardamos en un diccionario

if __name__ == '__main__':
    print 'Prueba MFCC'
    wavToMfcc('/home/fernando/Tesis/Prosodylab-Aligner-master/data/bsas_u2_t44_a1.wav')