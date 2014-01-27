import alignmentFilter as agmntFilter
import textgridExtractor as tgExtractor
import acousticExtractor as acExtractor

Path = '/home/fernando/Tesis/Prosodylab-Aligner-master/data1/'

def extract():

    pathList = agmntFilter.filter(Path)
    print pathList
    #res = tgExtractor.textgridsToAtt(pathList)
    #print res
    res = acExtractor.extracts(pathList)
    print res

if __name__ == '__main__':
    extract()