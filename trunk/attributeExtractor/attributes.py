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

    phrase = ''
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'words':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp':
                    phrase += row[2] + ' '
    logger.debug('phrase: '+phrase.lower().strip())
    return phrase.lower().strip()

def _accents(textgrid):
    return phToAcc.getAccents(phrases(textgrid))

def _goThroughWithCondition(textgrid, nameTier, condition):
    # recorre el tier con nameTier y devuelve el array que cumple con los 
    # elementos de la condicion

    logger.debug("_goThroughWithCondition: ")
    result = []
    for i, tier in enumerate(textgrid):
        if tier.nameid == nameTier:
            for row in tier.simple_transcript:
                if condition(row):
                    result += [ float(row[1]) - float(row[0]) ]
                logger.debug(row)
    return result

def _durationOfEachSyllable(textgrid):
    logger.debug('durationOfEachSilabe: ')
    
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
    print "arraySample: "+str(arraySample)+" arrayTotal:"+str(arrayTotal)
    res = (np.average(arraySample) - np.average(arrayTotal)) / np.var(arrayTotal)
    print str(np.average(arraySample))+" - "+str(np.average(arrayTotal))+" / "+str(np.var(arrayTotal))
    return round(res, digits)

def _durationOfEachPhoneme(textgrid):
    f = lambda row: row[2] != 'sil' and row[2] != 'sp' and row[2] !=""
    res = _goThroughWithCondition(textgrid, "phones", f)
    return res

#============================================================================

def duration(textgrid):
    logger.debug("duration: ")
    f = lambda row: row[2] != 'sil' and row[2] != 'sp'
    res = _goThroughWithCondition(textgrid, "words", f)
    res = round(np.sum(res), digits)
    logger.debug('res: '+str(res))
    return res

def durationAvgOfEachPhoneme(textgrid):
    logger.debug("durationAvgOfEachPhoneme: ")
    f = lambda row: row[2] != 'sil' and row[2] != 'sp' and row[2] !=""
    res = _goThroughWithCondition(textgrid, "phones", f)
    res = round(np.average(res), digits)
    logger.debug('res: '+str(res))
    return res

def durationAvgOfEachVowel(textgrid):
    logger.debug('durationOfEachVowel: ')
    f = lambda row: row[2] != 'sil' and row[2] != 'sp' and string.lower(row[2]) in vowels 
    res = _goThroughWithCondition(textgrid, "phones", f)
    res = _normalizar(res, _durationOfEachPhoneme(textgrid))
    logger.debug('res: '+str(res))
    return res

def durationAvgOfEachConsonant(textgrid):
    logger.debug('durationOfEachConsonant: ')
    f = lambda row: row[2] != 'sil' and row[2] != 'sp' and string.lower(row[2]) in consonants 
    res = _goThroughWithCondition(textgrid, "phones", f)
    res = _normalizar(res, _durationOfEachPhoneme(textgrid))
    logger.debug('res: '+str(res))
    return res

def durationAvgOfPhonemeSFinal(textgrid):

    wordsWithPhonemeS = []
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'words':
            for row in tier.simple_transcript:
                if str(row[2][-1]) == 'S':
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

    if len(result) == 0:
        logger.debug("durationAvgOfPhonemeSFinal: None")
        return None
    else:
        res = _normalizar(result, _durationOfEachPhoneme(textgrid))
        logger.debug("durationAvgOfPhonemeSFinal: "+ str(result)+" "+str(len(result))+" = "+str(res))
        return res

# Regla 1: Localice la silaba acentuada y estirar la silaba anterior
def durationAvgOfPrevSyllable(textgrid):

    logger.debug('durationAvgOfPrevSyllable:')
    syllables = _durationOfEachSyllable(textgrid)

    result = []

    prevSyllable = ''
    for word in syllables:
        for syllable in word:

            if syllable['text'][-1] == '*' and prevSyllable != '':
                result += [ prevSyllable['time'] ]

            logger.debug('prevSyllable: '+str(prevSyllable)+' syllable: '+str(syllable))
            prevSyllable = syllable

    if len(result) == 0:
        return None
    else:
        logger.debug("result: "+ str(result)+" "+str(len(result)))
        res = round(np.average(result), digits)
        logger.debug('res: '+str(res))
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

    logger.debug('wordInterval: '+str(wordInterval))

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

    if syllableIntervals:
        return syllableIntervals
    else:
        return None

def _durationAvg(syllableIntervals):
    
    if isinstance(syllableIntervals, list): 
        result = []
        for interval in syllableIntervals:
            result += [ interval['syllableMax'] - interval['syllableMin'] ]
        res = round(np.average(result), digits)
        logger.debug('res: '+str(res))
        return res
    else:
        return None    

KT = {'wordPattern': r'.CT.', 'syllablePattern': r'kt' } 

def durationAvgKT(textgrid):
    logger.debug('durationAvgKT:')
    syllableIntervals = _foundPattern(KT['wordPattern'], KT['syllablePattern'], textgrid)
    return _durationAvg(syllableIntervals)

LL = {'wordPattern': r'LL.', 'syllablePattern': r'Z.'}

def durationAvgLL(textgrid):
    logger.debug('durationAvgLL:')
    syllableIntervals = _foundPattern(LL['wordPattern'], LL['syllablePattern'], textgrid)
    return _durationAvg(syllableIntervals)
    
RR = {'wordPattern': r'.RR.', 'syllablePattern': r'R.'}

def durationAvgRR(textgrid):
    logger.debug('durationAvgRR:')
    syllableIntervals = _foundPattern(RR['wordPattern'], RR['syllablePattern'], textgrid)
    return _durationAvg(syllableIntervals)

SC = {'wordPattern': r'.SC.', 'syllablePattern': r'hk'}

def durationAvgSC(textgrid):
    logger.debug('durationAvgSC:')
    syllableIntervals = _foundPattern(SC['wordPattern'], SC['syllablePattern'], textgrid)
    return _durationAvg(syllableIntervals)