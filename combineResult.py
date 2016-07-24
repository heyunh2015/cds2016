# coding:utf-8
import operator
import support as myLib
systemPathSeperator = '\\'

def resultToQidDidScoreDic(resultFile):
    fp = open(resultFile)
    lines = fp.readlines() 
    
    QidDidScoreDic = {}  
    for line in lines:
        lineArr=line.split(' ')
        queryId = lineArr[0]
        doucmentId = lineArr[2]
        score = lineArr[4]
        if queryId not in QidDidScoreDic:
            QidDidScoreDic[queryId]={}
        if doucmentId not in QidDidScoreDic[queryId]:
            QidDidScoreDic[queryId][doucmentId]= score
    
    return QidDidScoreDic

def uniformQidDidScoreDic(QidDidScoreDic):
    scoreList = []
    uniformScoreList = []
    for queryId in QidDidScoreDic:
        for documentId in QidDidScoreDic[queryId]:
            score = QidDidScoreDic[queryId][documentId]
            scoreList.append(score)
    uniformScoreList = myLib.uniformMaxMin(scoreList) 
    
    documentIndex = 0
    for queryId in QidDidScoreDic:
        for documentId in QidDidScoreDic[queryId]:
            QidDidScoreDic[queryId][documentId] = uniformScoreList[documentIndex]
            documentIndex += 1
            
    return QidDidScoreDic

def combine(baseQidDidScoreDic, QidDidScoreDic):
    for queryId in baseQidDidScoreDic:
        for documentId in QidDidScoreDic[queryId]:
            if documentId in baseQidDidScoreDic[queryId]:
                baseQidDidScoreDic[queryId][documentId] += QidDidScoreDic[queryId][documentId]
            else:
                baseQidDidScoreDic[queryId][documentId] = QidDidScoreDic[queryId][documentId]
    return baseQidDidScoreDic

def combineResults(toBeCombinedResultsFolder, toBeCombinedResultsFile, combinedResultFile):
    filesNameList = myLib.getResultFileNameFromFile(toBeCombinedResultsFolder, 
                                             'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\toBeCombinedResults\\'+toBeCombinedResultsFile)
    combineFile = filesNameList[0]
    combineQidDidScoreDic = resultToQidDidScoreDic(combineFile)
    combineQidDidScoreDic = uniformQidDidScoreDic(combineQidDidScoreDic)
    for toBeCombinedResultIndex in range(1, len(filesNameList)):
        resultFile = filesNameList[toBeCombinedResultIndex]
        QidDidScoreDic = resultToQidDidScoreDic(resultFile)
        QidDidScoreDic = uniformQidDidScoreDic(QidDidScoreDic)
        combineQidDidScoreDic = combine(combineQidDidScoreDic, QidDidScoreDic)
    
    combineResultRerank=''        
    for queryId in combineQidDidScoreDic:
        rankIndex=0
        for item in sorted(combineQidDidScoreDic[queryId].iteritems(), key=operator.itemgetter(1), reverse=True):
            combineResultRerank += str(queryId)+' '+'Q0'+' '+str(item[0])+' '+str(rankIndex)+' '+str(item[1]).replace('\n','')+' '+'ecnuEn'+'\n'
            rankIndex += 1
        print str(queryId)
    fpWrite=open(combinedResultFile,'w')
    fpWrite.write(combineResultRerank)
    fpWrite.close()
    return combineQidDidScoreDic

    

if __name__ == "__main__": 
    baseQidDidScoreDic = combineResults('I:\\trec2016\\testMethodIn2015Data\\result2015', 
                                        'toBeCombinedResults.txt', 
                                        'I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2_PL2_BM25_rerank_new2.res')
    myLib.cut_amount('I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2_PL2_BM25_rerank_new2.res', 
                     'I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2_PL2_BM25_rerank_new2_1000.res', 
                     1001)
    
    
    
    #uniform_feature('I:\\trec2016\\testMethodIn2015Data\\result2015\\BM25b0.75_713.res','I:\\trec2016\\testMethodIn2015Data\\result2015\\BM25b0.75_713_u.res')
    #uniform_feature('I:\\trec2016\\testMethodIn2015Data\\result2015\\PL2c1.2_714.res','I:\\trec2016\\testMethodIn2015Data\\result2015\\PL2c1.2_714_u.res')
    #uniform_feature('I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2c1.0_715.res','I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2c1.0_715_u.res')
    
    #combine('I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2c1.0_715_u.res', 'I:\\trec2016\\testMethodIn2015Data\\result2015\\PL2c1.2_714_u.res', 'I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2_PL2.res');
    #combine('I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2_PL2.res', 'I:\\trec2016\\testMethodIn2015Data\\result2015\\BM25b0.75_713_u.res', 'I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2_PL2_BM25.res');
    
    #reRank('I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2_PL2_BM25.res', 'I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2_PL2_BM25_rerank.res')
    #myLib.cut_amount('I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2_PL2_BM25_rerank.res','I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2_PL2_BM25_rerank_1500.res',1501)
    
    #uniform_feature('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BM25b0.75_832.res','I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BM25b0.75_832_u.res')
    #uniform_feature('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\PL2c1.2_833.res','I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\PL2c1.2_833_u.res')
    #uniform_feature('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BB2c1.0_834.res','I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BB2c1.0_834_u.res')
    
    #combine('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BB2c1.0_834_u.res', 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\PL2c1.2_833_u.res', 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BB2_PL2.res');
    #combine('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BB2_PL2.res', 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BM25b0.75_832_u.res', 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BB2_PL2_BM25.res');
    
    #reRank('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BB2_PL2_BM25.res', 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BB2_PL2_BM25_rerank.res')
    #myLib.cut_amount('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BB2_PL2_BM25_rerank.res','I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BB2_PL2_BM25_rerank_200.res',201)