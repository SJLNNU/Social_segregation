import numpy as np
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import shap

def plot_standardized_coefficients(feature_names, standardized_coefficients):
    # 定义颜色映射（与小提琴图一致）
    color_map = {
        'SES': '#1f77b4',   # 深蓝
        'HCD': '#6a3d9a',   # 紫色
        'MSL': '#e377c2',   # 品红
        'H&T': '#2ca02c',   # 绿色
        'Comp.': '#17becf'  # 蓝绿色（如有需要）
    }

    # 倒序
    feature_names = feature_names[::-1]
    standardized_coefficients = standardized_coefficients[::-1]

    plt.figure(figsize=(10, 6))
    y_pos = range(len(feature_names))

    # 根据 feature_names 映射颜色
    colors = [color_map[feat] for feat in feature_names]

    bars = plt.barh(y_pos, standardized_coefficients, align='center', color=colors)
    plt.yticks(y_pos, feature_names)

    # 设置标题和标签
    plt.title('Standardized Coefficients (Beta Coefficients)')
    plt.xlabel('Coefficient Value')

    # 在条形上添加数值标签
    for i, v in enumerate(standardized_coefficients):
        plt.text(v if v >= 0 else v - 0.05, i, f'{v:.4f}', va='center')

    # 添加垂直线表示零点
    plt.axvline(x=0, color='k', linestyle='--')

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
    feature_names = ["SES", "HCD", "MSL", "H&T"]
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
    plot_standardized_coefficients(feature_names, standardized_coefficients)
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
    feature_names = ["SES", "HCD", "MSL", "H&T"]

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
    plot_standardized_coefficients(feature_names, standardized_coefficients)
    return importance_dict

def plot_shap_importance(feature_names, shap_values):
    # 定义颜色映射（与小提琴图一致）
    color_map = {
        'SES': '#1f77b4',   # 深蓝
        'HCD': '#6a3d9a',   # 紫色
        'MSL': '#e377c2',   # 品红
        'H&T': '#2ca02c',   # 绿色
        'Comp.': '#17becf'  # 蓝绿色
    }

    # 计算每个特征的平均绝对SHAP值
    mean_shap_values = np.abs(shap_values).mean(axis=0)
    
    # 计算百分比
    total_importance = np.sum(mean_shap_values)
    percentage_values = (mean_shap_values / total_importance) * 100

    # 倒序排序
    sorted_indices = np.argsort(percentage_values)
    feature_names = [feature_names[i] for i in sorted_indices]
    percentage_values = percentage_values[sorted_indices]

    plt.figure(figsize=(10, 6))
    y_pos = range(len(feature_names))

    # 根据feature_names映射颜色
    colors = [color_map[feat] for feat in feature_names]

    bars = plt.barh(y_pos, percentage_values, align='center', color=colors)
    plt.yticks(y_pos, feature_names)

    # 设置标题和标签
    plt.title('Feature Importance (SHAP Values)')
    plt.xlabel('Contribution Percentage (%)')

    # 在条形上添加百分比标签
    for i, v in enumerate(percentage_values):
        plt.text(v, i, f'{v:.1f}%', va='center')

    plt.tight_layout()
    plt.show()

def shap_importance_analysis(city_list):
    '''
    使用SHAP值进行特征重要性分析，评估四个主题对themes的贡献度
    :param city_list: list[City] 城市数据
    :return: dict 包含每个特征的重要性百分比
    '''
    X = np.array([[city.theme1, city.theme2, city.theme3, city.theme4] for city in city_list])
    y = np.array([city.themes for city in city_list])
    
    # 训练模型
    model = LinearRegression()
    model.fit(X, y)
    
    # 计算SHAP值
    explainer = shap.LinearExplainer(model, X)
    shap_values = explainer.shap_values(X)
    
    feature_names = ["SES", "HCD", "MSL", "H&T"]
    
    # 计算每个特征的平均绝对SHAP值
    mean_shap_values = np.abs(shap_values).mean(axis=0)
    
    # 计算百分比
    total_importance = np.sum(mean_shap_values)
    percentage_values = (mean_shap_values / total_importance) * 100
    
    # 创建重要性字典
    importance_dict = dict(zip(feature_names, percentage_values))
    
    # 打印结果
    print("\nSHAP-based Feature Importance (Percentage):")
    for name, percentage in importance_dict.items():
        print(f"{name}: {percentage:.2f}%")
    
    # 绘制可视化图表
    plot_shap_importance(feature_names, shap_values)
    
    return importance_dict


def shap_importance_analysis_with_selected_init_class(city_list,selected_init_class):
    '''
    使用SHAP值进行特征重要性分析，评估四个主题对themes的贡献度
    :param city_list: list[City] 城市数据
    :return: dict 包含每个特征的重要性百分比
    '''
    X = np.array([[city.theme1, city.theme2, city.theme3, city.theme4]
                  for city in city_list if city.init_class == selected_init_class])
    y = np.array([city.themes for city in city_list if city.init_class == selected_init_class])

    # 训练模型
    model = LinearRegression()
    model.fit(X, y)

    # 计算SHAP值
    explainer = shap.LinearExplainer(model, X)
    shap_values = explainer.shap_values(X)

    feature_names = ["SES", "HCD", "MSL", "H&T"]

    # 计算每个特征的平均绝对SHAP值
    mean_shap_values = np.abs(shap_values).mean(axis=0)

    # 计算百分比
    total_importance = np.sum(mean_shap_values)
    percentage_values = (mean_shap_values / total_importance) * 100

    # 创建重要性字典
    importance_dict = dict(zip(feature_names, percentage_values))

    # 打印结果
    print("\nSHAP-based Feature Importance (Percentage):")
    for name, percentage in importance_dict.items():
        print(f"{name}: {percentage:.2f}%")

    # 绘制可视化图表
    plot_shap_importance(feature_names, shap_values)

    return importance_dict