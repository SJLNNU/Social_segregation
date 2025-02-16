from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import random

def apply_kmeans_clustering(city_list, n_clusters):
    '''
    使用K-means算法进行聚类
    :param city_list: list[City] 城市数据
    :param n_clusters: 期望的聚类数量
    :return: 更新city.cluster_class
    '''
    data = np.array([[city.theme1, city.theme2, city.theme3, city.theme4] for city in city_list])
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto')
    labels = kmeans.fit_predict(data)

    for city, label in zip(city_list, labels):
        city.cluster_class = label
    return city_list


if __name__ == '__main__':
    from Social_segregation.struct.data_reader import data_reader,save_results_to_csv
    #from visual_analysis_first_paper import plot_city_data_by_class
    from Social_segregation.visual import plot_city_data_combined,plot_city_data_by_cluster

    file_path = r"D:\Code\Social_segregation\data\SSI_golbal_data.csv"
    city_list = data_reader(file_path,3)
    city_list = apply_kmeans_clustering(city_list, 3)
    plot_city_data_combined(city_list)
    plot_city_data_by_cluster(city_list)

    save_results_to_csv(city_list,r"D:\Code\Social_segregation\data\SSI_golbal_data_kmeans_result.csv")