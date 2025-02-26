import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier,export_text,plot_tree
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# # 读取数据
# file_path =r"D:\Code\Social_segregation\data\SSI_golbal_data.csv"  # 修改为你的文件路径
# df = pd.read_csv(file_path)
# # 选择用于聚类的特征
# features = ["Theme1", "Theme2", "Theme3", "Theme4"]
# X = df[features]
#
# # 进行 Hierarchical Clustering（不进行标准化）
# linkage_matrix = linkage(X, method='ward')
#
# # 绘制树状图（Dendrogram）
# plt.figure(figsize=(12, 6))
# dendrogram(linkage_matrix, labels=df["City"].values, leaf_rotation=90, leaf_font_size=10)
# plt.title("Hierarchical Clustering Dendrogram (No Scaling)")
# plt.xlabel("Cities")
# plt.ylabel("Distance")
# plt.show()
#
# # 最大剪切距离（Maximum Distance Cut）
# last_merges = linkage_matrix[-10:, 2]  # 取最后 10 次合并的距离
# differences = last_merges[1:] - last_merges[:-1]  # 计算相邻合并的距离变化
#
# # 找到最大剪切距离（即最大跳跃点）
# best_cut_index = differences.argmax() + 1  # 找到最大跳跃点对应的索引
# best_k_distance_cut = len(last_merges) - best_cut_index + 1  # 计算最佳簇数
#
# # 依据最大剪切距离进行聚类
# clusters_distance_cut = fcluster(linkage_matrix, last_merges[best_cut_index], criterion='distance')
# df["Cluster_Max_Distance_Cut"] = clusters_distance_cut
#
# print(f"Best k from Maximum Distance Cut: {best_k_distance_cut}")

def apply_decision_tree_hierarchy(city_list,n_clusters=None):
    data = np.array([[city.theme1, city.theme2, city.theme3, city.theme4] for city in city_list])
    city_names = [city.name for city in city_list]
    linkage_matrix = linkage(data, method='ward')
    if n_clusters is None:
        # 自动确定最佳聚类数
        last_merges = linkage_matrix[-10:, 2]
        differences = last_merges[1:] - last_merges[:-1]
        best_cut_index = differences.argmax() + 1
        n_clusters = len(last_merges) - best_cut_index + 1
        print(f"Best k from Maximum Distance Cut: {n_clusters}")
    # 进行聚类
    clusters = fcluster(linkage_matrix, n_clusters, criterion='maxclust')
    for city, cluster in zip(city_list, clusters):
            city.cluster_class = cluster

    df = pd.DataFrame({
        "City": city_names,
        "Cluster": clusters,
        "Theme1": [city.theme1 for city in city_list],
        "Theme2": [city.theme2 for city in city_list],
        "Theme3": [city.theme3 for city in city_list],
        "Theme4": [city.theme4 for city in city_list]
    })
    # 决策树分类器
    # X = df[["Theme 1", "Theme 2", "Theme 3", "Theme 4"]]
    # y = df["Cluster"]
    # clf = DecisionTreeClassifier(random_state=0, max_depth=3)  # 限制树深度以提升可解释性
    # clf.fit(X, y)
    clf = DecisionTreeClassifier(random_state=0, max_depth=3)
    clf.fit(data, clusters)
    feature_importance = pd.DataFrame({
        'feature': ['Theme1', 'Theme2', 'Theme3', 'Theme4'],
        'importance': clf.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance)

    # 决策树可视化
    plt.figure(figsize=(12, 8))
    plot_tree(clf,
              feature_names=["Theme1", "Theme2", "Theme3", "Theme4"],
              class_names=[str(i) for i in np.unique(clusters)],
              filled=True)
    plt.title("Decision Tree Visualization")
    plt.show()

    # # 获取特征重要性
    # feature_importance = pd.DataFrame({
    #     "Feature": X.columns,
    #     "Importance": clf.feature_importances_
    # }).sort_values(by="Importance", ascending=False)

    # 可视化 1: 特征重要性柱状图
    plt.figure(figsize=(8, 5))
    sns.barplot(x=feature_importance["Importance"], y=feature_importance["Feature"], palette="Blues")
    plt.title("Feature Importance (Decision Tree Analysis)")
    plt.xlabel("Importance Score")
    plt.ylabel("Feature")
    plt.show()

    # 可视化 2: PCA 降维后散点图
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(data)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=reduced_data[:, 0], y=reduced_data[:, 1], hue=clusters, palette="Set2", s=100)
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.title("K-Means Clustering (PCA Projection)")
    plt.legend(title="Cluster")
    plt.show()

    # 可视化变量分布（箱线图）
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Cluster", y="value", hue="variable",
                data=pd.melt(df, id_vars=["City", "Cluster"], value_vars=["Theme 1", "Theme 2", "Theme 3", "Theme 4"]))
    plt.title("Boxplot of Variables Across Clusters")
    plt.legend(title="Variable")
    plt.show()

    # 可视化变量贡献度（雷达图）
    cluster_means = df.groupby("Cluster").mean(numeric_only=True)
    num_vars = len(cluster_means.columns)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_ylim(0.45, 0.65)  # 设置雷达图的值域
    for idx, row in cluster_means.iterrows():
        ax.plot(angles + [angles[0]], row.tolist() + [row.tolist()[0]], label=f"Cluster {idx}")
    ax.set_xticks(angles)
    ax.set_xticklabels(cluster_means.columns)
    ax.set_title("Radar Chart of Cluster Characteristics")
    ax.legend()
    plt.show()
    return city_list, df, feature_importance
if __name__ == '__main__':
    from Social_segregation.data_struct.data_reader import data_reader,save_results_to_csv,save_city_location
    #from visual_analysis_first_paper import plot_city_data_by_class
    from Social_segregation.visual import plot_city_data_combined,plot_city_data_by_cluster

    file_path = r"D:\Code\Social_segregation\data\SSI_golbal_data.csv"
    city_list = data_reader(file_path,3)
    city_list,df, importance_df= apply_decision_tree_hierarchy(city_list)

    plot_city_data_by_cluster(city_list)
    #save_results_to_csv(city_list, r"D:\Code\Social_segregation\data\SSI_golbal_data_kmeans_result.csv")
    print(importance_df)