import alignmentFilter as agmntFilter
from textgridExtractor import textgridExtractor
from acousticExtractor import acousticExtractor
import diccToArff1 as dTA
import logging

Path = '/home/fernando/Tesis/Prosodylab-Aligner-master/data1/'
logging.basicConfig(level=logging.DEBUG)

def extract():

    attributesFilter = {
        'place': ('bsas', 'cba'), 
        'phrases': 'STRING', 
        'duration': 'NUMERIC', 
        'user': 'NUMERIC',
        'phraseId': 'NUMERIC',
        'attempt': 'NUMERIC',

        'durationAvgKT': 'NUMERIC', 
        'durationAvgLL': 'NUMERIC', 
        'durationAvgRR': 'NUMERIC', 
        'durationAvgSC': 'NUMERIC',
        'durationAvgOfPhonemeSFinal': 'NUMERIC',
        
        'durationAvgOfEachPhoneme': 'NUMERIC',
        'durationAvgOfEachVowel': 'NUMERIC', 
        'durationAvgOfEachConsonant': 'NUMERIC',
        
        'durationAvgOfSyllableAccent': 'NUMERIC',
        'durationAvgOfPrevSyllableAccent': 'NUMERIC'
        
        #, 
        # 'mfccAverageKT': ['NUMERIC' for i in range(26)],
        # 'mfccMaxKT': ['NUMERIC' for i in range(26)],
        # 'mfccMinKT': ['NUMERIC' for i in range(26)],
        # 'mfccAverageLL': ['NUMERIC' for i in range(26)],
        # 'mfccMaxLL': ['NUMERIC' for i in range(26)],
        # 'mfccMinLL': ['NUMERIC' for i in range(26)],
        # 'mfccAverageRR': ['NUMERIC' for i in range(26)],
        # 'mfccMaxRR': ['NUMERIC' for i in range(26)],
        # 'mfccMinRR': ['NUMERIC' for i in range(26)],
        # 'mfccAverageSC': ['NUMERIC' for i in range(26)],
        # 'mfccMaxSC': ['NUMERIC' for i in range(26)],
        # 'mfccMinSC': ['NUMERIC' for i in range(26)],
    }

    logger = logging.getLogger('Extract')
    logger.info('starting')

    pathList = agmntFilter.filter(Path)
    #logger.debug('pathList: '+ str(pathList))

    tgExtractor = textgridExtractor(attributesFilter.keys())
    tgRes = tgExtractor.textgridsToAtt(pathList)
    #logger.debug('tgRes: '+ str(tgRes))

    #acExtractor = acousticExtractor(attributesFilter.keys())
    #acRes = acExtractor.extracts(pathList)
    #logger.debug('acRes: '+ str(acRes))

    res = {}
    for sample in tgRes.keys():
    	#res[sample] = dict(tgRes[sample].items() + acRes[sample].items())
        res[sample] = dict(tgRes[sample].items())

    res1 = {}
    for key in res.keys():
    	filename = key.split('/')[-1]
    	res[key]['place'] = filename.split('_')[0]
        res[key]['user'] = filename.split('_')[1][1:]
        res[key]['phraseId'] = filename.split('_')[2][1:]
        res[key]['attempt'] = filename.split('_')[3][1:]
    	res1[filename] = res[key]

    logger.debug('Res: '+ str(res1))

    dTA.diccToArff(res1, 'testNew.arff', attributesFilter)

if __name__ == '__main__':
    extract()