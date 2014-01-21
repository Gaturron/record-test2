from textgrid import TextGrid, Tier
import attributes as att
import os

path = '/home/fernando/Tesis/Prosodylab-Aligner-master/data'

print 'Extractor: '

filenames = os.listdir(path)

attributesFiles = {}

for filename in filenames:
    if (filename.endswith('.TextGrid')):
        file = open(path+'/'+filename, 'r')

        def replace_tab(s, tabstop = 4):
            result = str()
            for c in s:
                if c == '\t':
                    result += ' '*tabstop
                else:
                    result += c    
            return result

        data = replace_tab(file.read())
        tg = TextGrid(data)

        attributesTg = {}
        attributesTg['phrase'] = att.getPhrase(tg)
        attributesTg['accents'] = att.getAccents(tg)
        attributesTg['duration'] = att.duration(tg)
        attributesTg['durationOfEachPhoneme'] = att.durationOfEachPhoneme(tg)
        attributesTg['durationOfEachVowel'] = att.durationOfEachVowel(tg)
        attributesTg['durationOfEachConsonant'] = att.durationOfEachConsonant(tg)
        attributesTg['durationOfEachSyllable'] = att.durationOfEachSyllable(tg)
        attributesTg['durationAvgOfPhonemeSFinal'] = att.durationAvgOfPhonemeSFinal(tg)

        attributesFiles[filename] = attributesTg

print attributesFiles