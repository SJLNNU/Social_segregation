import geopandas as gpd
import numpy as np
import pandas as pd
import statsmodels.api as sm
from mgwr.gwr import GWR
from mgwr.sel_bw import Sel_BW
from shapely.geometry import shape


def run_gwr(file_path, y_var="themes", x_vars=["theme1", "theme2", "theme3", "theme4"],
            output_csv="GWR_Regression_Summary.csv"):
    """
    运行地理加权回归（GWR），计算全局统计结果，类似于多元线性回归（OLS）

    参数：
        file_path: str  - GeoJSON 文件路径
        y_var: str  - 因变量（默认 "themes"）
        x_vars: list - 自变量列表（默认 ["theme1", "theme2", "theme3", "theme4"]）
        output_csv: str - 结果保存的 CSV 文件名（默认 "GWR_Regression_Summary.csv"）

    返回：
        summary_df: pd.DataFrame - 回归结果 DataFrame
    """
    # 1. 读取数据
    gdf = gpd.read_file(file_path)

    # 2. 确保数据是投影坐标系（GWR 需要米为单位）
    if gdf.crs.is_geographic:
        gdf = gdf.to_crs(epsg=3857)

    # 3. 提取中心点坐标
    gdf["centroid"] = gdf.geometry.centroid
    coords = np.array(list(zip(gdf.centroid.x, gdf.centroid.y)))

    # 4. 提取 X 和 Y
    y = gdf[y_var].values.reshape(-1, 1)
    X = gdf[x_vars].values
    X = sm.add_constant(X)

    # 5. 选择最佳带宽
    bandwidth = Sel_BW(coords, y, X).search()

    # 6. 运行 GWR
    model = GWR(coords, y, X, bandwidth)
    results = model.fit()

    # 7. 计算全局统计结果
    coeff_means = np.mean(results.params, axis=0)  # 平均回归系数
    coeff_se = np.std(results.params, axis=0) / np.sqrt(len(results.params))  # 标准误差
    t_values = coeff_means / coeff_se  # t 值
    p_values = sm.stats.ztest(results.params, value=0, alternative='two-sided')[1]  # p 值

    # 8. 生成回归结果表
    summary_df = pd.DataFrame({
        "变量": ["Intercept"] + x_vars,
        "回归系数": coeff_means,
        "标准误差": coeff_se,
        "t 值": t_values,
        "p 值": p_values
    })
    summary_df.loc[len(summary_df)] = ["调整 R²", results.adj_R2, np.nan, np.nan, np.nan]

    # 9. 保存结果
    #summary_df.to_csv(output_csv, index=False)
    #print(f"✅ GWR 结果已保存到: {output_csv}")

    print( summary_df)


def run_gwr_filtered(file_path, init_class_value, y_var="themes", x_vars=["theme1", "theme2", "theme3", "theme4"],
                     output_csv=None):
    """
    运行地理加权回归（GWR），但仅对 `init_class` 为指定值的区域进行计算

    参数：
        file_path: str  - GeoJSON 文件路径
        init_class_value: int - 需要筛选的类别（0, 1, 2）
        y_var: str  - 因变量（默认 "themes"）
        x_vars: list - 自变量列表（默认 ["theme1", "theme2", "theme3", "theme4"]）
        output_csv: str - 结果保存的 CSV 文件名（默认 "GWR_Regression_Summary_Class_X.csv"）

    返回：
        summary_df: pd.DataFrame - 回归结果 DataFrame
    """
    # 1. 读取数据
    gdf = gpd.read_file(file_path)

    # 2. 仅保留 `init_class == init_class_value` 的行
    gdf_filtered = gdf[gdf["init_class"] == init_class_value].copy()
    if gdf_filtered.empty:
        print(f"⚠️ 过滤后没有数据 (init_class = {init_class_value})，请检查数据！")
        return None

    # 3. 确保数据是投影坐标系
    if gdf_filtered.crs.is_geographic:
        gdf_filtered = gdf_filtered.to_crs(epsg=3857)

    # 4. 提取中心点坐标
    gdf_filtered["centroid"] = gdf_filtered.geometry.centroid
    coords = np.array(list(zip(gdf_filtered.centroid.x, gdf_filtered.centroid.y)))

    # 5. 提取 X 和 Y
    y = gdf_filtered[y_var].values.reshape(-1, 1)
    X = gdf_filtered[x_vars].values
    X = sm.add_constant(X)

    # 6. 选择最佳带宽
    bandwidth = Sel_BW(coords, y, X).search()

    # 7. 运行 GWR
    model = GWR(coords, y, X, bandwidth)
    results = model.fit()

    # 8. 计算全局统计结果
    coeff_means = np.mean(results.params, axis=0)
    coeff_se = np.std(results.params, axis=0) / np.sqrt(len(results.params))
    t_values = coeff_means / coeff_se
    p_values = sm.stats.ztest(results.params, value=0, alternative='two-sided')[1]

    # 9. 生成回归结果表
    summary_df = pd.DataFrame({
        "变量": ["Intercept"] + x_vars,
        "回归系数": coeff_means,
        "标准误差": coeff_se,
        "t 值": t_values,
        "p 值": p_values
    })
    summary_df.loc[len(summary_df)] = ["调整 R²", results.adj_R2, np.nan, np.nan, np.nan]
    print( summary_df)
    # # 10. 保存结果
    # if output_csv is None:
    #     output_csv = f"GWR_Regression_Summary_Class_{init_class_value}.csv"
    #
    # summary_df.to_csv(output_csv, index=False)
    # print(f"✅ GWR 结果（init_class={init_class_value}）已保存到: {output_csv}")
    #
    # return summary_df

if __name__ == '__main__':
    file_path=r'D:\Code\Social_segregation\data\Census_tract\Portland_census_tract.geojson'
    run_gwr(file_path)
    #run_gwr_filtered(file_path, init_class_value=0)
    #run_gwr_filtered(file_path, init_class_value=1)
    run_gwr_filtered(file_path,init_class_value=2)
