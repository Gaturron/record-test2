from textgrid import TextGrid, Tier
import mfccExtractor as mfccExt
import acousticAttributes as acAtt
import os
import inspect
import logging

logger = logging.getLogger('acousticExtractor')

class acousticExtractor(object):

    def __init__(self, attributesFilter):
        self.attributesFilter = attributesFilter

    def extracts(self, pathFileList):
        logger.info('Extractor de atributos acusticos - Lista de pathFiles')

        attributesFiles = {}

        for pathFile in pathFileList:
            attributesFiles[pathFile] = self.extract(pathFile)

        return attributesFiles    

    def extract(self, pathFile):
        logger.info('Archivo a analizar: '+str(pathFile))

        # Analizo textgrid
        tg = self._extractTextgrid(pathFile+'.TextGrid')

        # Analizo mfcc
        #mfcc = self._extractMfcc(pathFile+'.wav')
        mfcc = None

        attributesAc = {}

        # vamos a agarrar todas las funciones de acousticAttributes
        # y ejecutarlas con el argumento 
        list_functions = inspect.getmembers(acAtt, predicate=inspect.isfunction)
        for function in list_functions:
            function_name = function[0]
            # filtrar por si es function privada
            if function_name[0] != '_' and function_name in self.attributesFilter:
                res = getattr(acAtt, function_name)(tg, mfcc)
                attributesAc[function_name] = res

        return attributesAc

    def _extractTextgrid(self, pathFile):
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
        return TextGrid(data)

    def _extractMfcc(self, pathFile):
        logger.info('Wav a analizar: '+str(pathFile))

        return mfccExt.wavToMfcc(pathFile)