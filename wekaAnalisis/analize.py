import sys

import java.io.FileReader as FileReader
import java.lang.StringBuffer as StringBuffer
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.util.Random as Random

import weka.core.Instances as Instances
import weka.filters.Filter as Filter
import weka.core.Range as Range
import weka.classifiers.trees.J48 as J48
import weka.classifiers.rules.JRip as JRip
import weka.filters.unsupervised.attribute.Remove as Remove
import weka.classifiers.Evaluation as Evaluation

# load data file
file = FileReader("/home/fernando/Tesis/record-test2/attributeExtractor/test1.numeric.arff")
data = Instances(file)
data.setClassIndex(data.numAttributes() - 1)

# Calculando el Baseline
# ======================

listAttribute = []
listAttribute.append(data.attribute('durationAvgOfPrevSyllable').index())
listAttribute.append(data.attribute('duration').index())
listAttribute.append(data.attribute('place').index())

remove = Remove()
remove.setAttributeIndicesArray(listAttribute)
remove.setInvertSelection(True) 
#True: para que mantenga los atributos definidos
remove.setInputFormat(data)
data = Filter.useFilter(data, remove)
data.setClassIndex(data.attribute('place').index())

jrip = JRip()
jrip.setDebug(True)
jrip.setOptions(['-F 3', '-N 2.0', '-O 2', '-S 1'])

evaluation = Evaluation(data)
folds = 10

jrip.buildClassifier(data)

rand = Random(1); 
evaluation.crossValidateModel(jrip, data, folds, rand );

print "--> Generated model:\n"
print jrip

print "--> Evaluation:\n"
print evaluation.toSummaryString()
print evaluation.toMatrixString()