# coding:utf-8
import support as myLib

def extractMetricsToString(filesNameList):
    resCsv = ''
    for file in filesNameList:
        resCsvOfFile = file
        fp = open(file+'.eval')
        for line in fp.readlines():
            lineArr = line.strip().split('\t')
            if str(lineArr[0]).strip()=='infNDCG' and str(lineArr[2]).strip()=='all':
                resCsvOfFile += ','+'infNDCG'+','+str(lineArr[4])
            if str(lineArr[0]).strip()=='iP10' and str(lineArr[2]).strip()=='all':  
                resCsvOfFile += ','+'iP10'+','+str(lineArr[4])
        resCsv += resCsvOfFile +'\n'
    print resCsv
    
    return resCsv

def saveFile(string, fileName):
    fp_w = open(fileName,'w')
    fp_w.write(string)        
    fp_w.close()
    return 0

if __name__ == "__main__": 
    filesNameList = myLib.getResultFileNameFromFile('I:\\trec2016\\testMethodIn2015Data\\evaluateResultNDCG2015', 
                                              'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\learnToRankResultsName.txt')
    #filesNameList = myLib.getResultFileNameFromFolder('I:\\trec2016\\testMethodIn2015Data\\evaluateResultNDCG2015') 
    resCsv = extractMetricsToString(filesNameList)
    saveFile(resCsv, 'I:\\trec2016\\testMethodIn2015Data\\statisticResult2015\\learnToRank3.csv')