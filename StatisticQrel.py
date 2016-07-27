

def statisticRankingCountTrainData(fileName):
    fp = open(fileName)
    countRanking1 = 0
    countRanking2 = 0
    countRanking0 = 0
    for line in fp.readlines():
        lineArr = line.strip().split(' ')
        if lineArr[10]=='1':
            countRanking1 += 1
        elif lineArr[10]=='0':
            countRanking0 += 1
        elif lineArr[10]=='2':
            countRanking2 += 1
    print '0:',countRanking0
    print '1:',countRanking1
    print '2:',countRanking2
    return 0

def statisticRankingCountQrel(fileName):
    fp = open(fileName)
    countRanking1 = 0
    countRanking2 = 0
    countRanking0 = 0
    for line in fp.readlines():
        lineArr = line.strip().split('\t')
        if lineArr[3]=='1':
            countRanking1 += 1
        elif lineArr[3]=='0':
            countRanking0 += 1
        elif lineArr[3]=='2':
            countRanking2 += 1
    print '0:',countRanking0
    print '1:',countRanking1
    print '2:',countRanking2
    return 0

if __name__ == "__main__": 
    statisticRankingCountTrainData('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\trainData\\LM_LGD_BM25_whole.featureTrain')
    statisticRankingCountTrainData('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\2\\trainData\\LM_LGD_BM25_wholeSelect.featureTrain')
    statisticRankingCountTrainData('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\1\\trainData\\LM_LGD_BM25_score.featureTrain')
    statisticRankingCountQrel('I:\\trec2016\\testMethodIn2015Data\\qrel2014\\qrels-treceval-2014.txt')