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
        data = replace_tab(file.read())
        tg = TextGrid(data)

        for i, tier in enumerate(tg):
            print "\n***"
            print "Tier:", i + 1
            print tier

        attributesTg = {}
        attributesTg['duration'] = att.duration(tg)
        attributesTg['dummy'] = att.dummy(tg)

        attributesFiles[filename] = attributesTg

print attributesFiles        