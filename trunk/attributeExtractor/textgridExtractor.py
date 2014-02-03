from textgrid import TextGrid, Tier
import attributes as att
import os
import inspect
import logging

logger = logging.getLogger('textgridExtractor')

#TODO: cambiar de nombres a las funciones

def textgridsToAtt(param):
    if isinstance(param, str):
        return _textgridsToAttFromPathFolder(param)
    elif isinstance(param, list):
        return _textgridsToAttFromPathFileList(param)

def _textgridsToAttFromPathFileList(pathFileList):
    logger.info('Extractor de Textgrid - Lista de pathFiles')

    attributesFiles = {}

    for pathFile in pathFileList:
        filename = pathFile+'.TextGrid'
        if os.path.isfile(filename):
            attributesFiles[pathFile] = textgridToAtt(filename)

    return attributesFiles

def _textgridsToAttFromPathFolder(pathFolder):
    logger.info('Extractor de Textgrid - Directorio a analizar: '+str(pathFolder))

    filenames = os.listdir(pathFolder)
    attributesFiles = {}

    for filename in filenames:
        if (filename.endswith('.TextGrid')):
            attributesFiles[filename] = textgridToAtt(pathFolder+'/'+filename)

    return attributesFiles

def textgridToAtt(pathFile):
    logger.info('Textgrid a analizar: '+str(pathFile))

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

    # Lista de nombre de las funciones de atributos 
    # que se van a calcular
    attributesFilter = ['phrases', 'durationAvgKT', 'durationAvgRR']

    attributesTg = {}

    # vamos a agarrar todas las funciones de attributes
    # y ejecutarlas con el argumento tg 
    list_functions = inspect.getmembers(att, predicate=inspect.isfunction)
    for function in list_functions:
        function_name = function[0]
        # filtrar por si es function privada
        if function_name[0] != '_' and function_name in attributesFilter:
            res = getattr(att, function_name)(tg)
            attributesTg[function_name] = res

    return attributesTg

if __name__ == '__main__':
    logger.info('Prueba TextGrid: ')
    logger.info(textgridsToAtt('/home/fernando/Tesis/Prosodylab-Aligner-master/data1'))