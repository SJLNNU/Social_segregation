import numpy as np
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import shap

def plot_standardized_coefficients(feature_names, standardized_coefficients):
    # 倒序feature_names和standardized_coefficients
    feature_names = feature_names[::-1]
    standardized_coefficients = standardized_coefficients[::-1]

    plt.figure(figsize=(10, 6))
    y_pos = range(len(feature_names))

    # 定义不同的颜色
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # 蓝、橙、绿、红

    # 创建水平条形图，使用不同的颜色
    bars = plt.barh(y_pos, standardized_coefficients, align='center', color=colors)
    plt.yticks(y_pos, feature_names)

    # 设置标题和标签
    plt.title('Standardized Coefficients (Beta Coefficients)')
    plt.xlabel('Coefficient Value')

    # 在条形上添加数值标签
    for i, v in enumerate(standardized_coefficients):
        plt.text(v, i, f' {v:.4f}', va='center')

    # 添加垂直线表示零点
    plt.axvline(x=0, color='k', linestyle='--')

    # 调整布局并显示图表
    plt.tight_layout()
    plt.show()

def relative_importance_analysis(city_list):
    '''
    进行Relative Importance Analysis (RIA)分析，评估四个主题对themes的贡献度，并以百分比显示在图表中
    :param city_list: list[City] 城市数据
    :return: None (在控制台输出结果)
    '''
    X = np.array([[city.theme1, city.theme2, city.theme3, city.theme4] for city in city_list])
    y = np.array([city.themes for city in city_list])
    model = LinearRegression()
    model.fit(X, y)
    r_squared = model.score(X, y)
    #feature_names = ["Theme1", "Theme2", "Theme3", "Theme4"]
    feature_names = ["SES", "HCD", "MSL", "HTT"]
    print(f"\nR² Score: {r_squared:.4f}")
    if r_squared<0.5:
        return None
        # 计算标准化回归系数
    std_X = np.std(X, axis=0)  # 计算每个主题的标准差
    std_y = np.std(y)  # 计算Themes的标准差
    standardized_coefficients = model.coef_ * (std_X / std_y)
    print("\nStandardized Coefficients (Beta Coefficients):")
    importance_dict = {}
    for name, coef in zip(feature_names, standardized_coefficients):
        print(f"{name}: {coef:.4f}")
        importance_dict[name] = coef  # 将计算结果存入字典


    # for name, coef in zip(feature_names, standardized_coefficients):
    #     print(f"{name}: {coef:.4f}")
    #plot_standardized_coefficients(feature_names, standardized_coefficients)
    return importance_dict

def relative_importance_analysis_with_selected_initclass(city_list, selected_init_class):
    '''
    进行Relative Importance Analysis (RIA)分析，评估四个主题对themes的贡献度，并以百分比显示在图表中
    :param city_list: list[City] 城市数据
    :param selected_init_class: 选定的类别
    :return: None (在控制台输出结果)
    '''
    X = np.array([[city.theme1, city.theme2, city.theme3, city.theme4]
                  for city in city_list if city.init_class == selected_init_class])
    y = np.array([city.themes for city in city_list if city.init_class == selected_init_class])

    if X.shape[0] < 3:  # 设定一个最小样本阈值
        print("Warning: Sample size too small for reliable importance analysis.")
        return

    model = LinearRegression()
    model.fit(X, y)

    r_squared = model.score(X, y)

    # feature_names = ["Theme1", "Theme2", "Theme3", "Theme4"]
    feature_names = ["SES", "HCD", "MSL", "HTT"]

    print(f"\nR² Score: {r_squared:.4f}")
    if r_squared<0.5:
        return None
    # 计算标准化回归系数
    std_X = np.std(X, axis=0)  # 计算每个主题的标准差
    std_y = np.std(y)  # 计算Themes的标准差
    print(model.coef_)
    standardized_coefficients = model.coef_ * (std_X / std_y)

    # print("\nStandardized Coefficients (Beta Coefficients):")
    # for name, coef in zip(feature_names, standardized_coefficients):
    #     print(f"{name}: {coef:.4f}")
    # #plot_standardized_coefficients(feature_names, standardized_coefficients)

    print("\nStandardized Coefficients (Beta Coefficients):")
    importance_dict = {}
    for name, coef in zip(feature_names, standardized_coefficients):
        print(f"{name}: {coef:.4f}")
        importance_dict[name] = coef  # 将计算结果存入字典

    # for name, coef in zip(feature_names, standardized_coefficients):
    #     print(f"{name}: {coef:.4f}")
    # plot_standardized_coefficients(feature_names, standardized_coefficients)
    return importance_dict