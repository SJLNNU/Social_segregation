import geopandas as gpd
import numpy as np
import pandas as pd
import statsmodels.api as sm
from mgwr.gwr import GWR
from mgwr.sel_bw import Sel_BW
import os
from scipy.stats import ttest_ind_from_stats


def run_gwr(gdf, y_var="themes", x_vars=["theme1", "theme2", "theme3", "theme4"]):
    """ 运行 GWR 并返回结果 """
    if gdf.crs.is_geographic:
        gdf = gdf.to_crs(epsg=3857)

    gdf["centroid"] = gdf.geometry.centroid
    coords = np.array(list(zip(gdf.centroid.x, gdf.centroid.y)))

    y = gdf[y_var].values.reshape(-1, 1)
    X = gdf[x_vars].values
    X = sm.add_constant(X)

    bandwidth = Sel_BW(coords, y, X).search()
    model = GWR(coords, y, X, bandwidth)
    results = model.fit()

    coeff_means = np.mean(results.params, axis=0)
    coeff_se = np.std(results.params, axis=0) / np.sqrt(len(results.params))
    t_values = coeff_means / coeff_se
    p_values = sm.stats.ztest(results.params, value=0, alternative='two-sided')[1]

    summary_df = pd.DataFrame({
        "变量": ["Intercept"] + x_vars,
        "回归系数": coeff_means,
        "标准误差": coeff_se,
        "t 值": t_values,
        "p 值": p_values
    })
    summary_df.loc[len(summary_df)] = ["调整 R²", results.adj_R2, np.nan, np.nan, np.nan]

    return summary_df, len(gdf)  # 返回结果和 Census Tract 数量


def run_gwr_filtered(gdf, init_class_value, y_var="themes", x_vars=["theme1", "theme2", "theme3", "theme4"]):
    """ 运行 GWR 但仅对 `init_class` 为指定值的区域进行计算 """
    gdf_filtered = gdf[gdf["init_class"] == init_class_value].copy()

    if gdf_filtered.empty:
        print(f"⚠️ 过滤后没有数据 (init_class = {init_class_value})，请检查数据！")
        return None, 0

    return run_gwr(gdf_filtered, y_var, x_vars)


def analyze_all_geojson_in_folder(folder_path):
    """ 处理文件夹中的所有 GeoJSON，计算 GWR 并分析趋势 """
    geojson_files = [f for f in os.listdir(folder_path) if f.endswith('.geojson')]

    all_results = []
    for file in geojson_files:
        file_path = os.path.join(folder_path, file)
        print(f"📂 处理文件: {file_path}")

        gdf = gpd.read_file(file_path)

        # 计算全城市 GWR
        global_results, n_global = run_gwr(gdf)

        # 计算高隔离 GWR (init_class=2)
        high_iso_results, n_high = run_gwr_filtered(gdf, init_class_value=2)

        if high_iso_results is not None and n_high > 1:  # 确保有足够数据进行计算
            # 计算变量趋势（t 检验）
            trend_results = []
            for var in ["theme1", "theme2", "theme3", "theme4"]:
                global_coeff = global_results[global_results["变量"] == var]["回归系数"].values[0]
                high_coeff = high_iso_results[high_iso_results["变量"] == var]["回归系数"].values[0]

                global_se = global_results[global_results["变量"] == var]["标准误差"].values[0]
                high_se = high_iso_results[high_iso_results["变量"] == var]["标准误差"].values[0]

                # t 检验（基于均值、标准误差和样本量）
                t_stat, p_value = ttest_ind_from_stats(mean1=global_coeff, std1=global_se, nobs1=n_global,
                                                       mean2=high_coeff, std2=high_se, nobs2=n_high)

                trend_results.append({
                    "文件名": file,
                    "变量": var,
                    "全城市系数": global_coeff,
                    "高隔离系数": high_coeff,
                    "变化幅度": high_coeff - global_coeff,
                    "t 值": t_stat,
                    "p 值": p_value
                })

            all_results.extend(trend_results)

    # 汇总结果
    trend_df = pd.DataFrame(all_results)
    print("\n📊 **最终分析结果:**")
    print(trend_df)
    #这里保存下来
    trend_df.to_csv(r'D:\Code\Social_segregation\data\Census_tract\trend_df.csv', index=False)
    return trend_df


if __name__ == '__main__':
    folder_path = r'/data/Census_tract'
    analyze_all_geojson_in_folder(folder_path)
