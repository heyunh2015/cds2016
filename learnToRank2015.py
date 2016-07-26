# coding:utf-8
import support as myLib
import operator, automaticEvaluate, statisticResult
import math as math

def combine_score(filename, b, predictionFile, new_filename, topN):#将模型分数与原始分数相加
    fp=open(filename)
    lines=fp.readlines()
    FinalResultDic = {}
    
    fpPredict = open(predictionFile)
    predictList = []
    for line in fpPredict.readlines():
        predictScore = float(line.strip())
        predictList.append(predictScore)
    
    predictList = myLib.uniformMaxMin(predictList)
    
    resultIndex = 0    
    for line in lines:
        lineArr=line.strip().split(' ')
        queryId = lineArr[0]
        documentId = lineArr[1]
        score = lineArr[3]
        if queryId not in FinalResultDic:
            FinalResultDic[lineArr[0]] = {}
        if documentId not in FinalResultDic[queryId]:
            FinalResultDic[queryId][documentId] = float(score)*(1.0-b) + predictList[resultIndex]*b
        resultIndex += 1
    
    combineResultRerank=''        
    for queryId in FinalResultDic:
        rankIndex=0
        for item in sorted(FinalResultDic[queryId].iteritems(), key=operator.itemgetter(1), reverse=True)[0:topN]:
            combineResultRerank += str(queryId)+' '+'Q0'+' '+str(item[0])+' '+str(rankIndex)+' '+str(item[1]).replace('\n','')+' '+'ecnuEn'+'\n'
            rankIndex += 1
    
    fpWrite=open(new_filename,'w')
    fpWrite.write(combineResultRerank)
    fpWrite.close()
    return 0

def resultToQidDidRankScoreDic(resultFile):
    fp = open(resultFile)
    lines = fp.readlines() 
    
    QidDidRankScoreDic = {}  
    for line in lines:
        lineArr=line.split(' ')
        queryId = lineArr[0]
        doucmentId = lineArr[2]
        score = lineArr[4]
        rank = lineArr[3]
        if queryId not in QidDidRankScoreDic:
            QidDidRankScoreDic[queryId]={}
        if doucmentId not in QidDidRankScoreDic[queryId]:
            QidDidRankScoreDic[queryId][doucmentId] = [rank, score]
    
    return QidDidRankScoreDic

def qrelToLabelDic(qrelFile):
    fp = open(qrelFile)
    lines = fp.readlines() 
    
    QidDidRankingDic = {}  
    for line in lines:
        lineArr=line.split('\t')
        queryId = lineArr[0]
        doucmentId = lineArr[2]
        ranking = lineArr[3]
        if queryId not in QidDidRankingDic:
            QidDidRankingDic[queryId]={}
        if doucmentId not in QidDidRankingDic[queryId]:
            QidDidRankingDic[queryId][doucmentId] = ranking
    
    return QidDidRankingDic

def addFeature(baseQidDidRankScoreDic, QidDidRankScoreDic):
    for queryId in baseQidDidRankScoreDic:
        for documentId in baseQidDidRankScoreDic[queryId]:
            if documentId in QidDidRankScoreDic[queryId]:
                #1
                baseQidDidRankScoreDic[queryId][documentId].extend(QidDidRankScoreDic[queryId][documentId])
            else:
                
                baseQidDidRankScoreDic[queryId][documentId].extend(['10000', '0.0'])
    return baseQidDidRankScoreDic

def addLabel(baseQidDidRankScoreDic, QidDidRankingDic):
    #featureMatrixLabelDic = {}
    for queryId in baseQidDidRankScoreDic:
        removeFeatureList = []
     #   if queryId not in featureMatrixLabelDic:
      #      featureMatrixLabelDic[queryId] = {}
        for documentId in baseQidDidRankScoreDic[queryId]:
            if documentId in QidDidRankingDic[queryId]:
                #1
                baseQidDidRankScoreDic[queryId][documentId].extend(QidDidRankingDic[queryId][documentId])
            else:
                removeFeatureList.append(documentId)
                #baseQidDidRankScoreDic[queryId][documentId].extend(['0'])
        for documentId in removeFeatureList:
            baseQidDidRankScoreDic[queryId].pop(documentId)
    return baseQidDidRankScoreDic

def rankDidRankScoreDicByQid(baseQidDidRankScoreDic):
    QidDidRankScoreDicOrdered = []
    queryIdDic = {}
    for queryId in baseQidDidRankScoreDic:
        queryIdDic[int(queryId)] = 1
    for item in sorted(queryIdDic.iteritems(), key=operator.itemgetter(0), reverse=False):
        #print str(item[0])
        QidDidRankScoreDicOrdered.append(baseQidDidRankScoreDic[str(item[0])])
    
    return QidDidRankScoreDicOrdered

def generateVectorMatrix(baseFile, fileNameList):
    baseQidDidRankScoreDic = resultToQidDidRankScoreDic(baseFile)
    QidDidRankScoreDicOrdered = []
    for file in fileNameList:
        QidDidRankScoreDic = resultToQidDidRankScoreDic(file)
        baseQidDidRankScoreDic = addFeature(baseQidDidRankScoreDic, QidDidRankScoreDic)
    QidDidRankScoreDicOrdered = rankDidRankScoreDicByQid(baseQidDidRankScoreDic)
    return QidDidRankScoreDicOrdered
  
