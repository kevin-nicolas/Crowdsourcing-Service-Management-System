"""
协同过滤算法
"""
from abc import ABCMeta, abstractmethod
import numpy as np
from collections import defaultdict
import pymysql

def distance(point1, point2):  # 计算距离（欧几里得距离）
    return np.sqrt(np.sum((point1 - point2) ** 2))

def k_means(data, k, max_iter=10000):
    centers = {}  # 初始聚类中心
    # 初始化，随机选k个样本作为初始聚类中心。 random.sample(): 随机不重复抽取k个值
    n_data = data.shape[0]   # 样本个数
    for idx, i in enumerate(random.sample(range(n_data), k)):
        # idx取值范围[0, k-1]，代表第几个聚类中心;  data[i]为随机选取的样本作为聚类中心
        centers[idx] = data[i]  

    # 开始迭代
    for i in range(max_iter):  # 迭代次数
        print("开始第{}次迭代".format(i+1))
        clusters = {}    # 聚类结果，聚类中心的索引idx -> [样本集合]
        for j in range(k):  # 初始化为空列表
            clusters[j] = []
            
        for sample in data:  # 遍历每个样本
            distances = []  # 计算该样本到每个聚类中心的距离 (只会有k个元素)
            for c in centers:  # 遍历每个聚类中心
                # 添加该样本点到聚类中心的距离
                distances.append(distance(sample, centers[c])) 
            idx = np.argmin(distances)  # 最小距离的索引
            clusters[idx].append(sample)   # 将该样本添加到第idx个聚类中心
            
        pre_centers = centers.copy()  # 记录之前的聚类中心点

        for c in clusters.keys():
            # 重新计算中心点（计算该聚类中心的所有样本的均值）
            centers[c] = np.mean(clusters[c], axis=0)
  
        is_convergent = True
        for c in centers:
            if distance(pre_centers[c], centers[c]) > 1e-8:  # 中心点是否变化
                is_convergent = False
                break
        if is_convergent == True:  
            # 如果新旧聚类中心不变，则迭代停止
            break
    return centers, clusters

def predict(p_data, centers):  # 预测新样本点所在的类
    # 计算p_data 到每个聚类中心的距离，然后返回距离最小所在的聚类。
    distances = [distance(p_data, centers[c]) for c in centers]  
    return np.argmin(distances)

class CF_base(metaclass=ABCMeta):
    def __init__(self, k=3):
        self.k = k
        self.n_user = None
        self.n_item = None

    @abstractmethod
    def init_param(self, data):
        pass

    @abstractmethod
    def cal_prediction(self, *args):
        pass

    @abstractmethod
    def cal_recommendation(self, user_id, data):
        pass

    def fit(self, data):
        # 计算所有用户的推荐物品
        self.init_param(data)
        all_users = []
        for i in range(self.n_user):
            all_users.append(self.cal_recommendation(i, data))
        return all_users

class CF_svd(CF_base):
    """
    基于矩阵分解的协同过滤算法
    """

    def __init__(self, k=3, r=3):
        super(CF_svd, self).__init__(k)
        self.r = r  # 选取前k个奇异值
        self.uk = None  # 用户的隐因子向量
        self.vk = None  # 物品的隐因子向量
        return

    def init_param(self, data):
        # 初始化，预处理
        self.n_user = data.shape[0]
        self.n_item = data.shape[1]
        self.svd_simplify(data)
        return data

    def svd_simplify(self, data):
        # 奇异值分解以及简化
        u, s, v = np.linalg.svd(data)
        u, s, v = u[:, :self.r], s[:self.r], v[:self.r, :]  # 简化
        sk = np.diag(np.sqrt(s))  # r*r
        self.uk = u @ sk  # m*r
        self.vk = sk @ v  # r*n
        return

    def cal_prediction(self, user_ind, item_ind, user_row):
        rate_ave = np.mean(user_row)  # 用户已购物品的评价的平均值(未评价的评分为0)
        return rate_ave + self.uk[user_ind] @ self.vk[:, item_ind]  # 两个隐因子向量的内积加上平均值就是最终的预测分值

    def cal_recommendation(self, user_ind, data):
        # 计算目标用户的最具吸引力的k个物品list
        item_prediction = defaultdict(float)
        user_row = data[user_ind]
        un_purchase_item_inds = np.where(user_row == 0)[0]
        for item_ind in un_purchase_item_inds:
            item_prediction[item_ind] = self.cal_prediction(user_ind, item_ind, user_row)
        res = sorted(item_prediction, key=item_prediction.get, reverse=True)
        return res[:self.k]


if __name__ == '__main__':

    # 接包人员投递矩阵
    J = [
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 1]]

    # 众包项目邀请矩阵
    Z = [
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0]]

    # 偏好矩阵
    P2 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # 取数据
    db = pymysql.connect("localhost", "root", "root", "Crowdsourcing")
    cursor = db.cursor()
    sqlj = "SELECT * FROM user_task"

    try:
        cursor.execute(sqlj)
        resultj = cursor.fetchall()
        for i in resultj:
            if i[0]%2018000 < 10:
                if i[3] == "投递中":
                    if i[1] < 10:
                        J[i[1]%2018000][i[1]] = 1
    sqlz = "SELECT * FROM item"

    try:
        cursor.execute(sqlz)
        resultz = cursor.fetchall()
        for i in resultz:
            if i[0] < 10:
                if i[16]%2018000 < 10 :
                    Z[i[0]][i[16]] = 1

    # 众包项目邀请矩阵转置
    ZT = [[Z[j][i] for j in range(len(Z))] for i in range(len(Z[0]))]

    # 求偏好矩阵
    for i in range(len(J)):
        for j in range(len(ZT)):
            P2[i][j] = J[i][j] + ZT[i][j]
            if P2[i][j] == 2:
                P2[i][j] = 1
            else:
                P2[i][j] = 0

    # 新的偏好矩阵
    P2T = [[P2[j][i] for j in range(len(P2))] for i in range(len(P2[0]))]
    
    # 基于众包项目信息的接包人员发出投递的矩阵基于众包项目信息的接包人员发出投递的矩阵J2
    J2 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    # 基于接包人员信息的众包项目发出邀请的矩阵Z2
    Z2 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    for i in range(len(J)):
        for j in range(len(P2T)):
            J2[i][j] = J[i][j] + P2T[i][j]
    
    for i in range(len(J)):
        for j in range(len(P2T)):
            Z2[i][j] = Z[i][j] + P2T[i][j]
    
    # K-Meams聚类   
    centroidsJ2, clusterJ2 = k_means(J2, 3)
    centroidsZ2, clusterZ2 = k_means(Z2, 3)
    
    # 基于矩阵分解的协同过滤算法
    for c in clusterJ2:
        data1 = np.array(c)
        cf1 = CF_svd(k=3, r=3)
        ans1 = cf1.fit(data1)
        print(ans1) # 推荐项目
    
    for c in clusterZ2:
        data2 = np.array(c)
        cf2 = CF_svd(k=3, r=3)
        ans2 = cf2.fit(data2)
        print(ans2) # 推荐接包人员
