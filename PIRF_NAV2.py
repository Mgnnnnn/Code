#!/usr/bin/env python2.7
# -*- coding: utf-8 -*
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
import os


# 匹配点去重，取最优
def Remove_duplication(TheList):
    # 返回测试图像去重后的点的索引 query_index 
    temp = [TheList[0]]
    query_index = [TheList[0][1]]
    count = 0
    for i in range(1, len(TheList)):
        if(TheList[i][0] == temp[count][0] and TheList[i][2] < temp[count][2]):
            temp[count] = TheList[i]
            query_index[count] = TheList[i][1]

        elif(TheList[i][0] != temp[count][0]):
            temp.append(TheList[i])
            query_index.append(TheList[i][1])
            count+=1
    return query_index


def Update_CodeBook_IndexCode(CodeBook, CodeBookNum, QueryIndex, desc):
    AppendList = [i for i in range(len(desc)) if i not in QueryIndex]

    for index in AppendList:
        CodeBook[CodeBookNum] = desc[index]
        QueryIndex.append(CodeBookNum)
        CodeBookNum += 1
    return CodeBook, CodeBookNum, QueryIndex


def CountSame(L1, L2):
    res = 0
    for o in L1:
        if o in L2:
            res+=1
    return res




def ReadNodeImgVstack(path):
    	num = 1
	a = os.listdir(path)

	for i in a:
		if num == 1:
				temp = cv2.imread(path+i)
		else:
			temp = np.vstack((temp, cv2.imread(path+i)))
		num += 1		

	return temp


im1 = ReadNodeImgVstack('/home/kou-ikeda/catkin_ws/src/project_pro/data/1Landmark/img/')
im20 = ReadNodeImgVstack('/home/kou-ikeda/catkin_ws/src/project_pro/data/20Landmark/img/')
im26 = ReadNodeImgVstack('/home/kou-ikeda/catkin_ws/src/project_pro/data/26Landmark/img/')


im2 = ReadNodeImgVstack('/home/kou-ikeda/catkin_ws/src/project_pro/data/2Landmark/img/')
im21 = ReadNodeImgVstack('/home/kou-ikeda/catkin_ws/src/project_pro/data/21Landmark/img/')
im25 = ReadNodeImgVstack('/home/kou-ikeda/catkin_ws/src/project_pro/data/25Landmark/img/')


im6 = ReadNodeImgVstack('/home/kou-ikeda/catkin_ws/src/project_pro/data/6Landmark/img/')

im11 = ReadNodeImgVstack('/home/kou-ikeda/catkin_ws/src/project_pro/data/11Landmark/img/')
im15 = ReadNodeImgVstack('/home/kou-ikeda/catkin_ws/src/project_pro/data/15Landmark/img/')


im12 = ReadNodeImgVstack('/home/kou-ikeda/catkin_ws/src/project_pro/data/12Landmark/img/')
im14 = ReadNodeImgVstack('/home/kou-ikeda/catkin_ws/src/project_pro/data/14Landmark/img/')



test1 = im12
test2 = im14


timestart = time.time()

bf = cv2.BFMatcher_create()


surf = cv2.xfeatures2d.SURF_create(300)
key1,desc_query1 = surf.detectAndCompute(test1,None)
key2,desc_query2 = surf.detectAndCompute(test2,None)

# 建造密码本 CodeBook = {[索引]: 长64维矩阵}
CodeBookNum = 1
CodeBook = {}
for des in desc_query1:
    CodeBook[CodeBookNum] = des
    CodeBookNum += 1


# 创建节点索引字典　NodeBook = {[节点号]: 编码后的索引列表}
NodeNum = 1
NodeBook = {}
NodeBook[NodeNum] = range(1, len(desc_query1)+1)
NodeNum+=1


# 获得测试图像匹配到的点的索引 QueryIndex
#knnMatch(匹配点, 密码本)
CodeBookMatrix = np.array([i for i in CodeBook.values()])
matches = bf.match(desc_query2, CodeBookMatrix)
GoodMatches = [(match.trainIdx, match.queryIdx, match.distance) for match in matches if match.distance < 0.3]
QueryIndex = Remove_duplication(sorted(GoodMatches))


# 更新密码本，更新密码本最大索引值，更新测试图像索引
CodeBook, CodeBookNum, UpdatedIndexCode = Update_CodeBook_IndexCode(
    CodeBook, CodeBookNum, QueryIndex, desc_query2)


# 生成比对图像的 num_appear值, n_i 值, 计算 s_i 值
num_appear = len(QueryIndex)
n_i = CountSame(UpdatedIndexCode, NodeBook[1])
s_i = num_appear*n_i

print(s_i)

# 更新节点索引字典
NodeBook[NodeNum] = UpdatedIndexCode