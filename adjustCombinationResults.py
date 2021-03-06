import support as myLib
import statisticResult 
import automaticEvaluate
import combineResult
from itertools import combinations
systemPathSeperator = '\\'

def combinationOfCombine(filesNameList, saveCombineResultFolder, topN):
    for selectIndex in range(1, len(filesNameList)+1):
        if selectIndex>1:
            combinationList = list(combinations(range(len(filesNameList)), selectIndex))
            combinationListLength = len(combinationList)
            for combinationIndex in range(combinationListLength):
                oneOfThecombinationSet = list(combinations(range(len(filesNameList)), selectIndex))[combinationIndex]
                filesNameToBeCombinedList = []
                combineResultFileName = ''
                for oneOfThecombinationSetIndex in range(len(oneOfThecombinationSet)):
                    fileIndex = oneOfThecombinationSet[oneOfThecombinationSetIndex]
                    filesNameToBeCombinedList.append(filesNameList[fileIndex])
                    combineResultFileName += str(fileIndex)+'_'
                combineResultFileName = combineResultFileName.strip('_')+'.res'
                combineResult.combineResults(filesNameToBeCombinedList, 
                       saveCombineResultFolder + systemPathSeperator + combineResultFileName,
                       topN)
        else:
            for fileIndex in range(len(filesNameList)):
                myLib.cut_amount(filesNameList[fileIndex],
                                 saveCombineResultFolder + systemPathSeperator + str(fileIndex) + '.res', 
                                 topN)
    return 0

if __name__ == "__main__":
    #filesNameList = myLib.getResultFileNameFromFile('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014Results', 
     #                                         'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\toBeCombinedResults\\toBeCombinedResults.txt')
    
    #combinationOfCombine(filesNameList, 
     #                    'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014combineResults', 
      #                   1000)
    
    #automaticEvaluate.sampleEvalOnFolder('I:\\trec2016\\testMethodIn2015Data',
     #           'I:\\trec2016\\testMethodIn2015Data\\qrel2014\\qrels-sampleval-2014.txt',
      #          'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014combineResults',
       #         'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\eval')
    
    filesNameList = myLib.getResultFileNameFromFolder('I:\\trec2016\\testMethodIn2015Data\\combinationResults\\eval')
    resCsv = statisticResult.extractMetricsToString(filesNameList, ['infNDCG','iP10'])
    myLib.saveFile(resCsv, 'I:\\trec2016\\testMethodIn2015Data\\statisticResult2015\\adjustCombineResults2015.csv')
    rankResultMetric = statisticResult.rankResults(filesNameList, 'infNDCG')
    myLib.saveFile(rankResultMetric, 'I:\\trec2016\\testMethodIn2015Data\\statisticResult2015\\adjustCombineResultsRank2015.txt')
    
    
            