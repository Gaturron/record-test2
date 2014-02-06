import alignmentFilter as agmntFilter
from textgridExtractor import textgridExtractor
from acousticExtractor import acousticExtractor
import diccToArff1 as dTA
import logging

Path = '/home/fernando/Tesis/Prosodylab-Aligner-master/data1/'
logging.basicConfig(level=logging.DEBUG)

def extract():

    attributesFilter = {
        'place': ('bsas', 'cba'), 'phrases': 'STRING', 
        'durationAvgKT': 'REAL', 'durationAvgLL': 'REAL', 
        'durationAvgRR': 'REAL', 'durationAvgSC': 'REAL',
        'duration': 'REAL', 'durationOfEachPhoneme': 'REAL',
        'durationOfEachVowel': 'REAL', 'durationOfEachConsonant': 'REAL',
        'durationAvgOfPhonemeSFinal': 'REAL',
        'durationAvgOfPrevSyllable': 'REAL', 
        'mfccAverageKT': ['REAL' for i in range(26)],
        'mfccMaxKT': ['REAL' for i in range(26)],
        'mfccMinKT': ['REAL' for i in range(26)],
        'mfccAverageLL': ['REAL' for i in range(26)],
        'mfccMaxLL': ['REAL' for i in range(26)],
        'mfccMinLL': ['REAL' for i in range(26)],
        'mfccAverageRR': ['REAL' for i in range(26)],
        'mfccMaxRR': ['REAL' for i in range(26)],
        'mfccMinRR': ['REAL' for i in range(26)],
        'mfccAverageSC': ['REAL' for i in range(26)],
        'mfccMaxSC': ['REAL' for i in range(26)],
        'mfccMinSC': ['REAL' for i in range(26)],
    }

    logger = logging.getLogger('Extract')
    logger.info('starting')

    pathList = agmntFilter.filter(Path)
    logger.debug('pathList: '+ str(pathList))

    tgExtractor = textgridExtractor(attributesFilter.keys())
    tgRes = tgExtractor.textgridsToAtt(pathList)
    logger.debug('tgRes: '+ str(tgRes))

    acExtractor = acousticExtractor(attributesFilter.keys())
    acRes = acExtractor.extracts(pathList)
    logger.debug('acRes: '+ str(acRes))

    res = {}
    for sample in tgRes.keys():
    	res[sample] = dict(tgRes[sample].items() + acRes[sample].items())

    res1 = {}
    for key in res.keys():
    	filename = key.split('/')[-1]
    	res[key]['place'] = filename.split('_')[0]
    	res1[filename] = res[key]

    logger.debug('Res: '+ str(res1))

    dTA.diccToArff(res1, 'test.arff', attributesFilter)

if __name__ == '__main__':
    extract()