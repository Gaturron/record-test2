import re
import logging

#umbral = -65
umbral = -150
# umbral debe ser negativo
# mas cercano a 0 significa mejor alineado

def filter(pathFolder):
    logger = logging.getLogger('AlignmentFilter')
    logger.info('starting')

    file = open(pathFolder+'.SCORES.txt', 'r')
    lines = file.readlines()

    logger.debug('Files applying the filter:')

    paths = []
    for line in lines:
        line = re.split('\t|\n', line)[:-1]
        if float(line[1]) > umbral: 
            logger.debug(line)
            paths += [ line[0].strip('.wav') ]
    
    file.close()

    logger.info('end')
    return paths

if __name__ == '__main__':
    print filter('/home/fernando/Tesis/Prosodylab-Aligner-master/data1/')