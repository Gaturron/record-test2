import alignmentFilter as agmntFilter
import textgridExtractor as tgExtractor
import acousticExtractor as acExtractor

Path = '/home/fernando/Tesis/Prosodylab-Aligner-master/data1/'

def extract():

    pathList = agmntFilter.filter(Path)
    print pathList
    tgRes = tgExtractor.textgridsToAtt(pathList)
    print 'tgRes: '+ str(tgRes)
    acRes = acExtractor.extracts(pathList)
    print 'acRes: '+ str(acRes)

    res = {}
    for sample in tgRes.keys():
    	res[sample] = dict(tgRes[sample].items() + acRes[sample].items())

    res1 = {}
    for key in res.keys():
    	filename = key.split('/')[-1]
    	res[key]['place'] = filename.split('_')[0]
    	res1[filename] = res[key]

    print 'Res: '+ str(res1)

if __name__ == '__main__':
    extract()