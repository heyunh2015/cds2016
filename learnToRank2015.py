# coding:utf-8
import support as myLib
import operator, automaticEvaluate, statisticResult
import math as math
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

def combineOriginalScoreAndPredcition(filename, b, predictionFile, new_filename, topN):#将模型分数与原始分数相加
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
        lineArr=line.split(' ')
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

def generateFeatureMatrix(baseFile, fileNameList):
    baseQidDidRankScoreDic = resultToQidDidRankScoreDic(baseFile)
    QidDidRankScoreDicOrdered = []
    for file in fileNameList:
        QidDidRankScoreDic = resultToQidDidRankScoreDic(file)
        baseQidDidRankScoreDic = addFeature(baseQidDidRankScoreDic, QidDidRankScoreDic)
    QidDidRankScoreDicOrdered = rankDidRankScoreDicByQid(baseQidDidRankScoreDic)
    return QidDidRankScoreDicOrdered
  
def generateFeatureMatrixLabel(baseFile, fileNameList, qrelFile):
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

def selectTrainSample(featureMatrixFile, featureMatrixSelectFile, irrelevantSampleMaxRank):
    featureMatrixSelect = ''
    fp = open(featureMatrixFile)
    for line in fp.readlines():
        lineArr = line.strip().split(' ')
        if lineArr[10]=='1' or lineArr[10]=='2':
            featureMatrixSelect += str(line)
        else:
            if int(lineArr[2])<irrelevantSampleMaxRank:
                featureMatrixSelect += str(line)
    myLib.saveFile(featureMatrixSelect, featureMatrixSelectFile)
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

def addLabelOnTestData(FeatureMatrixFile, qrelFile, FeatureMatrixLabelFile):
    labelDic = qrelToLabelDic(qrelFile)
    FeatureMatrixLabel=''
    count=0
    fp = open(FeatureMatrixFile)#this set should be large enough          
    for line in fp.readlines():
        lineArr=line.strip().split(' ')
        if lineArr[0] in labelDic and lineArr[1] in labelDic[lineArr[0]]:
            FeatureMatrixLabel+=str(line).strip()+' '+str(labelDic[lineArr[0]][lineArr[1]]).strip()+'\n'
        else:
            FeatureMatrixLabel+=str(line).strip()+' '+'0'+'\n'
        count+=1
        if count%1000==0:
            print count  
    fpWrite=open(FeatureMatrixLabelFile, 'w')
    fpWrite.write(FeatureMatrixLabel)
    return 0

def randomForestClassify(X_train,y_train,X_test,y_test):
    clf = RandomForestClassifier(n_estimators=100, max_depth=None, min_samples_split=1, random_state=0)
    #clf = AdaBoostClassifier(n_estimators=200)
    clf = clf.fit(X_train,y_train)
    result=clf.predict(X_test)
    #print clf.feature_importances_
    return result,calculatePrecision(result,y_test)

def calculatePrecision(result,y_test):
    ranking0 = 0
    ranking0right = 0
    ranking1 = 0
    ranking1right = 0
    ranking2 = 0 
    ranking2right = 0
    for i in range(len(y_test)):
        if y_test[i]=='0':
            ranking0 += 1
            if y_test[i]==result[i]:
                ranking0right += 1
        elif y_test[i]=='1':
            ranking1 += 1
            if y_test[i]==result[i]:
                ranking1right += 1
        elif y_test[i]=='2':
            ranking2 += 1
            if y_test[i]==result[i]:
                ranking2right += 1
    print '0: ',ranking0,ranking0right,ranking0right*1.0/ranking0
    print '1: ',ranking1,ranking1right,ranking1right*1.0/ranking1
    print '2: ',ranking2,ranking2right,ranking2right*1.0/ranking2
    
    right_count=0
    for i in range(len(result)):
        if result[i]==y_test[i]:
            right_count+=1

    
    return right_count*1.0/len(result)

def loadDataSet(filename):
    dataMat=[]; labelMat=[];
    fr = open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split(' ')
        dataMat.append([float(lineArr[2]),float(lineArr[3]),float(lineArr[4]),float(lineArr[5]),float(lineArr[6]),float(lineArr[7]),float(lineArr[8]),float(lineArr[9])])
        #dataMat.append([float(lineArr[3]),float(lineArr[5]),float(lineArr[7]),float(lineArr[9])])
        #dataMat.append([float(lineArr[8]),float(lineArr[9]),float(lineArr[12]),float(lineArr[13]),float(lineArr[14]),float(lineArr[15].replace('\n',''))])
        #if int(lineArr[3])==0:
        #if int(lineArr[10])==0:
         #   labelMat.append(0)
        #else:
         #   labelMat.append(1)
        labelMat.append(lineArr[10])
    return dataMat,labelMat

