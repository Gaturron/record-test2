import alignmentFilter as agmntFilter
import textgridExtractor as tgExtractor
import acousticExtractor as acExtractor
import diccToArff as dTA
import logging

Path = '/home/fernando/Tesis/Prosodylab-Aligner-master/data1/'
logging.basicConfig(level=logging.DEBUG)

def extract():

    logger = logging.getLogger('Extract')
    logger.info('starting')

    pathList = agmntFilter.filter(Path)
    logger.debug('pathList: '+ str(pathList))

    tgRes = tgExtractor.textgridsToAtt(pathList)
    logger.debug('tgRes: '+ str(tgRes))
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

    dTA.diccToArff(res1, 'test.arff')


if __name__ == '__main__':
    extract()