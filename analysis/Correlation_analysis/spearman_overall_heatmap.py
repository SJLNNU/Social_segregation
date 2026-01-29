"""
Spearman correlation heatmap for all 30 cities (no grouping).
Reads SSI data, computes pairwise Spearman correlations, and saves a single heatmap.
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
sys.path.append(project_root)

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from data_process.data_reader import data_reader


def calculate_correlations(data):
    """Compute Spearman correlation matrix and p-values."""
    variables = list(data.columns)
    n = len(variables)
    correlation_matrix = np.zeros((n, n))
    p_values = np.zeros((n, n))

    for i, var1 in enumerate(variables):
        for j, var2 in enumerate(variables):
            corr, p_value = stats.spearmanr(data[var1], data[var2])
            correlation_matrix[i, j] = corr
            p_values[i, j] = p_value

    return correlation_matrix, p_values


def create_correlation_heatmap(correlation_matrix, p_values, variables, save_path, dpi=300):
    """Draw and save correlation heatmap (lower triangle, significance stars)."""
    significance_mask = np.zeros_like(p_values, dtype=str)
    significance_mask[p_values < 0.001] = '***'
    significance_mask[(p_values >= 0.001) & (p_values < 0.01)] = '**'
    significance_mask[(p_values >= 0.01) & (p_values < 0.05)] = '*'
    significance_mask[p_values >= 0.05] = ''

    mask = np.zeros_like(correlation_matrix, dtype=bool)
    mask[np.triu_indices_from(mask, k=0)] = True

    plt.figure(figsize=(8, 6))
    plt.rcParams['font.family'] = 'Calibri'
    plt.rcParams['font.size'] = 10

    heatmap = sns.heatmap(
        correlation_matrix,
        mask=mask,
        annot=True,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        center=0,
        square=True,
        fmt='.2f',
        annot_kws={'size': 10, 'weight': 'bold'},
        xticklabels=variables,
        yticklabels=variables,
        linewidths=0.5,
        cbar_kws={'label': ''},
    )

    for _, spine in heatmap.spines.items():
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_color('black')

    plt.xticks(rotation=0)
    plt.yticks(rotation=0)

    texts = heatmap.texts
    text_idx = 0
    for i in range(len(variables)):
        for j in range(len(variables)):
            if not mask[i, j]:
                value = correlation_matrix[i, j]
                if text_idx < len(texts):
                    text = texts[text_idx]
                    if significance_mask[i, j]:
                        text.set_text(f'{value:.2f}{significance_mask[i, j]}')
                        text.set_color('black')
                    else:
                        text.set_text(f'{value:.2f}')
                        text.set_color('gray')
                    text_idx += 1

    cbar = heatmap.collections[0].colorbar
    cbar.set_ticks([-1, -0.5, 0, 0.5, 1])
    cbar.set_ticklabels(['-1.0', '-0.5', '0', '0.5', '1.0'])

    plt.xlabel('Different Dimensions', fontsize=10)
    plt.ylabel('Different Dimensions', fontsize=10)
    plt.tight_layout()
    plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    plt.close()


def run_overall_spearman_heatmap(project_root=None, save_dir=None, dpi=300):
    """
    Run Spearman correlation analysis on all 30 cities and save one heatmap.

    Parameters
    ----------
    project_root : str, optional
        Project root path. If None, inferred from script location.
    save_dir : str, optional
        Directory to save the heatmap. If None, uses results_Quartile/spearman_overall.
    dpi : int
        Figure DPI for saved image (default 300).
    """
    if project_root is None:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    file_path = os.path.join(project_root, "data", "SSI_golbal_data.csv")
    city_list = data_reader(file_path, 4, classification_strategy='quartiles_4')

    df = pd.DataFrame({
        'SES': [c.theme1 for c in city_list],
        'HCD': [c.theme2 for c in city_list],
        'MSL': [c.theme3 for c in city_list],
        'HT': [c.theme4 for c in city_list],
        'Comp.': [c.themes for c in city_list],
    })

    variables = ['SES', 'HCD', 'MSL', 'HT', 'Comp.']
    corr_matrix, p_values = calculate_correlations(df)

    if save_dir is None:
        save_dir = os.path.join(project_root, "results_Quartile", "spearman_overall")
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, "overall_correlation_all30.png")
    create_correlation_heatmap(corr_matrix, p_values, variables, save_path, dpi=dpi)
    print(f"Heatmap saved: {save_path}")
    return save_path


if __name__ == "__main__":
    run_overall_spearman_heatmap(
        project_root=r"D:\Code\Social_segregation",
        dpi=300,
    )
