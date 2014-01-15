from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav
import scikits.talkbox.features as features

wavFile = '/home/fernando/Tesis/Prosodylab-Aligner-master/data/bsas_u2_t44_a1.wav'
(rate,sig) = wav.read(wavFile)

mfcc_feat = mfcc(sig,rate)
print mfcc_feat
print features.mfcc(sig, fs = rate)