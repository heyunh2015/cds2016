import support as myLib
import statisticResult 
import automaticEvaluate
def x():
    
    return 0

if __name__ == "__main__":
    #myLib.cut_amount('I:\\trec2016\\testMethodIn2015Data\\combinationResults\\results\\BB2c1.0_Bo1bfree_d_8_t_20_1463.res', 'I:\\trec2016\\testMethodIn2015Data\\combinationResults\\results1000\\BB2c1.0_Bo1bfree_d_8_t_20_1463.res', 1001)
    #myLib.cut_amount('I:\\trec2016\\testMethodIn2015Data\\combinationResults\\results\\Hiemstra_LM0.15_Bo1bfree_d_8_t_20_1464.res', 'I:\\trec2016\\testMethodIn2015Data\\combinationResults\\results1000\\Hiemstra_LM0.15_Bo1bfree_d_8_t_20_1464.res', 1001)
    #myLib.cut_amount('I:\\trec2016\\testMethodIn2015Data\\combinationResults\\results\\LGDc1.0_Bo1bfree_d_8_t_20_1465.res', 'I:\\trec2016\\testMethodIn2015Data\\combinationResults\\results1000\\LGDc1.0_Bo1bfree_d_8_t_20_1465.res', 1001)
    #myLib.cut_amount('I:\\trec2016\\testMethodIn2015Data\\combinationResults\\results\\PL2c1.2_Bo1bfree_d_8_t_20_1466.res', 'I:\\trec2016\\testMethodIn2015Data\\combinationResults\\results1000\\PL2c1.2_Bo1bfree_d_8_t_20_1466.res', 1001)
    #myLib.cut_amount('I:\\trec2016\\testMethodIn2015Data\\combinationResults\\results\\TF_IDF_Bo1bfree_d_8_t_20_1467.res', 'I:\\trec2016\\testMethodIn2015Data\\combinationResults\\results1000\\TF_IDF_Bo1bfree_d_8_t_20_1467.res', 1001)
    #myLib.cut_amount('I:\\trec2016\\testMethodIn2015Data\\combinationResults\\results\\BM25b0.75_Bo1bfree_d_8_t_20_1468.res', 'I:\\trec2016\\testMethodIn2015Data\\combinationResults\\results1000\\BM25b0.75_Bo1bfree_d_8_t_20_1468.res', 1001)
    
    #automaticEvaluate.sample_eval('I:\\trec2016\\testMethodIn2015Data',
     #           'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\toBeEvaluatedResults\\adjustCombineResults.txt',
      #          'I:\\trec2016\\testMethodIn2015Data\\qrel2015\\qrels-sampleval-2015.txt',
       #         'I:\\trec2016\\testMethodIn2015Data\\combinationResults\\results1000',
        #        'I:\\trec2016\\testMethodIn2015Data\\combinationResults\\eval')
    
    filesNameList = myLib.getResultFileNameFromFile('I:\\trec2016\\testMethodIn2015Data\\combinationResults\\eval', 
                                              'H:\\Users2016\\hy\\workspace\\trec16Python\\resultFileNames\\toBeAnalyizedResults\\adjustCombineResults.txt')
    resCsv = statisticResult.extractMetricsToString(filesNameList, ['infNDCG','iP10'])
    statisticResult.saveFile(resCsv, 'I:\\trec2016\\testMethodIn2015Data\\statisticResult2015\\adjustCombineResults.csv')
    statisticResult.rankResults(filesNameList, 'infNDCG')