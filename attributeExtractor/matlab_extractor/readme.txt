# ANTES de correr el extractor hay que exportar algunas variables para que funcione el wrapper de matlab
# ejecutar esto antes de ejecutar el extractor 
# ejecutar de esta forma: $ source exports.sh

Files to generate mfcc feature vectors

Folder contents:

- wav2mfcc: returns mel frequency cepstral coefficients (MFCCs) computed from speech signal given a waveform filename
- vec2frames: splits signal into overlapped frames using indexing (used by wav2mfcc)
- trifbank: builds triangular filterbanks (used by wav2mfcc)

- batchFeatureExtraction: batch generation of MFCC features vectors from wav files (you must complete the parameters based on theory slides)