

def statisticRankingCount(fileName):
    fp = open(fileName)
    countRanking1 = 0
    countRanking2 = 0
    countRanking0 = 0
    for line in fp.readlines():
        lineArr = line.strip().split(' ')
        if lineArr[12]=='1':
            countRanking1 += 1
        elif lineArr[12]=='0':
            countRanking0 += 1
        elif lineArr[12]=='2':
            countRanking2 += 1
    print '0:',countRanking0
    print '1:',countRanking1
    print '2:',countRanking2
    return 0


if __name__ == "__main__": 
    #statisticRankingCount('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\qerl2014.txt')
    statisticRankingCount('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014_wholeTrain.txt')