from textgrid import TextGrid, Tier
import phraseToAccents as phToAcc
import scipy as np
import string
import re
import logging

logger = logging.getLogger('attributes textgrid ')

# Las funciones declaradas aca deben tener como parametro TextGrid
# si se agrega al principio _ no se ejecuta para extractor

vowels = ['a', 'e', 'i', 'o', 'u']

# calculate the consonants
consonants = []
for l in string.lowercase:
    if not l in vowels: 
        consonants += [l]

#digits to round
digits = 3

#============================================================================

def phrases(textgrid):
    """return the phrase from the textgrid"""
    phrase = ''
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'words':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp' and row[2] != '':
                    phrase += row[2].strip() + ' '
    return phrase.lower().strip()

def _accents(textgrid):
    """return the accents"""
    return phToAcc.getAccents(phrases(textgrid))

def _goThroughWithCondition(textgrid, nameTier, condition):
    # recorre el tier con nameTier y devuelve el array que cumple con los 
    # elementos de la condicion

    result = []
    for i, tier in enumerate(textgrid):
        if tier.nameid == nameTier:
            for row in tier.simple_transcript:
                if condition(row):
                    result += [ float(row[1]) - float(row[0]) ]
    return result

def _durationOfEachSyllable(textgrid):
    
    """duration of each syllable of the textgrid. Returns a dictionary"""

    phones = []
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'phones':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp' and row[2] != '':
                    phones += [ {'text': row[2], 'time': float(row[1]) - float(row[0])} ]

    #logger.debug('phones: '+str(phones))
    
    silabes = []
    for w in _accents(textgrid):
        silabes += w
    
    #logger.debug('silabes: '+str(silabes))

    silabes2 = []
    index = 0
    for silabe in silabes:
        silabe_time = 0
        for char in silabe:
            if char != '*':
                silabe_time += phones[index]['time']
                index += 1
        silabes2 += [ {'text': silabe, 'time': round(silabe_time, digits)} ]

    #logger.debug('silabes2: '+str(silabes2))

    silabes3 = []
    index = 0
    for word in _accents(textgrid):
        w = []
        for silabe in word:
            w += [ silabes2[index] ]
            index += 1
        silabes3 += [ w ]

    #logger.debug('silabes3: '+ str(silabes3))

    return silabes3

def _normalizar(arraySample, arrayTotal):
    """Normalizar utilizando mu y desvio estandar"""
    if len(arraySample) == 0 or len(arrayTotal) == 0:
        return None
    else:
        res = (np.average(arraySample) - np.average(arrayTotal)) / np.var(arrayTotal)
        logger.debug("sample: "+str(np.round_(arraySample, 2))+" total: "+str(np.round_(arrayTotal, 2)))
        logger.debug(str(np.average(arraySample))+" - "+str(np.average(arrayTotal))+" / "+str(np.var(arrayTotal)))
        return round(res, digits)

def _normalizar_halfdist(arraySample, arrayTotal):
    """Normalizar utilizando solo desvio standar. Suponiendo mu = 0"""
    if len(arraySample) == 0 or len(arrayTotal) == 0:
        return None
    else:
        res = np.average(arraySample) / np.var(arrayTotal)
        logger.debug("sample: "+str(np.round_(arraySample, 2))+" total: "+str(np.round_(arrayTotal, 2)))
        logger.debug(str(np.average(arraySample))+" - "+str(np.average(arrayTotal))+" / "+str(np.var(arrayTotal)))
        return round(res, digits)

def _durationOfEachPhoneme(textgrid):
    f = lambda row: row[2] != 'sil' and row[2] != 'sp' and row[2] != ''
    res = _goThroughWithCondition(textgrid, "phones", f)
    return res

#============================================================================

def duration(textgrid):
    f = lambda row: row[2] != 'sil' and row[2] != 'sp' and row[2] != ''
    res = _goThroughWithCondition(textgrid, "words", f)
    res = round(np.sum(res), digits)
    
    logger.info('duration: '+str(res))
    
    return res

