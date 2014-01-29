from textgrid import TextGrid, Tier
import mfccExtractor as mfccExt
import phraseToAccents as phToAcc
import attributes as att
import numpy as np
import re

# La 'c' antes de la 't' no suena
def _foundPattern(wordPattern, syllablePattern, textgrid, mfcc):
    accents = att._accents(textgrid)

    # buquemos si esta es la frase con 'CT'
    interval = {}

    for i, tier in enumerate(textgrid):
        if tier.nameid == 'words':
            for row in tier.simple_transcript:
                if re.search(wordPattern, str(row[2])):
                    interval['xmin'] = row[0]
                    interval['xmax'] = row[1]

    # busquemos en ese intervalo la 'k'
    interval1 = {}
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'phones':

            prevChar = ''
            for row in tier.simple_transcript:

                # guardo la letra previa sino es
                # if str(prevChar)+str(row[2]) == 'kt':
                if re.search(syllablePattern, str(prevChar)+str(row[2])):

                    if interval['xmin'] < row[0] and row[1] < interval['xmax']:
                        interval1['xmin'] = row[0]
                        interval1['xmax'] = row[1]
                else:
                    prevChar = row[2]

    if interval1:
        return mfcc[float(interval1['xmin']):float(interval1['xmax'])]
    else:
        return False

def mfccAverageKT(textgrid, mfcc):
    mfccTemp = _foundPattern(r'.CT.', r'kt', textgrid, mfcc)
    return np.average(mfccTemp, axis=0)

def mfccMaxKT(textgrid, mfcc):
    mfccTemp = _foundPattern(r'.CT.', r'kt', textgrid, mfcc)
    return np.amax(mfccTemp, axis=0)

def mfccMinKT(textgrid, mfcc):
    mfccTemp = _foundPattern(r'.CT.', r'kt', textgrid, mfcc)
    return np.amin(mfccTemp, axis=0)
#=======================================================================
def mfccAverageLL(textgrid, mfcc):
    mfccTemp = _foundPattern(r'(.*)LL.', r'.Z', textgrid, mfcc)
    return np.average(mfccTemp, axis=0)

def mfccMaxLL(textgrid, mfcc):
    mfccTemp = _foundPattern(r'(.*)LL.', r'.Z', textgrid, mfcc)
    return np.amax(mfccTemp, axis=0)

def mfccMinLL(textgrid, mfcc):
    mfccTemp = _foundPattern(r'(.*)LL.', r'.Z', textgrid, mfcc)
    return np.amin(mfccTemp, axis=0)



def dummy(textgrid, mfcc):
    return '8'