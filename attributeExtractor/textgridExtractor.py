from textgrid import TextGrid, Tier
import attributes as att
import os
import inspect
import logging

logger = logging.getLogger('textgridExtractor')

#TODO: cambiar de nombres a las funciones

class textgridExtractor(object):

    def __init__(self, attributesFilter):
        self.attributesFilter = attributesFilter

    def textgridsToAtt(self, param):
        if isinstance(param, str):
            return self._textgridsToAttFromPathFolder(param)
        elif isinstance(param, list):
            return self._textgridsToAttFromPathFileList(param)

    def _textgridsToAttFromPathFileList(self, pathFileList):
        logger.info('Extractor de Textgrid - Lista de pathFiles')

        attributesFiles = {}

        for pathFile in pathFileList:
            filename = pathFile+'.TextGrid'
            if os.path.isfile(filename):
                attributesFiles[pathFile] = self.textgridToAtt(filename)

        return attributesFiles

    def _textgridsToAttFromPathFolder(self, pathFolder):
        logger.info('Extractor de Textgrid - Directorio a analizar: '+str(pathFolder))

        filenames = os.listdir(pathFolder)
        attributesFiles = {}

        for filename in filenames:
            if (filename.endswith('.TextGrid')):
                attributesFiles[filename] = textgridToAtt(pathFolder+'/'+filename)

        return attributesFiles

    def textgridToAtt(self, pathFile):
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

        def info(textgrid):
            phones = []
            for i, tier in enumerate(textgrid):
                if tier.nameid == 'words':
                    for row in tier.simple_transcript:
                        if row[2] != 'sil' and row[2] != 'sp' and row[2] != '':
                            phones += [ row ]
            logger.info(str(phones))

            phrase = ''
            for i, tier in enumerate(textgrid):
                if tier.nameid == 'words':
                    for row in tier.simple_transcript:
                        if row[2] != 'sil' and row[2] != 'sp':
                            phrase += row[2] + ' '
            logger.info(str(phrase.lower().strip()))

        info(tg)

        attributesTg = {}

        # vamos a agarrar todas las funciones de attributes
        # y ejecutarlas con el argumento tg 
        list_functions = inspect.getmembers(att, predicate=inspect.isfunction)
        for function in list_functions:
            function_name = function[0]
            # filtrar por si es function privada
            if function_name[0] != '_' and function_name in self.attributesFilter:
                res = getattr(att, function_name)(tg)
                attributesTg[function_name] = res

        logger.info('=========================================================================')
        return attributesTg

if __name__ == '__main__':
    logger.info('Prueba TextGrid: ')
    logging.basicConfig(level=logging.DEBUG)
    tgExtractor = textgridExtractor({ 'FON_sc_norm': 'NUMERIC',
                                      'FON_sc_normhd': 'NUMERIC'
                                      })
    logger.info(tgExtractor.textgridToAtt('/home/fernando/Tesis/Prosodylab-Aligner-master/data1.complete/bsas_u30_t5_a3.TextGrid'))