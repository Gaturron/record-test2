import sys

import java.io.FileReader as FileReader
import java.lang.StringBuffer as StringBuffer
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.util.Random as Random

import weka.core.Instances as Instances
import weka.core.Utils as utils
import weka.filters.Filter as Filter
import weka.core.Range as Range

import weka.classifiers.trees.J48 as J48
import weka.classifiers.rules.ZeroR as ZeroR
import weka.classifiers.rules.JRip as JRip
import weka.classifiers.bayes.NaiveBayes as NaiveBayes
import weka.classifiers.functions.SMO as functionsSMO

import weka.filters.unsupervised.attribute.Remove as Remove
import weka.filters.supervised.attribute.AttributeSelection as AttributeSelection

import weka.classifiers.Evaluation as Evaluation

import weka.classifiers.meta.AttributeSelectedClassifier as AttributeSelectedClassifier

import weka.attributeSelection.CfsSubsetEval as CfsSubsetEval
import weka.attributeSelection.InfoGainAttributeEval as InfoGainAttributeEval

import weka.attributeSelection.GreedyStepwise as GreedyStepwise
import weka.attributeSelection.Ranker as Ranker

filepath = "/home/fernando/Tesis/record-test2/attributeExtractor/tests/test2014-05-08/extractionTotal.arff"

file = FileReader(filepath)
data = Instances(file)
data.setClassIndex(data.attribute('place').index())

classifier = AttributeSelectedClassifier()
eval = InfoGainAttributeEval()

eval.buildEvaluator(data)

infogainscores = []
for i in range(0, data.numAttributes()):
    t_attr = data.attribute(i);
    infogain  = eval.evaluateAttribute(i);
    infogainscores = infogainscores + [(t_attr, infogain)];
print infogainscores

print eval.getRevision() 

search = Ranker()
#search.setSearchBackwards(True)
#base = J48()
#classifier.setClassifier(base)
classifier.setEvaluator(eval)
classifier.setSearch(search)
print classifier.globalInfo()

evaluation = Evaluation(data)
evaluation.crossValidateModel(classifier, data, 10, Random(1))
print evaluation.toSummaryString()