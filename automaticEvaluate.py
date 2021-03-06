# coding:utf-8
import os
import support as myLib
SystemPathSeperator = '\\'

def sample_eval(evaluateTool, resultNamesFile, qrelFile, resultFiles, evalFiles):
    fpResultNamesFile = open(resultNamesFile)
    
    for line in fpResultNamesFile.readlines():
        filename = str(line).strip()
        cmdStr = evaluateTool + SystemPathSeperator + 'sample_eval.pl -q ' + qrelFile + ' ' + resultFiles + SystemPathSeperator + filename + ' > ' + evalFiles + SystemPathSeperator + filename + '.eval'
        print cmdStr
        ret = os.popen(cmdStr).read().strip()
    return 0

def sampleEvalOnFolder(evaluateTool, qrelFile, resultFiles, evalFiles):
    files = myLib.listDir(resultFiles)
    
    for file in files:
        filename = file[file.rfind(SystemPathSeperator) + 1:]
        cmdStr = evaluateTool + SystemPathSeperator + 'sample_eval.pl -q ' + qrelFile + ' ' + resultFiles + SystemPathSeperator + filename + ' > ' + evalFiles + SystemPathSeperator + filename + '.eval'
        print cmdStr
        ret = os.popen(cmdStr).read().strip()
    return 0

def terc_eval(evaluateTool, resultNamesFile, qrelFile, resultFiles, evalFiles):
    fpResultNamesFile = open(resultNamesFile)
    SystemPathSeperator = '\\'
    for line in fpResultNamesFile.readlines():
        filename = str(line).strip()
        cmdStr = evaluateTool + SystemPathSeperator + 'terc_eval.pl -c -q ' + qrelFile + ' ' + resultFiles + SystemPathSeperator + filename + ' > ' + evalFiles + SystemPathSeperator + filename + '.eval'
        print cmdStr
        ret = os.popen(cmdStr).read().strip()
    return 0 

if __name__ == "__main__": 
    sample_eval('I:\\trec2016\\testMethodIn2015Data',
                'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\toBeEvaluatedResults\\queryExpansionWeight.txt',
                'I:\\trec2016\\testMethodIn2015Data\\qrel2015\\qrels-sampleval-2015.txt',
                'I:\\trec2016\\testMethodIn2015Data\\queryExpansionWeight\\results',
                'I:\\trec2016\\testMethodIn2015Data\\queryExpansionWeight\\eval')
    
    #terc_eval这个文件有问题，好像不是perl文件
    
    #terc_eval('I:\\trec2016\\testMethodIn2015Data',
     #         'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\resultNames.txt',
      #        'I:\\trec2016\\testMethodIn2015Data\\qrel2015\\qrels-treceval-2015.txt',
       #       'I:\\trec2016\\testMethodIn2015Data\\result2015',
        #      'I:\\trec2016\\testMethodIn2015Data\\evaluateResultMAP20152')
