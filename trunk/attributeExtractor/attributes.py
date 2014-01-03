from textgrid import TextGrid, Tier
import phraseToAccents as phToAcc
import string

vowels = ['a', 'e', 'i', 'o', 'u']

# calculate the consonants
consonants = []
for l in string.lowercase:
    if not l in vowels: 
        consonants += [l]

def duration(textgrid):
    print 'duration: '
    res = float(0)
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'words':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp':
                    res += float(row[1]) - float(row[0])
                print row
    print 'res: '+str(res)
    return res

def durationOfEachPhoneme(textgrid):
    print 'durationOfEachPhoneme: '
    zum = float(0)
    amount = 0
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'phones':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp' and row[2] != '':
                    zum += float(row[1]) - float(row[0])
                    amount += 1
                print row
    print 'sum: '+str(zum)+' amount: '+str(amount)+' res: '+str(zum / amount)
    return zum / amount

def durationOfEachVowel(textgrid):
    print 'durationOfEachVowel: '
    zum = float(0)
    amount = 0
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'phones':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp' and string.lower(row[2]) in vowels:
                    zum += float(row[1]) - float(row[0])
                    amount += 1
                print row
    print 'sum: '+str(zum)+' amount: '+str(amount)+' res: '+str(zum / amount)
    return zum / amount

def durationOfEachConsonant(textgrid):
    print 'durationOfEachConsonant: '
    zum = float(0)
    amount = 0
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'phones':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp' and string.lower(row[2]) in consonants:
                    zum += float(row[1]) - float(row[0])
                    amount += 1
                print row
    print 'sum: '+str(zum)+' amount: '+str(amount)+' res: '+str(zum / amount)
    return zum / amount

def getPhrase(textgrid):
    phrase = ''
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'words':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp':
                    phrase += row[2] + ' '
    return phrase.lower().strip()

def getAccents(textgrid):
    return phToAcc.getAccents(getPhrase(textgrid))

def durationOfEachSyllable(textgrid):
    print 'durationOfEachSilabe: '
    
    phones = []
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'phones':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp' and row[2] != '':
                    phones += [ {'text': row[2], 'time': float(row[1]) - float(row[0])} ]

    #print 'phones: '+str(phones)
    
    silabes = []
    for w in getAccents(textgrid):
        silabes += w
    
    #print 'silabes: '+str(silabes)

    silabes2 = []
    index = 0
    for silabe in silabes:
        silabe_time = 0
        for char in silabe:
            if char != '*':
                silabe_time += phones[index]['time']
                index += 1
        silabes2 += [ {'text': silabe, 'time': silabe_time} ]

    #print 'silabes2: '+str(silabes2)

    silabes3 = []
    index = 0
    for word in getAccents(textgrid):
        w = []
        for silabe in word:
            w += [ silabes2[index] ]
            index += 1
        silabes3 += [ w ]

    #print 'silabes3: '+ str(silabes3)

    return silabes3

def durationAvgOfPhonemeSFinal(textgrid):
    print 'durationAvgOfPhonemeSFinal: '

    wordsWithPhonemeS = []
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'words':
            for row in tier.simple_transcript:
                if str(row[2][-1]) == 'S':
                    # buscar entre esos valores de tiempo que es una /s/ final
                    wordsWithPhonemeS += [ {'xmin': row[0], 'xmax': row[1]} ]
    #print 'wordsWithPhonemeS: '+str(wordsWithPhonemeS)

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
        print 'sum: '+str(zum)+' amount: '+str(amount)+' res: '+str(zum / amount)
        return zum / amount

def dummy(textgrid):
    return '8'