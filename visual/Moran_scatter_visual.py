# 导入必要的库
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 设置字体为Calibri
plt.rcParams['font.family'] = 'Calibri'
plt.rcParams['font.size'] = 20

# 读取数据文件
file_path = r"D:\Code\Social_segregation\data\morans_i_results_added_z.csv"
df = pd.read_csv(file_path)

# 处理列名，确保一致性
df.rename(columns={"city_name": "City", "themes_moran": "Themes_Moran"}, inplace=True)

# 去除 "_census_tract" 后缀，仅保留城市名称
df["City"] = df["City"].str.replace("_census_tract", "", regex=True)

# 选择要可视化的主题列
theme_columns = ["theme1_moran", "theme2_moran", "theme3_moran", "theme4_moran", "Themes_Moran"]
theme_p_columns = ["theme1_moran_p", "theme2_moran_p", "theme3_moran_p", "theme4_moran_p", "themes_moran_p"]
theme_names = ["SES", "HCD", "MSL", "HT", "Comp."]

# 设置颜色方案
theme_colors = ["#1f77b4", "#6a3d9a", "#e377c2", "#2ca02c", "#17becf"]  # 主题色
mean_line_color = "#333333"  # 均值线颜色
box_color = "#f0f0f0"  # 箱线图颜色
reference_line_color = "#cccccc"  # 参考线颜色

# 计算全局范围
global_min = df[theme_columns].min().min()
global_max = df[theme_columns].max().max()
global_range = global_max - global_min

# 创建更灵活的布局
fig = plt.figure(figsize=(18, 12))
gs = plt.GridSpec(2, 6, height_ratios=[1, 1])  # 将宽度分成6份以便更精确控制

# 创建前3个子图（第一行）
axes = []
for i in range(3):
    axes.append(plt.subplot(gs[0, i*2:i*2+2]))  # 每个图占2个单位宽度

# 创建最后2个子图（第二行，居中）
axes.append(plt.subplot(gs[1, 1:3]))  # 第4个图，从第1个单位开始，占2个单位
axes.append(plt.subplot(gs[1, 3:5]))  # 第5个图，从第3个单位开始，占2个单位

