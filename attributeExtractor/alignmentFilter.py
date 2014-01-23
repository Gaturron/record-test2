import re

umbral = -60
# umbral debe ser negativo
# mas cercano a 0 significa mejor alineado

def filter(pathFolder):
    file = open(pathFolder+'.SCORES.txt', 'r')
    lines = file.readlines()

    paths = []
    for line in lines:
        line = re.split('\t|\n', line)[:-1]
        if float(line[1]) > umbral: 
            print line
            paths += [ line[0].strip('.wav') ]
    
    file.close()

    return paths

if __name__ == '__main__':
    print filter('/home/fernando/Tesis/Prosodylab-Aligner-master/data1/')