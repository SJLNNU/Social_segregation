import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from itertools import combinations
from scipy import stats
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
sys.path.append(project_root)

from data_process.data_reader import data_reader
# -----------------------------
# 1) 将 city_list 转为 DataFrame
# -----------------------------
def cities_to_df(city_list):
    """
    Convert city_list to DataFrame with consistent column names.
    Assumes each city has attributes: theme1, theme2, theme3, theme4, themes.
    """
    df = pd.DataFrame({
        'SES':   [c.theme1 for c in city_list],
        'HCD':   [c.theme2 for c in city_list],
        'MSL':   [c.theme3 for c in city_list],
        'HT':    [c.theme4 for c in city_list],   # 统一用 HT，避免 H&T/HT 混用
        'Comp.': [c.themes for c in city_list]
    })
    return df


# -------------------------------------------------------
# 2) 单个窗口 Spearman + bootstrap CI（在窗口内部重采样）
# -------------------------------------------------------
def spearman_with_bootstrap_ci(x, y, n_boot=2000, ci=95, random_state=42):
    """
    Compute Spearman rho and bootstrap CI for rho.
    Bootstrap resamples paired (x,y) observations with replacement.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    n = len(x)
    if n < 3:
        return np.nan, (np.nan, np.nan)

    rho, _ = stats.spearmanr(x, y)

    rng = np.random.default_rng(random_state)
    boot = np.empty(n_boot, dtype=float)

    # paired bootstrap
    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        rb, _ = stats.spearmanr(x[idx], y[idx])
        boot[b] = rb

    alpha = (100 - ci) / 2
    lo = np.nanpercentile(boot, alpha)
    hi = np.nanpercentile(boot, 100 - alpha)
    return rho, (lo, hi)


# -------------------------------------------------------
# 3) Rolling-window Spearman：相关性随隔离程度 S 变化
# -------------------------------------------------------
def rolling_spearman(df, sort_by='Comp.', variables=None, window=15, step=1,
                     n_boot=2000, ci=95, random_state=42):
    """
    Rolling-window Spearman correlation curves with bootstrap CI.

    Parameters
    ----------
    df : DataFrame
        Must contain sort_by and all variables.
    sort_by : str
        Continuous segregation level variable, e.g., 'Comp.'.
    variables : list[str]
        Variables to analyze. If None, use ['SES','HCD','MSL','HT','Comp.'].
        Note: Usually you may NOT want to include sort_by itself in pairwise curves;
              you can exclude it when plotting if desired.
    window : int
        Window size, recommended 12-15 for n=30.
    step : int
        Step size for sliding.
    n_boot : int
        Bootstrap iterations per window.
    ci : int
        CI level (e.g., 95).
    """
    if variables is None:
        variables = ['SES', 'HCD', 'MSL', 'HT', 'Comp.']

    # Sort by segregation level
    df_sorted = df.sort_values(sort_by).reset_index(drop=True)

    n = len(df_sorted)
    if window > n:
        raise ValueError(f"window={window} is larger than n={n}")

    # Prepare results container
    pairs = list(combinations(variables, 2))
    results = {pair: {'S_center': [], 'rho': [], 'ci_low': [], 'ci_high': [], 'n': []}
               for pair in pairs}

    # Rolling
    for start in range(0, n - window + 1, step):
        end = start + window
        w = df_sorted.iloc[start:end]

        # x-axis: center S in this window (用中位数更稳健)
        S_center = float(np.mean(w[sort_by].values))

        for (a, b) in pairs:
            rho, (lo, hi) = spearman_with_bootstrap_ci(
                w[a].values, w[b].values,
                n_boot=n_boot, ci=ci, random_state=random_state
            )
            results[(a, b)]['S_center'].append(S_center)
            results[(a, b)]['rho'].append(rho)
            results[(a, b)]['ci_low'].append(lo)
            results[(a, b)]['ci_high'].append(hi)
            results[(a, b)]['n'].append(window)

    return results


# -------------------------------------------------------
# 4) 绘图：每对变量一张曲线（rho vs S_center + CI band）
# -------------------------------------------------------
def plot_rolling_curve(pair_result, pair_name, sort_by, out_path, ci_label='95% CI'):
    """
    Plot a single rolling correlation curve for one variable pair.
    """
    x = np.asarray(pair_result['S_center'], dtype=float)
    y = np.asarray(pair_result['rho'], dtype=float)
    lo = np.asarray(pair_result['ci_low'], dtype=float)
    hi = np.asarray(pair_result['ci_high'], dtype=float)

    # sort by x (just in case)
    order = np.argsort(x)
    x, y, lo, hi = x[order], y[order], lo[order], hi[order]

    plt.figure()
    plt.axhline(0, linewidth=1)
    plt.plot(x, y)
    plt.fill_between(x, lo, hi, alpha=0.2)
    plt.xlabel(f"Segregation level (sorted by {sort_by})")
    plt.ylabel("Spearman's rho")
    plt.title(pair_name)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()


# -------------------------------------------------------
# 4b) 统一可视化：热图式布局，每个单元格显示rolling曲线
# -------------------------------------------------------
def plot_all_rolling_curves(roll_results, sort_by, window, step, ci, out_path, variables=None):
    """
    Plot all rolling correlation curves in a heatmap-like layout (lower triangle only).
    Each cell shows a rolling correlation curve for a variable pair.
    
    Parameters
    ----------
    roll_results : dict
        Results from rolling_spearman, keyed by variable pairs (tuple).
    sort_by : str
        Variable used for sorting.
    window : int
        Window size.
    step : int
        Step size.
    ci : int
        Confidence interval level.
    out_path : str
        Output file path.
    variables : list
        List of variables in order. If None, inferred from roll_results.
    """
    # 获取变量列表
    if variables is None:
        all_vars = set()
        for pair in roll_results.keys():
            all_vars.add(pair[0])
            all_vars.add(pair[1])
        # 使用标准顺序
        standard_order = ['SES', 'HCD', 'MSL', 'HT', 'Comp.']
        variables = [v for v in standard_order if v in all_vars]
        # 添加任何不在标准顺序中的变量
        for v in sorted(all_vars):
            if v not in variables:
                variables.append(v)
    
    n_vars = len(variables)
    
    # 创建图形，只保留中间的子图矩阵部分
    fig = plt.figure(figsize=(n_vars * 3, n_vars * 3), facecolor='white')
    # 创建主网格，直接使用n_vars x n_vars，不留标签空间
    gs = plt.GridSpec(n_vars, n_vars, figure=fig, 
                     hspace=0.25, wspace=0.25,
                     left=0.05, right=0.95, top=0.95, bottom=0.05)
    
    plt.rcParams['font.family'] = 'Calibri'
    plt.rcParams['font.size'] = 20  # 放大字号
    
    # 计算全局y轴范围（用于统一y轴尺度）
    all_y = []
    for pair_result in roll_results.values():
        all_y.extend(pair_result['rho'])
    y_min, y_max = np.nanmin(all_y), np.nanmax(all_y)
    y_range = y_max - y_min
    y_margin = y_range * 0.1
    y_lim = (y_min - y_margin, y_max + y_margin)
    
    # 创建子图矩阵（只保留下三角）
    for i in range(n_vars):
        for j in range(n_vars):
            ax = fig.add_subplot(gs[i, j])  # 直接使用i, j，不再跳过标签行/列
            var_i = variables[i]
            var_j = variables[j]
            
            if j >= i:  # 上三角和对角线：空白
                ax.axis('off')
            else:  # 下三角：绘制曲线
                # 获取对应的pair（注意顺序可能不同）
                pair = None
                if (var_i, var_j) in roll_results:
                    pair = (var_i, var_j)
                elif (var_j, var_i) in roll_results:
                    pair = (var_j, var_i)
                
                if pair and pair in roll_results:
                    pair_result = roll_results[pair]
                    
                    x = np.asarray(pair_result['S_center'], dtype=float)
                    y = np.asarray(pair_result['rho'], dtype=float)
                    lo = np.asarray(pair_result['ci_low'], dtype=float)
                    hi = np.asarray(pair_result['ci_high'], dtype=float)
                    
                    # sort by x
                    order = np.argsort(x)
                    x, y, lo, hi = x[order], y[order], lo[order], hi[order]
                    
                    # 绘制零线（加粗）
                    ax.axhline(0, color='gray', linewidth=1.0, linestyle='--', alpha=0.5)
                    
                    # 根据显著性和符号确定颜色
                    # 如果置信区间不包含0，则显著；否则不显著
                    colors = []
                    edge_colors = []  # 边框颜色数组
                    linewidths = []  # 边框宽度数组
                    for rho_val, ci_low, ci_high in zip(y, lo, hi):
                        # 判断是否显著：置信区间不包含0
                        is_significant = (ci_low > 0) or (ci_high < 0)
                        
                        if not is_significant:
                            # 不显著：浅灰色，无边框
                            colors.append('#BFC6C4')  # 使用更浅的灰色 (lightgray)
                            edge_colors.append('#BFC6C4')  # 边框颜色与填充色相同（看起来无边框）
                            linewidths.append(0)  # 边框宽度为0
                        elif rho_val > 0:
                            # 显著且正相关：红色，有黑色边框
                            colors.append('red')
                            edge_colors.append('black')
                            linewidths.append(0.5)
                        else:
                            # 显著且负相关：蓝色，有黑色边框
                            colors.append('blue')
                            edge_colors.append('black')
                            linewidths.append(0.5)
                    
                    # 绘制散点图
                    ax.scatter(x, y, c=colors, s=30, alpha=0.7, edgecolors=edge_colors, linewidths=linewidths)
                    
                    # 设置y轴（统一范围）
                    ax.set_ylim(y_lim)
                    
                    # 设置刻度标签（增大字号）
                    ax.tick_params(labelsize=14)
                    
                    # X轴刻度：在底部显示（恢复到原来位置）
                    ax.tick_params(axis='x', labelsize=14, bottom=True, top=False, labelbottom=True, labeltop=False)
                    ax.xaxis.set_visible(True)
                    ax.set_xlabel('Mean Comp. SSI', fontsize=16, fontweight='bold')
                    
                    # Y轴刻度：在左侧显示（恢复到原来位置）
                    ax.tick_params(axis='y', labelsize=14, left=True, right=False, labelleft=True, labelright=False)
                    ax.yaxis.set_visible(True)
                    ax.set_ylabel("ρ", fontsize=16, fontweight='bold')
                    
                    # 调整spines：只显示底部和左侧（恢复到原来位置）
                    ax.spines['bottom'].set_visible(True)
                    ax.spines['left'].set_visible(True)
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    
                    # 取消子图内部的网格线
                    ax.grid(False)
                else:
                    # 如果没有找到对应的pair，显示空白
                    ax.axis('off')
    
    # 移除所有标签和标题，只保留中间的子图矩阵
    # 取消子图之间的固定网格线
    
    # 调整布局
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()


# -------------------------------------------------------
# 5) 总入口：读数据 → rolling → 批量输出图片
# -------------------------------------------------------
def spearman_correlation_analysis_rolling(project_root,
                                          window=15, step=1,
                                          sort_by='Comp.',
                                          variables=None,
                                          n_boot=2000, ci=95):
    """
    Rolling-window Spearman correlation analysis across continuous segregation level.
    Produces one curve per variable pair.

    Notes:
    - For n=30, recommended window: 12-15
    - Default variables include all dimensions: ['SES','HCD','MSL','HT','Comp.']
    - If you want to exclude Comp. from correlation pairs (since it's used for sorting),
      pass variables=['SES','HCD','MSL','HT'] explicitly.
    """
    file_path = os.path.join(project_root, "data", "SSI_golbal_data.csv")
    city_list = data_reader(file_path, 4, classification_strategy='quartiles_4')  # init_classes=4 here only for reader; not used further

    df = cities_to_df(city_list)

    if variables is None:
        # 默认包含所有变量，与 Spearman_correlation_and_heatmap.py 保持一致
        variables = ['SES', 'HCD', 'MSL', 'HT', 'Comp.']

    results_dir = os.path.join(project_root, "results_Quartile", "correlation_analysis_rolling_15")
    os.makedirs(results_dir, exist_ok=True)

    # Rolling results
    roll = rolling_spearman(
        df,
        sort_by=sort_by,
        variables=variables,
        window=window,
        step=step,
        n_boot=n_boot,
        ci=ci,
        random_state=42
    )

    # Save individual plots (optional, for detailed inspection)
    for (a, b), r in roll.items():
        pair_name = f"Rolling Spearman: {a} vs {b} (window={window}, step={step}, CI={ci}%)"
        fname = f"rolling_{a}_vs_{b}_by_{sort_by}_w{window}_s{step}.png".replace('.', '')
        out_path = os.path.join(results_dir, fname)
        plot_rolling_curve(r, pair_name, sort_by, out_path, ci_label=f"{ci}% CI")
    
    # Save combined visualization (all curves in one figure, heatmap-style layout)
    combined_fname = f"rolling_all_pairs_by_{sort_by}_w{window}_s{step}.png".replace('.', '')
    combined_out_path = os.path.join(results_dir, combined_fname)
    plot_all_rolling_curves(roll, sort_by, window, step, ci, combined_out_path, variables=variables)
    print(f"Combined visualization saved to: {combined_out_path}")

    return roll, results_dir


roll, out_dir = spearman_correlation_analysis_rolling(
    project_root=r"D:\Code\Social_segregation",
    window=15,     # n=30 时推荐 12-15
    step=1,        # step=1 曲线更平滑；step=2 更"粗"
    sort_by='Comp.',
    variables=['SES','HCD','MSL','HT','Comp.'],  # 包含所有变量，与 Spearman_correlation_and_heatmap.py 保持一致
    n_boot=2000,   # bootstrap 次数（可先 500 快速跑）
    ci=95
)
print(out_dir)