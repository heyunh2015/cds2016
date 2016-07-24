#! /usr/bin/python
# coding:utf-8
import os
import statisticResult 
import support as myLib 
SystemPathSeperator = '/'

def submitQueryToTerrier(documentCount, termCount):
    for documentIndex in range(1, documentCount+1):
        for termIndex in range(1, termCount+1):
            cmdStr = 'trec_terrier.sh -r -q -Dexpansion.documents='+str(documentIndex)+' -Dexpansion.terms='+str(termIndex)+' -Dtrec.model=BM25 -c 0.75 -Dtrec.topics=/home/lmy/trec16/testMethodIn2015Data/query2015/2015OriginalQuery.txt' 
            print cmdStr
            ret = os.popen(cmdStr).read().strip()
    return 0


def evalPesudoRelevance(documentCount, termCount):
    for documentIndex in range(1, documentCount+1):
        for termIndex in range(1, termCount+1):
            #cmdStr = '/home/lmy/trec16/sample_eval.pl -q /home/lmy/trec16/testMethodIn2015Data/qrel2015/qrels-sampleval-2015.txt /home/lmy/soft/terrier/var/results/BM25b0.75_Bo1bfree_d_'+str(documentIndex)+'_t_'+str(termIndex)+'_'+str(1127+(documentIndex-1)*20+termIndex-1)+'.res > /home/lmy/trec16/testMethodIn2015Data/adjustPesudoRelevanceParameters/eval/BM25b0.75_Bo1bfree_d_'+str(documentIndex)+'_t_'+str(termIndex)+'_'+str(1127+(documentIndex-1)*20+termIndex-1)+'.res.eval' 
            #print cmdStr
            #ret = os.popen(cmdStr).read().strip()
            print 'BM25b0.75_Bo1bfree_d_'+str(documentIndex)+'_t_'+str(termIndex)+'_'+str(1127+(documentIndex-1)*20+termIndex-1)+'.res.eval'
    return 0

if __name__ == "__main__": 
    #submitQueryToTerrier(10, 20)
    #evalPesudoRelevance(10, 20)
    filesNameList = myLib.getResultFileNameFromFile('I:\\trec2016\\testMethodIn2015Data\\adjustPesudoRelevanceParameters\\eval', 
                                              'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\toBeAnalyizedResults\\adjustPesudoRelevanceFeedback.txt')
    statisticResult.rankResults(filesNameList, 'infNDCG')
    #statisticResult.plotResults(filesNameList, 'infNDCG')