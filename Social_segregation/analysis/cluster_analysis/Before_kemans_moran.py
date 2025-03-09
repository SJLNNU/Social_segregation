import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# 从 city_list 提取 theme1 ~ theme4 数据
def extract_features(city_list):
    data = []
    for city in city_list:
        data.append([city.theme1, city.theme2, city.theme3, city.theme4])
    return np.array(data)


# 计算 KMeans 的 SSE（Elbow Method）和 Silhouette Score
def analyze_k(city_list, max_k=10):
    data = extract_features(city_list)
    sse = []
    silhouette_scores = []
    k_values = range(2, max_k + 1)  # K 至少从 2 开始

    for k in k_values:
        kmeans = KMeans(n_clusters=k,  random_state=42, n_init=10)
        labels = kmeans.fit_predict(data)
        sse.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(data, labels))

    # 绘制 Elbow Method 图
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(k_values, sse, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of clusters (K)')
    plt.ylabel('Sum of Squared Errors (SSE)')
    plt.title('Elbow Method')

    # 绘制 Silhouette Score 图
    plt.subplot(1, 2, 2)
    plt.plot(k_values, silhouette_scores, marker='o', linestyle='-', color='g')
    plt.xlabel('Number of clusters (K)')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score Analysis')

    plt.tight_layout()
    plt.show()

    return k_values, sse, silhouette_scores

if __name__ == '__main__':
    from data_process.data_reader import data_reader

    # from visual_analysis_first_paper import plot_city_data_by_class

    file_path = r"D:\Code\Social_segregation\data\SSI_golbal_data.csv"
    city_list = data_reader(file_path, 3)    # 调用分析函数
    k_values,sse, silhouette_scores = analyze_k(city_list)
    best_k_elbow = k_values[np.argmin(np.gradient(sse))]  # 肘部法
    best_k_silhouette = k_values[np.argmax(silhouette_scores)]  # Silhouette Score
    print(best_k_elbow)
    print(best_k_silhouette)