def FON_phoneme(textgrid):
    """duration average of each phoneme"""
    f = lambda row: row[2] != 'sil' and row[2] != 'sp' and row[2] != ''
    res = _goThroughWithCondition(textgrid, "phones", f)
    
    if len(res) == 0:
        return None    
    
    res = round(np.average(res), digits)
    logger.info('FON_phoneme: '+str(res))
    
    return res

def FON_vowel_norm(textgrid):
    """duration average of each vowel normalized"""    
    f = lambda row: row[2] != 'sil' and row[2] != 'sp' and string.lower(row[2]) in vowels 
    res = _goThroughWithCondition(textgrid, "phones", f)
    res = _normalizar(res, _durationOfEachPhoneme(textgrid))
    
    logger.info('FON_wowel_norm: '+str(res))
    
    return res

def FON_vowel_normhd(textgrid):
    """duration average of each vowel normalized half distribution""" 
    f = lambda row: row[2] != 'sil' and row[2] != 'sp' and string.lower(row[2]) in vowels 
    res = _goThroughWithCondition(textgrid, "phones", f)
    res = _normalizar_halfdist(res, _durationOfEachPhoneme(textgrid))
    
    logger.info('FON_vowel_normhd: '+str(res))
    
    return res

def FON_consonant_norm(textgrid):
    """duration average of each consonant normalized""" 
    f = lambda row: row[2] != 'sil' and row[2] != 'sp' and string.lower(row[2]) in consonants 
    res = _goThroughWithCondition(textgrid, "phones", f)
    res = _normalizar(res, _durationOfEachPhoneme(textgrid))
    
    logger.info('FON_consonant_norm: '+str(res))
    
    return res

def FON_consonant_normhd(textgrid):
    """duration average of each consonant normalized half distribution"""
    f = lambda row: row[2] != 'sil' and row[2] != 'sp' and string.lower(row[2]) in consonants 
    res = _goThroughWithCondition(textgrid, "phones", f)
    res = _normalizar_halfdist(res, _durationOfEachPhoneme(textgrid))
    
    logger.info('FON_consonant_normhd: '+str(res))
    
    return res

def _durationAvgOfPhonemeSFinal(textgrid):

    wordsWithPhonemeS = []
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'words':
            for row in tier.simple_transcript:
                logger.debug('analising row: '+str(row))
                if len(row[2]) > 1 and str(row[2][-1]) == 'S':
                    # buscar entre esos valores de tiempo que es una /s/ final
                    wordsWithPhonemeS += [ {'xmin': row[0], 'xmax': row[1]} ]
    #logger.debug('wordsWithPhonemeS: '+str(wordsWithPhonemeS))

    #busco en esos intervalos que va a haber una /s/ final
    result = []
    for word in wordsWithPhonemeS:
        for i, tier in enumerate(textgrid):
            if tier.nameid == 'phones':
                for row in tier.simple_transcript:
                    if str(row[2]) == 's' and word['xmin'] <= row[0] and row[1] <= word['xmax']:
                        result += [ float(row[1]) - float(row[0]) ]

    return result

def FON_Sfinal_norm(textgrid):
    """duration average of phoneme S Final normalized"""
    res = _durationAvgOfPhonemeSFinal(textgrid)
    res = _normalizar(res, _durationOfEachPhoneme(textgrid))
    logger.info("FON_Sfinal_norm: "+str(res))
    return res 

def FON_Sfinal_normhd(textgrid):
    """duration average of phoneme S Final normalized half distribution"""
    res = _durationAvgOfPhonemeSFinal(textgrid)
    res = _normalizar_halfdist(res, _durationOfEachPhoneme(textgrid))
    logger.info("FON_Sfinal_normhd: "+str(res))
    return res

