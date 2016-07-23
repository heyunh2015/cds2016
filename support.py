# coding:utf-8

import operator,os,re

def max_mine(array):
    max_mine=1.0
    for item in array:
        if float(item)>max_mine:
            max_mine=float(item)
    return max_mine 

def min_mine(array):
    min_mine=100
    for item in array:
        if float(item)<min_mine:
            min_mine=float(item)
    return min_mine 

def uniformMaxMin(feature):
    feature_uniform=[]
    min_item=min_mine(feature)
    max_item=max_mine(feature)
    print min_item,max_item
    for item in feature:
        item_uniform=(float(item) - min_item)/(max_item-min_item)
        feature_uniform.append(item_uniform)
    return feature_uniform   

def listDir(path):
    list = []
    for file in os.listdir(path):  
        if os.path.isdir(os.path.join(path, file)):  # dir 
            list.extend(listDir(os.path.join(path, file)))
        else:  # file
            list.append(os.path.join(path, file))
    return list

def getResultFileNameFromFolder(folderName):
    filesNameList = listDir(folderName)
    return filesNameList

def getResultFileNameFromFile(folderName, resultNamesFile):
    SystemPathSeperator = '\\'
    filesNameList = []
    fp =open(resultNamesFile)
    for line in fp.readlines():
        filesNameList.append(folderName + SystemPathSeperator + str(line).strip())
    return filesNameList

def cut_amount(filename,newfilename,n):#
    dic_query={}
    fp=open(filename)
    lines=fp.readlines()
    text=''
    for line in lines:
        lineArr=line.split(' ')
        if lineArr[0] not in dic_query:
            dic_query[lineArr[0]]=1
        else:
            dic_query[lineArr[0]]+=1
        if dic_query[lineArr[0]]>=n:
            continue
        else:
            text+=str(line)
    fp_write=open(newfilename,'w')
    fp_write.write(text)
    return 0

def reRank(filename,reRankfile):#�����·�����������
    fp=open(filename)
    lines=fp.readlines()
    dic_query={}   
    for line in lines:
        lineArr=line.split(' ')
        if lineArr[0] not in dic_query:
            dic_query[lineArr[0]]={}
        if lineArr[2] not in dic_query[lineArr[0]]:
            dic_query[lineArr[0]][lineArr[2]]=float(lineArr[4]) 
            
    combine_result_rank=''        
    for i in dic_query:
        count=0
        for item in sorted(dic_query[i].iteritems(), key=operator.itemgetter(1), reverse=True):
            combine_result_rank+=str(i)+' '+'Q0'+' '+str(item[0])+' '+str(count)+' '+str(item[1]).replace('\n','')+' '+'ecnuEn'+'\n'
            count+=1
        print str(i)
    fp_write=open(reRankfile,'w')
    fp_write.write(combine_result_rank)
    
    return 0