def generateVectorMatrixLabel(baseFile, fileNameList, qrelFile):
    baseQidDidRankScoreDic = resultToQidDidRankScoreDic(baseFile)
    QidDidRankScoreDicOrdered = []
    for file in fileNameList:
        QidDidRankScoreDic = resultToQidDidRankScoreDic(file)
        baseQidDidRankScoreDic = addFeature(baseQidDidRankScoreDic, QidDidRankScoreDic)
    labelDic = qrelToLabelDic(qrelFile)
    baseQidDidRankScoreDic = addLabel(baseQidDidRankScoreDic, labelDic)
    QidDidRankScoreDicOrdered = rankDidRankScoreDicByQid(baseQidDidRankScoreDic)
    return QidDidRankScoreDicOrdered
    
def saveVectorMatrix(QidDidRankScoreDicOrdered, featureMatrixFile):   
    featureMatrix = ''
    for queryId in range(len(QidDidRankScoreDicOrdered)):
        for documentId in QidDidRankScoreDicOrdered[queryId]:
            vectorLength = len(QidDidRankScoreDicOrdered[queryId][documentId])
            featureVector = ''
            featureVector += str(queryId+1) + ' ' + documentId + ' '
            for feature in range(vectorLength):
                featureVector += QidDidRankScoreDicOrdered[queryId][documentId][feature] + ' '
            featureMatrix += featureVector.strip() + '\n'
    myLib.saveFile(featureMatrix, featureMatrixFile)
    return 0

def SvmRankFormat(filename,svmRankFile, hasLabel):
    fp=open(filename)
    lines=fp.readlines()
    if hasLabel == 'noLabel':
        file_new=''
        for line in lines:
            lineArr=line.strip().split(' ')
            file_new+='0'+' '+'qid:'+lineArr[0]+' 1:'+lineArr[3]+' 2:'+lineArr[5]+' 3:'+lineArr[7]+' 4:'+lineArr[9]+'\n'
    else:
        file_new=''
        for line in lines:
            lineArr=line.strip().split(' ')
            file_new+=lineArr[10]+' '+'qid:'+lineArr[0]+' 1:'+lineArr[3]+' 2:'+lineArr[5]+' 3:'+lineArr[7]+' 4:'+lineArr[9]+'\n'
    fp_w=open(svmRankFile,'w')
    fp_w.write(file_new)
    return 0

if __name__ == "__main__": 
    #filesNameList = myLib.getResultFileNameFromFile('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData', 
     #                                        'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\toBeCombinedResults\\toBeCombinedResults.txt')
    #QidDidRankScoreDicOrdered = generateVectorMatrix('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\LM_LGD_BM25_1200.res',
     #                   filesNameList)
    #saveVectorMatrix(QidDidRankScoreDicOrdered, 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\testFeatureMatrix\\LM_LGD_BM25_score.feature')
    #SvmRankFormat('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\testFeatureMatrix\\LM_LGD_BM25_score.feature',
     #                       'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\testFeatureMatrixSvm\\LM_LGD_BM25_score.featureSvm',
      #                      'noLabel')
    
    #filesNameList = myLib.getResultFileNameFromFile('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014Results', 
     #                                        'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\toBeAddAsFeature\\toBeAddAsFeature.txt')
    #QidDidRankScoreDicOrdered = generateVectorMatrixLabel('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\LM_LGD_BM25_1200.res',
     #                   filesNameList,
      #                  'I:\\trec2016\\testMethodIn2015Data\\qrel2014\\qrels-treceval-2014.txt')
    #saveVectorMatrix(QidDidRankScoreDicOrdered, 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\trainFeatureMatrix\\LM_LGD_BM25_score.feature')
    #SvmRankFormat('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\trainFeatureMatrix\\LM_LGD_BM25_score.feature',
     #                       'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\trainFeatureMatrixSvm\\LM_LGD_BM25_score.featureTrainSvm',
      #                      'haveLabel')
     
    #for i in range(1,20):
     #   combine_score('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\testFeatureMatrix\\LM_LGD_BM25_score.feature', 
      #                0.05*i, 
       #               'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\prediction\\predictions.2015LM_LGD_BM25',
        #              'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\finalResult\\LM_LGD_BM\\2015LM_LGD_BM25Final'+str(0.05*i)+'.txt',
         #             1000)
        #print '2015LM_LGD_BM25Final'+str(0.05*i)+'.txt'
        
   # automaticEvaluate.sampleEvalOnFolder('I:\\trec2016\\testMethodIn2015Data',
    #            'I:\\trec2016\\testMethodIn2015Data\\qrel2015\\qrels-sampleval-2015.txt',
     #           'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\finalResult\\LM_LGD_BM',
      #          'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\eval\\LM_LGD_BM')
      
   filesNameList = myLib.getResultFileNameFromFolder('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\eval\\LM_LGD_BM')
   resCsv = statisticResult.extractMetricsToString(filesNameList, ['infNDCG','iP10'])
   myLib.saveFile(resCsv, 'I:\\trec2016\\testMethodIn2015Data\\statisticResult2015\\learnToRankBM25LmLgdB2015.csv')
   rankResultMetric = statisticResult.rankResults(filesNameList, 'infNDCG')
   myLib.saveFile(rankResultMetric, 'I:\\trec2016\\testMethodIn2015Data\\statisticResult2015\\learnToRankBM25LmLgdB2015rank.txt')