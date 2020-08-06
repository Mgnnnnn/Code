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
        CodeBookNum += 1
        CodeBook[CodeBookNum] = desc[index]
        QueryIndex.append(CodeBookNum)

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



if __name__ == '__main__':
    # 把16个节点的图片打包拼接，存入NodeImgVstack列表
    NodeImgVstack = []
    for i in range(1, 17):
        NodeImgVstack.append(ReadNodeImgVstack('/home/kou-ikeda/catkin_ws/src/project_pro/DataLandmarkTest/' + str(i) + 'Landmark/img/'))

    # SURF 初始项
    bf = cv2.BFMatcher_create()
    surf = cv2.xfeatures2d.SURF_create(300)

    # 创建密码本  CodeBook = {[索引]: 长64维矩阵}
    CodeBook = {}
    CodeBookNum = 0   # 索引


    # 创建节点索引字典   NodeBook = {[节点号]: 编码后的索引列表}
    NodeBook = {}
    NodeNum = 0   # 节点号


    ResNum = 1
    TheRes = [0]

    # 开始对每个节点遍历
    for i in NodeImgVstack:
        res = []

        # 计算当前节点融合图像的 SURF 值
        key, desc_query = surf.detectAndCompute(i, None)

        # 初始情况密码本为空 更新密码本 
        if CodeBook == {}:
            # 更新密码本
            for des in desc_query:
                CodeBookNum += 1
                CodeBook[CodeBookNum] = des

            # 更新节点索引字典
            NodeNum += 1
            NodeBook[NodeNum] = range(1, len(desc_query) + 1)

            s = 0
            res.append(s)
        
        else:
            # 与密码本匹配 (筛选优质点，保证1对1匹配)
            CodeBookMatrix = np.array([i for i in CodeBook.values()])
            matches = bf.match(desc_query, CodeBookMatrix)
            GoodMatches = [(match.trainIdx, match.queryIdx, match.distance) for match in matches if match.distance < 0.3]
            QueryIndex = Remove_duplication(sorted(GoodMatches))

            # 更新密码本，更新密码本最大索引值，更新测试图像索引
            CodeBook, CodeBookNum, UpdatedIndexCode = Update_CodeBook_IndexCode(
                CodeBook, CodeBookNum, QueryIndex, desc_query)

            # 计算当前图像在密码本中的 num_appear 值
            num_appear = len(QueryIndex)

            # 计算与各个节点中索引的 n 值，并计算 s 值
            for o in range(1, len(NodeBook) + 1):
                n = CountSame(UpdatedIndexCode, NodeBook[o])
                s = num_appear * n
                s = n

                res.append(s)
            
            # 更新节点索引字典
            NodeNum += 1
            NodeBook[NodeNum] = UpdatedIndexCode

            # 计算s所占百分比
            ResSum = float(sum(res))
            TheRes = [i/ResSum for i in res]


        print(ResNum, TheRes)
        print(ResNum, res)
        ResNum += 1