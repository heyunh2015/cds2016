# coding:utf-8
import operator
import support as myLib
systemPathSeperator = '\\'

def uniform_feature(original_feature,uniform_feature):
    fp=open(original_feature)
    lines=fp.readlines()
    fp_u=open(uniform_feature,'w')
    feature_u=''
    feature_2=[]
    feature_2_uniform=[]    
    for line in lines:
        lineArr=line.split(' ')
        feature_2.append(lineArr[4])
    feature_2_uniform=myLib.uniformMaxMin(feature_2)    
    i=0
    for line in lines:
        lineArr=line.split(' ')
        feature_u+=str(lineArr[0])+' '+str(lineArr[1])+' '+str(lineArr[2])+' '+str(lineArr[3])+' '+str(feature_2_uniform[i])+' '+str(lineArr[5])
        i+=1
    fp_u.write(feature_u)

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

def combine1(filename_1,filename_2,combine_result_filename):
    fp_1=open(filename_1)
    fp_2=open(filename_2)
    dic_query={}
    lines_2=fp_2.readlines()
    for line in lines_2:
        lineArr=line.split(' ')
        if lineArr[0] not in dic_query:
            dic_query[lineArr[0]]={}
        if lineArr[2] not in dic_query[lineArr[0]]:
            dic_query[lineArr[0]][lineArr[2]]=lineArr[4]
    #storeweakClassArr(dic_query, 'dic_query.txt')
    combine_result=''
    combine_score=0.0
    lines_1=fp_1.readlines()
    for line in lines_1:
        lineArr=line.split(' ')
        if lineArr[0] in dic_query and lineArr[2] in dic_query[lineArr[0]]:
            combine_score=float(lineArr[4])
            combine_score+=float(dic_query[lineArr[0]][lineArr[2]])
            combine_result+=str(lineArr[0])+' '+str(lineArr[1])+' '+str(lineArr[2])+' '+str(lineArr[3])+' '+str(combine_score)+'\n'
    fp_write=open(combine_result_filename,'w')
    fp_write.write(combine_result)
    return 0

def combine(baseQidDidScoreDic, QidDidScoreDic):
    for queryId in baseQidDidScoreDic:
        for documentId in QidDidScoreDic[queryId]:
            if documentId not in baseQidDidScoreDic[queryId]:
                baseQidDidScoreDic[queryId][documentId] = QidDidScoreDic[queryId][documentId]
            else:
                baseQidDidScoreDic[queryId][documentId] += QidDidScoreDic[queryId][documentId]
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
    #QidDidScoreDic = resultToQidDidScoreDic('I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2c1.0_715.res')
    #QidDidScoreDic = uniformQidDidScoreDic(QidDidScoreDic)
    #for queryId in QidDidScoreDic:
     #   for documentId in QidDidScoreDic[queryId]:
      #      print queryId, documentId, QidDidScoreDic[queryId][documentId]
    
    #baseQidDidScoreDic = combineResults('I:\\trec2016\\testMethodIn2015Data\\result2015', 
     #                                   'toBeCombinedResults.txt', 
      #                                  'I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2_PL2_BM25_rerank_new.res')
    myLib.cut_amount('I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2_PL2_BM25_rerank_new.res', 
                     'I:\\trec2016\\testMethodIn2015Data\\result2015\\BB2_PL2_BM25_rerank_new_1000.res', 
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