def combineScoreOfOriginalAndClassfier(originalResultFile, prediction, award, topN, finalResultFile):
    predictionIndex = 0
    ScoreOfOriginalAndClassfierDic = {}
    fp = open(originalResultFile)
    for line in fp.readlines():
        lineArr = line.strip().split(' ')
        queryId = lineArr[0]
        documentId = lineArr[1]
        score = lineArr[3]
        if queryId not in ScoreOfOriginalAndClassfierDic:
            ScoreOfOriginalAndClassfierDic[queryId] = {}
        if documentId not in ScoreOfOriginalAndClassfierDic[queryId]:
            ScoreOfOriginalAndClassfierDic[queryId][documentId] = float(score)+float(prediction[predictionIndex])*award
        predictionIndex+=1
    
    combineResultRerank=''        
    for queryId in ScoreOfOriginalAndClassfierDic:
        rankIndex=0
        for item in sorted(ScoreOfOriginalAndClassfierDic[queryId].iteritems(), key=operator.itemgetter(1), reverse=True)[0:topN]:
            combineResultRerank += str(queryId)+' '+'Q0'+' '+str(item[0])+' '+str(rankIndex)+' '+str(item[1]).replace('\n','')+' '+'ecnuEn'+'\n'
            rankIndex += 1
    
    fpWrite=open(finalResultFile,'w')
    fpWrite.write(combineResultRerank)
    fpWrite.close()
            
    return 0

if __name__ == "__main__": 
    #X_train,y_train = loadDataSet('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\3\\trainData\\LM_LGD_BM25_wholeSelect.featureTrain')
    #X_test,y_test = loadDataSet('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\3\\testData\\LM_LGD_BM25_score.featureTestLabel')
    #result, precision = randomForestClassify(X_train,y_train,X_test,y_test)
    #print precision
    
    #for i in range(1,20):
     #   combineScoreOfOriginalAndClassfier('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\3\\testData\\LM_LGD_BM25_score.featureTestLabel',
      #                                     result,
       #                                    0.02*i,
        #                                   1000,
         #                                  'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\3\\finalResult\\randomForestFinalResult'+str(i)+'.txt')
        #print 'randomForestFinalResult'+str(i)+'.txt'
        
    #filesNameList = myLib.getResultFileNameFromFile('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\testData', 
     #                                        'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\toBeAddAsFeature\\toBeAddAsFeature.txt')
    #QidDidRankScoreDicOrdered = generateFeatureMatrix('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\testData\\LM_LGD_BM25_2000.res2015',
     #                   filesNameList)
    #addLabelOnTestData('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\3\\testData\\LM_LGD_BM25_score.featureTest',
     #                  'I:\\trec2016\\testMethodIn2015Data\\qrel2015\\qrels-treceval-2015.txt',
      #                 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\3\\testData\\LM_LGD_BM25_score.featureTestLabel')
    #saveVectorMatrix(QidDidRankScoreDicOrdered, 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\testData\\LM_LGD_BM25_score.featureTest')
    #SvmRankFormat('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\testData\\LM_LGD_BM25_score.featureTest',
     #                       'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\testData\\LM_LGD_BM25_score.featureTestSvm',
      #                      'noLabel')
    
    #filesNameList = myLib.getResultFileNameFromFile('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\trainData', 
     #                                        'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\toBeAddAsFeature\\toBeAddAsFeature.txt')
    #QidDidRankScoreDicOrdered = generateFeatureMatrixLabel('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\trainData\\LM_LGD_BM25_whole.res',
     #                   filesNameList,
      #                  'I:\\trec2016\\testMethodIn2015Data\\qrel2014\\qrels-treceval-2014.txt')
    #saveVectorMatrix(QidDidRankScoreDicOrdered, 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\trainData\\LM_LGD_BM25_whole.featureTrain')
    #selectTrainSample('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\trainData\\LM_LGD_BM25_whole.featureTrain',
     #                 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\trainData\\LM_LGD_BM25_wholeSelect.featureTrain',
      #                600)
    #SvmRankFormat('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\trainData\\LM_LGD_BM25_wholeSelect.featureTrain',
     #                       'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\trainData\\LM_LGD_BM25_wholeSelect.featureTrainSvm',
      #                     'haveLabel')
     
    #for i in range(1,20):
     #   combineOriginalScoreAndPredcition('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\testData\\LM_LGD_BM25_score.featureTest', 
      #                0.05*i, 
       #               'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\prediction\\predictions.2015LM_LGD_BM25',
        #              'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\finalResult\\2015LM_LGD_BM25Final'+str(0.05*i)+'.txt',
         #             1000)
        #print '2015LM_LGD_BM25Final'+str(0.05*i)+'.txt'
        
    #automaticEvaluate.sampleEvalOnFolder('I:\\trec2016\\testMethodIn2015Data',
     #           'I:\\trec2016\\testMethodIn2015Data\\qrel2015\\qrels-sampleval-2015.txt',
      #          'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\3\\finalResult',
       #         'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\3\\eval')
      
   filesNameList = myLib.getResultFileNameFromFolder('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\3\\eval')
   resCsv = statisticResult.extractMetricsToString(filesNameList, ['infNDCG','iP10'])
   myLib.saveFile(resCsv, 'I:\\trec2016\\testMethodIn2015Data\\statisticResult2015\\learnToRank3.csv')
   rankResultMetric = statisticResult.rankResults(filesNameList, 'infNDCG')
   myLib.saveFile(rankResultMetric, 'I:\\trec2016\\testMethodIn2015Data\\statisticResult2015\\learnToRank3rank.txt')