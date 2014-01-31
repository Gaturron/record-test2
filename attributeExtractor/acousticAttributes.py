from textgrid import TextGrid, Tier
import mfccExtractor as mfccExt
import phraseToAccents as phToAcc
import attributes as att
import numpy as np
import re

def phrases(textgrid, mfcc):
    return att.phrases(textgrid)

#=======================================================================
# La 'c' antes de la 't' no suena
def _foundPattern(wordPattern, syllablePattern, textgrid, mfcc):

    # buquemos si esta es la frase con 'CT'
    wordInterval = []

    for i, tier in enumerate(textgrid):
        if tier.nameid == 'words':
            for row in tier.simple_transcript:
                if re.search(wordPattern, str(row[2])):
                    interval = {}
                    interval['xmin'] = row[0]
                    interval['xmax'] = row[1]
                    wordInterval += [interval]

    print 'wordInterval: '+str(wordInterval)+' phrases: '+str(phrases(textgrid, mfcc))

    # busquemos en ese intervalo la 'k'
    syllableIntervals = []
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'phones':

            prevRow = (0,0,'')
            for row in tier.simple_transcript:

                # guardo la letra previa sino es
                if re.search(syllablePattern, str(prevRow[2])+str(row[2])):

                    for interval in wordInterval:
                        if interval['xmin'] < prevRow[0] and prevRow[1] < interval['xmax']:
                            interval1 = {}
                            interval1['xmin'] = prevRow[0]
                            interval1['xmax'] = prevRow[1]
                            syllableIntervals += [interval1]
                
                prevRow = row

    if syllableIntervals:
        #mfccs = ()
        l = []
        for interval in syllableIntervals:

            #tuplee = mfcc[float(interval['xmin']):float(interval['xmax'])]
            #mfccs = mfccs + tuplee
            l.append((float(interval['xmin']), float(interval['xmax'])))
        #return mfccs
        print 'syllableIntervals: '+str(syllableIntervals)
        return l
    else:
        return False

#=======================================================================

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
    mfccTemp = _foundPattern(r'LL.', r'Z.', textgrid, mfcc)
    return np.average(mfccTemp, axis=0)

def mfccMaxLL(textgrid, mfcc):
    mfccTemp = _foundPattern(r'LL.', r'Z.', textgrid, mfcc)
    return np.amax(mfccTemp, axis=0)

def mfccMinLL(textgrid, mfcc):
    mfccTemp = _foundPattern(r'LL.', r'Z.', textgrid, mfcc)
    return np.amin(mfccTemp, axis=0)
#=======================================================================

# TODO: Para la RR hacer el extractor de atributos para la longitud
def mfccAverageR(textgrid, mfcc):
    mfccTemp = _foundPattern(r'.RR.', r'R.', textgrid, mfcc)
    return np.average(mfccTemp, axis=0)

def mfccMaxR(textgrid, mfcc):
    mfccTemp = _foundPattern(r'.RR.', r'R.', textgrid, mfcc)
    return np.amax(mfccTemp, axis=0)

def mfccMinR(textgrid, mfcc):
    mfccTemp = _foundPattern(r'.RR.', r'R.', textgrid, mfcc)
    return np.amin(mfccTemp, axis=0)

#=======================================================================
def mfccAverageSC(textgrid, mfcc):
    mfccTemp = _foundPattern(r'.SC.', r'hk', textgrid, mfcc)
    return mfccTemp
    #return np.average(mfccTemp, axis=0)

def mfccMaxSC(textgrid, mfcc):
    mfccTemp = _foundPattern(r'.SC.', r'hk', textgrid, mfcc)
    return np.amax(mfccTemp, axis=0)

def mfccMinSC(textgrid, mfcc):
    mfccTemp = _foundPattern(r'.SC.', r'hk', textgrid, mfcc)
    return np.amin(mfccTemp, axis=0)

def _dummy(textgrid, mfcc):
    return '8'