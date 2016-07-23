# coding:utf-8
import support as myLib
import operator
import math as math

def query_web_dic(test_filename):
    fp=open(test_filename)
    lines=fp.readlines()
    dic={}   
    for line in lines:
        lineArr=line.split(' ')
        if lineArr[0] not in dic:
            dic[lineArr[0]]={}
        if lineArr[2] not in dic[lineArr[0]]:
            dic[lineArr[0]][lineArr[2]]=[lineArr[3],lineArr[4]]
    return dic

def select_feature1(result_filename,dic_twoLevel,feature_filename):
    feature=''
    count=0
    fp_result=open(result_filename)#this set should be large enough
    lines_result=fp_result.readlines()             
    for line in lines_result:
        lineArr=line.split(' ')
        if lineArr[0] in dic_twoLevel and str(lineArr[2]).replace('\n','') in dic_twoLevel[lineArr[0]]:
            feature+=str(line).replace('\n','')+' '+str(dic_twoLevel[lineArr[0]][str(lineArr[2]).replace('\n','')][0])+' '+str(dic_twoLevel[lineArr[0]][str(lineArr[2]).replace('\n','')][1])+'\n'
        else:
            feature+=str(line).replace('\n','')+' '+'10000'+' '+'0'+'\n'
        count+=1
        if count%1000==0:
            print count  
    fp_feature1=open(feature_filename,'w')
    fp_feature1.write(feature)

def query_web_dic2(test_filename):
    fp=open(test_filename)
    lines=fp.readlines()
    dic={}   
    for line in lines:
        lineArr=line.strip().split('\t')
        if lineArr[0] not in dic:
            dic[lineArr[0]]={}
        if str(lineArr[2]).replace('\n','') not in dic[lineArr[0]]:
            dic[lineArr[0]][str(lineArr[2]).replace('\n','')]=lineArr[3]
    return dic

def select_feature3(result_filename,dic_twoLevel,feature_filename):
    feature=''
    count=0
    fp_result=open(result_filename)#this set should be large enough
    lines_result=fp_result.readlines()             
    for line in lines_result:
        lineArr=line.strip().split(' ')
        if lineArr[0] in dic_twoLevel and str(lineArr[2]).replace('\n','') in dic_twoLevel[lineArr[0]]:
            feature+=str(line).replace('\n','')+' '+str(dic_twoLevel[lineArr[0]][str(lineArr[2]).replace('\n','')])+'\n'
        #else:
         #   feature+=str(line).replace('\n','')+' '+'0'+'\n'
        count+=1
        if count%1000==0:
            print count  
    fp_feature1=open(feature_filename,'w')
    fp_feature1.write(feature)

def transform_SvmRankFormat(filename,svmRankFile):
    fp=open(filename)
    lines=fp.readlines()
    file_new=''
    for line in lines:
        lineArr=line.strip().split(' ')
        file_new+=lineArr[12]+' '+'qid:'+lineArr[0]+' 1:'+lineArr[4]+' 2:'+lineArr[7]+' 3:'+lineArr[9]+' 4:'+lineArr[11]+'\n'
        
    fp_w=open(svmRankFile,'w')
    fp_w.write(file_new)
    return 0

def format_trec(filename_old,filename_new):#14.将结果转化为trec的标准格式
    fp=open(filename_old)
    lines=fp.readlines()
    dic_query={}    
    for line in lines:
        lineArr=line.split(' ')
        if lineArr[0] not in dic_query:
            query_name=str(lineArr[0])
            dic_query[int(query_name)]=1
    sort_dic=sorted(dic_query.iteritems(), key=operator.itemgetter(0), reverse=False)
    query_array=[]
    for item in sort_dic:
        query_array.append(str(item[0]))
    
    trec_file='' 
    dic_query_content={}
    query_content=''
    for item in query_array:
        for line in lines:
            lineArr=line.strip().split(' ')
            if lineArr[0] == str(item):
                query_content+=str(lineArr[0])+' '+str(lineArr[1])+' '+str(lineArr[2])+' '+str(lineArr[3])+' '+str(lineArr[4])+' '+'ecnuEn'+' '+str(lineArr[6])+' '+str(lineArr[7])+' '+str(lineArr[8])+' '+str(lineArr[9])+' '+str(lineArr[10])+' '+str(lineArr[11])+' '+str(lineArr[12])+'\n'   
        dic_query_content[item]=query_content
        query_content=''
    for item in query_array:
        trec_file+=str(dic_query_content[item])
        
    fp_write=open(filename_new,'w')
    fp_write.write(trec_file)  
    
    return 0