# 为每个主题创建子图
for idx, (theme, theme_p, name, color) in enumerate(zip(theme_columns, theme_p_columns, theme_names, theme_colors)):
    # 按当前主题的Moran's I值排序并添加排名
    df_sorted = df.sort_values(by=theme, ascending=False).copy()
    df_sorted['Rank'] = range(1, len(df_sorted) + 1)
    
    # 计算均值
    mean_value = df_sorted[theme].mean()
    
    # 计算P值统计信息
    p_values = df_sorted[theme_p].dropna()
    total_count = len(p_values)
    significant_001 = (p_values < 0.001).sum()
    significant_01 = ((p_values >= 0.001) & (p_values < 0.01)).sum()
    significant_05 = ((p_values >= 0.01) & (p_values < 0.05)).sum()
    not_significant = (p_values >= 0.05).sum()
    
    # 根据显著性水平设置散点颜色（可选：如果所有都显著，就保持原色）
    # 这里我们使用原色，但添加文本说明显著性
    if not_significant > 0:
        # 如果有不显著的点，使用颜色区分
        colors_map = []
        for p_val in df_sorted[theme_p]:
            if pd.isna(p_val):
                colors_map.append('#cccccc')  # 灰色表示缺失
            elif p_val < 0.001:
                colors_map.append(color)  # 原色表示p<0.001
            elif p_val < 0.01:
                colors_map.append(color)  # 原色
            elif p_val < 0.05:
                colors_map.append('#888888')  # 灰色表示p<0.05
            else:
                colors_map.append('#cccccc')  # 浅灰色表示不显著
        # 使用matplotlib的scatter来支持自定义颜色
        axes[idx].scatter(df_sorted[theme], df_sorted['Rank'], 
                         c=colors_map, alpha=0.6, s=100)
    else:
        # 如果全部显著，使用原色
        sns.scatterplot(data=df_sorted, x=theme, y='Rank', color=color, alpha=0.6, ax=axes[idx])
    
    # 添加均值线
    axes[idx].axvline(x=mean_value, color=mean_line_color, linestyle='-', linewidth=2)
    
    # 添加参考线（0.3, 0.5, 0.7）
    for ref_value in [0.3, 0.5, 0.7]:
        axes[idx].axvline(x=ref_value, color=reference_line_color, linestyle='--', alpha=0.5)
    
    # # 设置标题和标签，添加显著性信息
    # if not_significant == 0:
    #     if significant_001 == total_count:
    #         sig_text = "All significant (p<0.001)"
    #     else:
    #         sig_text = f"All significant (p<0.05)"
    # else:
    #     sig_text = f"{total_count - not_significant}/{total_count} significant (p<0.05)"
    sig_text = f"{total_count - not_significant}/{total_count} significant (p<0.05)"
    axes[idx].set_title(f"{name}", pad=20, fontsize=18)
    if idx < 3:  # 第一行的图
        if idx == 1:  # 只保留中间图的x轴标签
            axes[idx].set_xlabel("Moran's I Value")
        else:
            axes[idx].set_xlabel("")
        if idx == 0:  # 只保留第一个图的y轴标签
            axes[idx].set_ylabel("Rank")
        else:
            axes[idx].set_ylabel("")
    else:  # 第二行的图
        if idx == 3:  # 只保留第一个图的y轴标签
            axes[idx].set_ylabel("Rank")
            axes[idx].set_xlabel("Moran's I Value")
        else:
            axes[idx].set_ylabel("")
            axes[idx].set_xlabel("")
    
    # 反转Y轴，使排名1在最上方
    axes[idx].invert_yaxis()
    
    # 添加均值标注（移到顶部）
    axes[idx].text(mean_value, 1, f'Mean: {mean_value:.3f}', 
                  rotation=90, va='top', ha='right',
                  bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    # 统一设置x轴范围
    
    axes[idx].set_xlim(global_min - 0.1*global_range, global_max + 0.1*global_range)
    
    # 添加参考线标注
    axes[idx].text(0.3, len(df_sorted)/2, '0.3', rotation=90, va='center', ha='right', color='#666666', fontweight='bold')
    axes[idx].text(0.5, len(df_sorted)/2, '0.5', rotation=90, va='center', ha='right', color='#666666', fontweight='bold')
    axes[idx].text(0.7, len(df_sorted)/2, '0.7', rotation=90, va='center', ha='right', color='#666666', fontweight='bold')
    
    # 标注前3名城市
    for i in range(3):
        city = df_sorted.iloc[i]['City']
        value = df_sorted.iloc[i][theme]
        axes[idx].text(value, i+1, city, fontsize=16, ha='left', va='center', fontweight='bold')
    
    # 在图的右上角添加P值统计文本框（可选，如果需要更详细的信息）
    # 如果需要更详细的P值统计，可以取消下面的注释
    # stats_text = f"p<0.001: {significant_001}\np<0.01: {significant_01}\np<0.05: {significant_05}"
    # if not_significant > 0:
    #     stats_text += f"\np≥0.05: {not_significant}"
    # axes[idx].text(0.98, 0.98, stats_text, transform=axes[idx].transAxes,
    #               fontsize=12, va='top', ha='right',
    #               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
    #               family='monospace')

# 添加整体标题和说明
#fig.suptitle("Moran's I Distribution Across Themes", y=1.02, fontsize=24)
# fig.text(0.5, 0.01, "Note: Dashed lines indicate reference values (0.3, 0.5, 0.7) for spatial autocorrelation strength", 
#          ha='center', fontsize=10)

# 调整布局
plt.tight_layout()

# 保存图表
plt.savefig('moran_small_multiples.png', dpi=300, bbox_inches='tight')
plt.show()

# 创建极值表格
extreme_values = pd.DataFrame()
for theme, name in zip(theme_columns, theme_names):
    df_sorted = df.sort_values(by=theme, ascending=False)
    top3 = df_sorted[['City', theme]].head(3)
    bottom3 = df_sorted[['City', theme]].tail(3)
    
    top3.columns = ['City', f'{name}_Top3']
    bottom3.columns = ['City', f'{name}_Bottom3']
    
    if extreme_values.empty:
        extreme_values = pd.concat([top3, bottom3], axis=1)
    else:
        extreme_values = pd.concat([extreme_values, top3[f'{name}_Top3'], bottom3[f'{name}_Bottom3']], axis=1)

# 保存极值表格
extreme_values.to_csv('moran_extreme_values.csv', index=False)