# Regla 1: Localice la silaba acentuada y estirar la silaba anterior
def _durationAvgOfPrevSyllableAccent(textgrid):

    syllables = _durationOfEachSyllable(textgrid)

    result = []

    prevSyllable = ''
    for word in syllables:
        for syllable in word:

            if syllable['text'][-1] == '*' and prevSyllable != '':
                result += [ prevSyllable['time'] ]

            logger.debug('prevSyllable: '+str(prevSyllable)+' syllable: '+str(syllable))
            prevSyllable = syllable

    # obtener solo el tiempo de cada silaba
    syllablesTime = []
    for word in syllables:
        for syllable in word:
            syllablesTime += [ syllable["time"] ]
    
    return result, syllablesTime

def _durationAvgOfPrevSyllableAccentConcatWords(textgrid):

    syllables = _durationOfEachSyllable(textgrid)

    phrase = []
    for word in syllables:
        for syllable in word:
            phrase += [syllable]

    result = []
    
    prevSyllable = ''
    for syllable in phrase:

        if syllable['text'][-1] == '*' and prevSyllable != '':
            result += [ prevSyllable['time'] ]

        logger.debug('prevSyllable: '+str(prevSyllable)+' syllable: '+str(syllable))
        prevSyllable = syllable

    # obtener solo el tiempo de cada silaba
    syllablesTime = []
    for word in syllables:
        for syllable in word:
            syllablesTime += [ syllable["time"] ]
    
    return result, syllablesTime

def SIL_prevSyllableAccent_norm(textgrid):
    """duration average of previous syllable accent normalized"""
    res = _durationAvgOfPrevSyllableAccent(textgrid)
    res = _normalizar(res[0], res[1])
    logger.info('SIL_prevSyllableAccent_norm: '+str(res))
    return res

def SIL_prevSyllableAccentConcatWords_norm(textgrid):
    """duration average of previous syllable accent normalized"""
    res = _durationAvgOfPrevSyllableAccentConcatWords(textgrid)
    res = _normalizar(res[0], res[1])
    logger.info('SIL_prevSyllableAccent_norm: '+str(res))
    return res

def SIL_prevSyllableAccent_normhd(textgrid):
    """duration average of previous syllable accent normalized half distribution"""
    res = _durationAvgOfPrevSyllableAccent(textgrid)
    res = _normalizar_halfdist(res[0], res[1])
    logger.info('SIL_prevSyllableAccent_normhd: '+str(res))
    return res

def SIL_prevSyllableAccentConcatWords_normhd(textgrid):
    """duration average of previous syllable accent normalized half distribution"""
    res = _durationAvgOfPrevSyllableAccentConcatWords(textgrid)
    res = _normalizar_halfdist(res[0], res[1])
    logger.info('SIL_prevSyllableAccent_normhd: '+str(res))
    return res

# Promedio de la silaba acentuada
def _durationAvgOfSyllableAccent(textgrid):

    syllables = _durationOfEachSyllable(textgrid)

    result = []

    for word in syllables:
        for syllable in word:

            if syllable['text'][-1] == '*':
                result += [ syllable['time'] ]

    # obtener solo el tiempo de cada silaba
    syllablesTime = []
    for word in syllables:
        for syllable in word:
            syllablesTime += [ syllable["time"] ]
    
    return result, syllablesTime     

def SIL_syllableAccent_norm(textgrid):
    """duration average of syllable accent normalized"""
    res = _durationAvgOfSyllableAccent(textgrid)
    res = _normalizar(res[0], res[1])
    logger.info('SIL_syllableAccent_norm: '+str(res))
    return res

def SIL_syllableAccent_normhd(textgrid):
    """duration average of syllable accent normalized half distribution"""
    res = _durationAvgOfSyllableAccent(textgrid)
    res = _normalizar_halfdist(res[0], res[1])
    logger.info('SIL_syllableAccent_normhd: '+str(res))
    return res

def _dummy(textgrid):
    return '8'

#==========================================================================

