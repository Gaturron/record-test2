from textgrid import TextGrid, Tier
import phraseToAccents as phToAcc
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

#============================================================================

def duration(textgrid):
    logger.debug('duration: ')
    res = float(0)
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'words':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp':
                    res += float(row[1]) - float(row[0])
                logger.debug(row)
    res = round(res, digits)
    logger.debug('res: '+str(res))
    return res

def durationOfEachPhoneme(textgrid):
    logger.debug('durationOfEachPhoneme: ')
    zum = float(0)
    amount = 0
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'phones':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp' and row[2] != '':
                    zum += float(row[1]) - float(row[0])
                    amount += 1
                logger.debug(row)
    zum = round(zum, digits)
    amount = round(amount, digits)
    logger.debug('sum: '+str(zum)+' amount: '+str(amount)+' res: '+str(round(zum / amount, digits)))
    return round(zum / amount, digits)

def durationOfEachVowel(textgrid):
    logger.debug('durationOfEachVowel: ')
    zum = float(0)
    amount = 0
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'phones':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp' and string.lower(row[2]) in vowels:
                    zum += float(row[1]) - float(row[0])
                    amount += 1
                logger.debug(row)
    zum = round(zum, digits)
    amount = round(amount, digits)
    logger.debug('sum: '+str(zum)+' amount: '+str(amount)+' res: '+str(round(zum / amount, digits)))
    return round(zum / amount, digits)

def durationOfEachConsonant(textgrid):
    logger.debug('durationOfEachConsonant: ')
    zum = float(0)
    amount = 0
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'phones':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp' and string.lower(row[2]) in consonants:
                    zum += float(row[1]) - float(row[0])
                    amount += 1
                logger.debug(row)
    zum = round(zum, digits)
    amount = round(amount, digits)
    logger.debug('sum: '+str(zum)+' amount: '+str(amount)+' res: '+str(round(zum / amount, digits)))
    return round(zum / amount, digits)

def durationOfEachSyllable(textgrid):
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

def durationAvgOfPhonemeSFinal(textgrid):
    logger.debug('durationAvgOfPhonemeSFinal: ')

    wordsWithPhonemeS = []
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'words':
            for row in tier.simple_transcript:
                if str(row[2][-1]) == 'S':
                    # buscar entre esos valores de tiempo que es una /s/ final
                    wordsWithPhonemeS += [ {'xmin': row[0], 'xmax': row[1]} ]
    #logger.debug('wordsWithPhonemeS: '+str(wordsWithPhonemeS))

    #busco en esos intervalos que va a haber una /s/ final
    zum = float(0)
    amount = 0
    for word in wordsWithPhonemeS:
        for i, tier in enumerate(textgrid):
            if tier.nameid == 'phones':
                for row in tier.simple_transcript:
                    if str(row[2]) == 's' and word['xmin'] <= row[0] and row[1] <= word['xmax']:
                        zum += float(row[1]) - float(row[0])
                        amount += 1
    if amount == 0:
        return False
    else:
        zum = round(zum, digits)
        amount = round(amount, digits)
        logger.debug('sum: '+str(zum)+' amount: '+str(amount)+' res: '+str(round(zum / amount, digits)))
        return round(zum / amount, digits)

def durationAvgOfPrevSyllable(textgrid):

    logger.debug('durationAvgOfPrevSyllable:')
    syllables = durationOfEachSyllable(textgrid)

    zum = float(0)
    amount = 0

    prevSyllable = ''
    for word in syllables:
        for syllable in word:

            if syllable['text'][-1] == '*' and prevSyllable != '':
                zum += prevSyllable['time']
                amount += 1

            logger.debug('prevSyllable: '+str(prevSyllable)+' syllable: '+str(syllable))
            prevSyllable = syllable

    if amount == 0:
        return False
    else:
        zum = round(zum, digits)
        amount = round(amount, digits)
        logger.debug('sum: '+str(zum)+' amount: '+str(amount)+' res: '+str(round(zum / amount, digits)))
        return round(zum / amount, digits)

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
        duration, total = 0, 0
        for interval in syllableIntervals:
            duration += interval['syllableMax'] - interval['syllableMin']
            total += interval['wordMax'] - interval['wordMin'] 
        res = round(duration / total, digits) 
        logger.debug('Resultado: duration: '+str(duration)+' total: '+str(total)+' res: '+str(res))
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