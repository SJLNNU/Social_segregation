import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd

# 读取数据
file_path = r"D:\Code\Social_segregation\data\SSI_golbal_data.csv"  # 修改为你的文件路径
df = pd.read_csv(file_path)

# 选择用于聚类的特征
features = ["Theme1", "Theme2", "Theme3", "Theme4"]
X = df[features]

# 确定最佳 K 值（Elbow Method）
wcss = []  # 簇内误差平方和
K_range = range(1, 10)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

# 绘制 Elbow Method 图表
plt.figure(figsize=(8, 5))
plt.plot(K_range, wcss, marker='o', linestyle='-', color='r')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('WCSS (Within-Cluster Sum of Squares)')
plt.title('Elbow Method (No Scaling)')
plt.grid()
plt.show()

# 进行 K-Means 聚类，并计算 Silhouette Score
def evaluate_kmeans(k, X):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X)
    score = silhouette_score(X, cluster_labels)
    return cluster_labels, score

# 计算 k=3 和 k=4 的聚类结果及 Silhouette Score
df["Cluster_k3"], silhouette_k3 = evaluate_kmeans(3, X)
df["Cluster_k4"], silhouette_k4 = evaluate_kmeans(4, X)

# 打印 Silhouette Scores
print(f"Silhouette Score for k=3: {silhouette_k3}")
print(f"Silhouette Score for k=4: {silhouette_k4}")
