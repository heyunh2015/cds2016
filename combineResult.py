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

def combineResults(filesNameList, combinedResultFile, countOption):
    combineFile = filesNameList[0]
    combineQidDidScoreDic = resultToQidDidScoreDic(combineFile)
    combineQidDidScoreDic = uniformQidDidScoreDic(combineQidDidScoreDic)
    for toBeCombinedResultIndex in range(1, len(filesNameList)):
        resultFile = filesNameList[toBeCombinedResultIndex]
        QidDidScoreDic = resultToQidDidScoreDic(resultFile)
        QidDidScoreDic = uniformQidDidScoreDic(QidDidScoreDic)
        combineQidDidScoreDic = combine(combineQidDidScoreDic, QidDidScoreDic)
    
    if countOption=='whole':
        combineResultRerank=''        
        for queryId in combineQidDidScoreDic:
            rankIndex=0
            for item in sorted(combineQidDidScoreDic[queryId].iteritems(), key=operator.itemgetter(1), reverse=True):#[0:topN]:
                combineResultRerank += str(queryId)+' '+'Q0'+' '+str(item[0])+' '+str(rankIndex)+' '+str(item[1]).replace('\n','')+' '+'ecnuEn'+'\n'
                rankIndex += 1
        
            print str(queryId)
    else:
        combineResultRerank=''        
        for queryId in combineQidDidScoreDic:
            rankIndex=0
            for item in sorted(combineQidDidScoreDic[queryId].iteritems(), key=operator.itemgetter(1), reverse=True)[0:int(countOption)]:
                combineResultRerank += str(queryId)+' '+'Q0'+' '+str(item[0])+' '+str(rankIndex)+' '+str(item[1]).replace('\n','')+' '+'ecnuEn'+'\n'
                rankIndex += 1
        
            print str(queryId)
    fpWrite=open(combinedResultFile,'w')
    fpWrite.write(combineResultRerank)
    fpWrite.close()
    return 0

    

if __name__ == "__main__": 
    filesNameList = myLib.getResultFileNameFromFile('I:\\trec2016\\final Result',
                                             'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\toBeCombinedResults\\toBeCombinedResults.txt')
    combineResults(filesNameList, 
                   'I:\\trec2016\\final Result\\BM25_LGD_LM.res',
                   '1000')
    
    