def _foundPattern(wordPattern, syllablePattern, textgrid):

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

    #logger.debug('wordInterval: '+str(wordInterval))

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
                            interval1['wordMin'] = float(interval['xmin'])
                            interval1['syllableMin'] = float(prevRow[0])
                            interval1['syllableMax'] = float(prevRow[1])
                            interval1['wordMax'] = float(interval['xmax'])
                            syllableIntervals += [interval1]
                
                prevRow = row

    return syllableIntervals

def timeSyllableIntervals(syllableIntervals):
    result = []
    for interval in syllableIntervals:
        result += [ interval['syllableMax'] - interval['syllableMin'] ]
    return result

#==========================================================================================

KT = {'wordPattern': r'.CT.', 'syllablePattern': r'kt' } 

def _durationAvgKT(textgrid):
    syllableIntervals = _foundPattern(KT['wordPattern'], KT['syllablePattern'], textgrid)
    result = timeSyllableIntervals(syllableIntervals)
    return result, _durationOfEachPhoneme(textgrid)

def FON_kt_norm(textgrid):
    """duration average of pattern kt normalized"""
    res = _durationAvgKT(textgrid)
    res = _normalizar(res[0], res[1])
    logger.info('FON_kt_norm: '+str(res))
    return res

def FON_kt_normhd(textgrid):
    """duration average of pattern kt normalized half distribution"""
    res = _durationAvgKT(textgrid)
    res = _normalizar_halfdist(res[0], res[1])
    logger.info('FON_kt_normhd: '+str(res))
    return res

#==========================================================================================

LL = {'wordPattern': r'LL.', 'syllablePattern': r'Z.'}

def _durationAvgLL(textgrid):
    syllableIntervals = _foundPattern(LL['wordPattern'], LL['syllablePattern'], textgrid)
    result = timeSyllableIntervals(syllableIntervals)
    return result, _durationOfEachPhoneme(textgrid)
    
def FON_ll_norm(textgrid):
    """duration average of pattern ll normalized"""
    res = _durationAvgLL(textgrid)
    res = _normalizar(res[0], res[1])    
    logger.info('FON_ll_norm: '+str(res))
    return res

def FON_ll_normhd(textgrid):
    """duration average of pattern ll normalized half distribution"""
    res = _durationAvgLL(textgrid)
    res = _normalizar_halfdist(res[0], res[1])    
    logger.info('FON_ll_normhd: '+str(res))
    return res

#==========================================================================================

RR = {'wordPattern': r'.RR.', 'syllablePattern': r'R.'}

def _durationAvgRR(textgrid):
    syllableIntervals = _foundPattern(RR['wordPattern'], RR['syllablePattern'], textgrid)
    result = timeSyllableIntervals(syllableIntervals)
    return result, _durationOfEachPhoneme(textgrid)

def FON_rr_norm(textgrid):
    """duration average of pattern rr normalized"""
    res = _durationAvgRR(textgrid)
    res = _normalizar(res[0], res[1])    
    logger.info('FON_rr_norm: '+str(res))
    return res

def FON_rr_normhd(textgrid):
    """duration average of pattern rr normalized half distribution"""
    res = _durationAvgRR(textgrid)
    res = _normalizar_halfdist(res[0], res[1])    
    logger.info('FON_rr_normhd: '+str(res))
    return res

#==========================================================================================

SC = {'wordPattern': r'.SC.', 'syllablePattern': r'hk'}

def _durationAvgSC(textgrid):
    syllableIntervals = _foundPattern(SC['wordPattern'], SC['syllablePattern'], textgrid)
    result = timeSyllableIntervals(syllableIntervals)
    return result, _durationOfEachPhoneme(textgrid)

def FON_sc_norm(textgrid):
    """duration average of pattern sc normalized"""
    res = _durationAvgSC(textgrid)
    res = _normalizar(res[0], res[1])    
    logger.info('FON_sc_norm: '+str(res))
    return res

def FON_sc_normhd(textgrid):
    """duration average of pattern sc normalized half distribution"""
    res = _durationAvgSC(textgrid)
    res = _normalizar_halfdist(res[0], res[1])    
    logger.info('FON_sc_normhd: '+str(res))
    return res