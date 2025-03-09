from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier, plot_tree
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score

def apply_decision_tree_kmeans_analysis_moran(city_list, n_clusters):
    '''
    使用 K-Means 进行聚类，并使用决策树分析特征重要性
    :param city_list: list[City] 城市数据
    :param n_clusters: 期望的聚类数量
    :return: 更新 city.cluster_class, 并返回数据分析结果
    '''
    data = np.array([[city.theme1_moran, city.theme2_moran, city.theme3_moran, city.theme4_moran, city.themes_moran] for city in city_list])
    city_names = [city.name for city in city_list]
    theme_names = ["SES", "HCD", "MSL", "HTT", "Overall"]
    # scaler = StandardScaler()
    # X_scaled = scaler.fit_transform(data)

    # KMeans 聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(data)
    for city, label in zip(city_list, labels):
        city.cluster_class = label
    # 构建 DataFrame
    df = pd.DataFrame({
        "City": city_names,
        "Cluster": labels,
        "theme1_moran": [city.theme1_moran for city in city_list],
        "theme2_moran": [city.theme2_moran for city in city_list],
        "theme3_moran": [city.theme3_moran for city in city_list],
        "theme4_moran": [city.theme4_moran for city in city_list],
        "themes_moran": [city.themes_moran for city in city_list]
    })

    # 决策树分类器
    X = df[["theme1_moran", "theme2_moran", "theme3_moran", "theme4_moran",'themes_moran']]
    y = df["Cluster"]
    clf = DecisionTreeClassifier(random_state=0, max_depth=3)  # 限制树深度以提升可解释性
    cv_scores = cross_val_score(clf, X, y, cv=5)
    mean_accuracy = cv_scores.mean()
    clf.fit(X, y)
    print(f"决策树模型的平均准确率（5折交叉验证）: {mean_accuracy:.4f}")
#决策树可视化
    plt.figure(figsize=(12, 8))
    plot_tree(clf, feature_names=X.columns, class_names=[str(i) for i in np.unique(y)], filled=True)
    plt.title("Decision Tree Visualization")
    plt.show()

    # 获取特征重要性
    feature_importance = pd.DataFrame({
        "Feature": X.columns,
        "Importance": clf.feature_importances_
    }).sort_values(by="Importance", ascending=False)

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
    sns.scatterplot(x=reduced_data[:, 0], y=reduced_data[:, 1], hue=labels, palette="Set2", s=100)
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.title("K-Means Clustering (PCA Projection)")
    plt.legend(title="Cluster")
    plt.show()
    #feature_names = ["SES", "HCD", "MSL", "HTT"]
    # 可视化变量分布（箱线图）
    plt.figure(figsize=(12, 6))
    melted_df = pd.melt(df, id_vars=["City", "Cluster"],
                        value_vars=["theme1_moran", "theme2_moran", "theme3_moran", "theme4_moran", 'themes_moran'])
    melted_df['variable'] = melted_df['variable'].map(
        {f"theme{i + 1}_moran": name for i, name in enumerate(theme_names[:4])})
    melted_df.loc[melted_df['variable'] == 'themes_moran', 'variable'] = theme_names[4]
    sns.boxplot(x="Cluster", y="value", hue="variable", data=melted_df)
    # sns.boxplot(x="Cluster", y="value", hue="variable",
    #             data=pd.melt(df, id_vars=["City", "Cluster"],
    #                          value_vars=["theme1_moran", "theme2_moran", "theme3_moran", "theme4_moran",'themes_moran']))
    plt.title("Boxplot of Variables Across Clusters")
    plt.legend(title="Variable")
    plt.show()

    # 可视化变量贡献度（雷达图）
    cluster_means = df.groupby("Cluster").mean(numeric_only=True)
    cluster_means.columns = theme_names  # 重命名列
    num_vars = len(cluster_means.columns)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    #ax.set_ylim(0.45, 0.65)  # 设置雷达图的值域
    for idx, row in cluster_means.iterrows():
        values = row.tolist()
        values += values[:1]
        ax.plot(angles + [angles[0]], values, label=f"Cluster {idx}")
    ax.set_xticks(angles)
    ax.set_xticklabels(cluster_means.columns)
    ax.set_title("Radar Chart of Cluster Characteristics")
    ax.legend()
    plt.show()
    return city_list, df, feature_importance
if __name__ == '__main__':
    from data_process.data_reader import data_reader,save_results_to_csv,save_city_location,read_moran_results
    #from visual_analysis_first_paper import plot_city_data_by_class
    from visual.visual import plot_city_data_by_cluster

    file_path = r"D:\Code\Social_segregation\data\SSI_golbal_data.csv"
    moran_results_path = r'D:\Code\Social_segregation\data\morans_i_results.csv'

    city_list = data_reader(file_path,3)
    city_list=read_moran_results(moran_results_path,city_list)
    city_list,df, importance_df= apply_decision_tree_kmeans_analysis_moran(city_list, 2)
    #save_city_location(city_list,r"D:\Code\Social_segregation\data\SSI_golbal_data_kmeans_result.geojson")
    #plot_city_data_by_cluster(city_list)
    #save_results_to_csv(city_list, r"D:\Code\Social_segregation\data\SSI_golbal_data_moran_kmeans_result.csv")
    #print(importance_df)

