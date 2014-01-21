from textgrid import TextGrid, Tier
import attributes as att
import os
import inspect

def textgridsToAtt(pathFolder):
    print 'Extractor de Textgrid - Directorio a analizar: '+str(pathFolder)

    filenames = os.listdir(pathFolder)
    attributesFiles = {}

    for filename in filenames:
        if (filename.endswith('.TextGrid')):
            attributesFiles[filename] = textgridToAtt(pathFolder+'/'+filename)

    return attributesFiles

def textgridToAtt(pathFile):
    print 'Textgrid a analizar: '+str(pathFile)

    file = open(pathFile, 'r')

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

    # vamos a agarrar todas las funciones de attributes
    # y ejecutarlas con el argumento tg 
    list_functions = inspect.getmembers(att, predicate=inspect.isfunction)
    for function in list_functions:
        function_name = function[0]
        # filtrar por si es function privada
        if function_name[0] != '_':
            res = getattr(att, function_name)(tg)
            attributesTg[function_name] = res

    return attributesTg

if __name__ == '__main__':
    print 'Prueba TextGrid: '
    print textgridsToAtt('/home/fernando/Tesis/Prosodylab-Aligner-master/data')