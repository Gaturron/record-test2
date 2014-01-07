from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav

wavFile = '/home/fernando/Tesis/Prosodylab-Aligner-master/data/bsas_u2_t44_a1.wav'
(rate,sig) = wav.read(wavFile)
mfcc_feat = mfcc(sig,rate)

print mfcc_feat[1:3,:]
print len(mfcc_feat)