def add_score(filename,file_score,new_filename):#将模型的分数加到原来的结果的最后一列
    data_score=[]
    fp_score=open(file_score)
    lines_score=fp_score.readlines()
    for line in lines_score:
        if float(str(line).strip())<0.0001:
            data_score.append(0.0)
        else:
            data_score.append(float(str(line).strip()))
    
    data_score=myLib.uniform_calculate(data_score)    
    add_score_txt=''   
    fp=open(filename)
    lines=fp.readlines()
    for i in range(len(lines)):
        add_score_txt+=str(lines[i]).strip()+' '+str(data_score[i])+'\n'
    
    fp_writa=open(new_filename,'w')
    fp_writa.write(add_score_txt)
    
    return 0

def combine_score(filename,b,new_filename):#将模型分数与原始分数相加
    fp=open(filename)
    lines=fp.readlines()
    new_file=''
        
    for line in lines:
        lineArr=line.strip().split(' ')
        new_file+=str(lineArr[0])+' '+str(lineArr[1])+' '+str(lineArr[2])+' '+str(lineArr[3])+' '+str(float(lineArr[4])*(1.0-b)+float(lineArr[6])*b)+' '+str(lineArr[5])+'\n'
    
    fp_write=open(new_filename,'w')
    fp_write.write(new_file)
    return 0

if __name__ == "__main__": 
    #dic_twoLevel=query_web_dic('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BB2c1.0_834.res')
    #select_feature1('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BB2_PL2_BM25_rerank.res',dic_twoLevel,'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014_feature_5.txt')      
    #dic_twoLevel=query_web_dic('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\PL2c1.2_833.res')
    #select_feature1('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014_feature_5.txt',dic_twoLevel,'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014_feature_5_2.txt')
    #dic_twoLevel=query_web_dic('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\BM25b0.75_832.res')
    #select_feature1('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014_feature_5_2.txt',dic_twoLevel,'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014_feature_5_2_4.txt')          
    
    #dic_twoLevel=query_web_dic2('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\qerl2014.txt')
    #select_feature3('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014_feature_5_2_4.txt',dic_twoLevel,'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014_wholeTrain.txt')   
    #format_trec('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014_wholeTrain.txt', 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014_wholeTrainOrder.txt')  
    #transform_SvmRankFormat('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014_wholeTrainOrder.txt', 
            #                'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\trainData\\2014_wholeTrainSvm.txt')  
    
    #dic_twoLevel=query_web_dic('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\BB2c1.0_715.res')
    #select_feature1('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\BB2_PL2_BM25_rerank_1500.res',dic_twoLevel,'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\2015_feature_5.txt')      
    #dic_twoLevel=query_web_dic('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\PL2c1.2_714.res')
    #select_feature1('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\2015_feature_5.txt',dic_twoLevel,'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\2015_feature_5_2.txt')
    #dic_twoLevel=query_web_dic('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\BM25b0.75_713.res')
    #select_feature1('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\2015_feature_5_2.txt',dic_twoLevel,'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\2015_feature_5_2_4.txt')          
    
    #dic_twoLevel=query_web_dic2('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\qerl2014.txt')
    #select_feature3('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\2015_feature_5_2_4.txt',dic_twoLevel,'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\2015_1200test.txt')   
    #format_trec('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\2015_1200test.txt', 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\2015_1200testOrder.txt')  
    #transform_SvmRankFormat('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\2015_1200testOrder.txt', 
     #                       'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\2015_1200testSvm.txt')  
     
    add_score('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\testData\\BB2_PL2_BM25_rerank_1500.res', 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\prediction\\predictions.2015testWhole', 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\finalResult\\2015testWholeAddScore.txt')
    for i in range(1,50):
        #combine_score('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\finalResult\\2015testWholeAddScore.txt', 0.02*i, 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\finalResult\\2015testWholeCombineScore'+str(0.02*i)+'.txt')
        #myLib.reRank('I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\finalResult\\2015testWholeCombineScore'+str(0.02*i)+'.txt', 'I:\\trec2016\\testMethodIn2015Data\\learnToRank2015\\finalResult\\2015testWholeCombineScore'+str(0.02*i)+'rerank.txt')
        print '2015testWholeCombineScore'+str(0.02*i)+'rerank.txt'