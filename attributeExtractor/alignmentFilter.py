import re

ProsodylabPath = '/home/fernando/Tesis/Prosodylab-Aligner-master/'
umbral = -60
# umbral debe ser negativo
# mas cercano a 0 significa mejor alineado

def filter():
    file = open(ProsodylabPath+'data/.SCORES.txt', 'r')
    lines = file.readlines()

    paths = []
    for line in lines:
        line = re.split('\t|\n', line)[:-1]
        if float(line[1]) > umbral: 
            paths += [line]
            print line
    
    file.close()

    return paths

if __name__ == '__main__':
    filter()