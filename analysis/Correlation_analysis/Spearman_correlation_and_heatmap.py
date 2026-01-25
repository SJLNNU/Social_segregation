import sys
import os
import matplotlib.colors as mcolors

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
sys.path.append(project_root)

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from data_process.data_reader import data_reader

def create_custom_colormap():
    """Create a custom colormap that matches the reference image"""
    # Define colors for the custom colormap
    colors = ['#000099', '#9999FF', '#FFFFFF', '#FFB2B2', '#FF0000']  # Adjusted blue and pink shades
    # Create custom colormap
    n_bins = 256
    positions = [0, 0.25, 0.5, 0.75, 1]
    return mcolors.LinearSegmentedColormap.from_list('custom_diverging', 
                                                    list(zip(positions, colors)), 
                                                    N=n_bins)

def create_correlation_heatmap(correlation_matrix, p_values, variables, title, save_path):
    """Helper function to create and save correlation heatmap"""
    # Create a mask for p-values
    significance_mask = np.zeros_like(p_values, dtype=str)
    significance_mask[p_values < 0.001] = '***'
    significance_mask[p_values >= 0.001] = '**'
    significance_mask[p_values >= 0.01] = '*'
    significance_mask[p_values >= 0.05] = ''

    # Create mask for upper triangle and diagonal
    mask = np.zeros_like(correlation_matrix, dtype=bool)
    mask[np.triu_indices_from(mask, k=0)] = True  # Include diagonal (k=0 instead of k=1)

    # Create the heatmap
    plt.figure(figsize=(8, 6))
    plt.rcParams['font.family'] = 'Calibri'
    plt.rcParams['font.size'] = 10

    # Create heatmap using coolwarm colormap
    heatmap = sns.heatmap(correlation_matrix,
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
                         cbar_kws={'label': ''})

    # Add black border to the heatmap
    for _, spine in heatmap.spines.items():
        spine.set_visible(True)
        spine.set_linewidth(2)
        spine.set_color('black')

    # Customize the appearance
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    
    # Get all text elements
    texts = heatmap.texts
    text_idx = 0
    
    # Add significance stars and adjust text color
    for i in range(len(variables)):
        for j in range(len(variables)):
            if not mask[i, j]:  # Only process visible cells
                value = correlation_matrix[i, j]
                
                # Format the text with significance stars
                if text_idx < len(texts):
                    text = texts[text_idx]
                    if significance_mask[i, j]:  # Significant correlations (with stars)
                        text.set_text(f'{value:.2f}{significance_mask[i, j]}')
                        text.set_color('black')  # Set significant correlations to black
                    else:  # Non-significant correlations
                        text.set_text(f'{value:.2f}')
                        text.set_color('gray')  # Set non-significant correlations to gray
                    text_idx += 1

    # Add colorbar
    cbar = heatmap.collections[0].colorbar
    cbar.set_ticks([-1, -0.5, 0, 0.5, 1])
    cbar.set_ticklabels(['-1.0', '-0.5', '0', '0.5', '1.0'])
    
    # Add labels
    plt.xlabel('Different Dimensions', fontsize=10)
    plt.ylabel('Different Dimensions', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')  # Reduced DPI for individual plots
    plt.close()

def calculate_correlations(data):
    """Calculate correlation matrix and p-values for given data"""
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

def create_combined_heatmap(correlation_matrices, p_values_list, variables, titles, save_path):
    """Create a combined heatmap with subplots sharing one colorbar (supports 2, 3, 4, or 5 subplots)"""
    n_subplots = len(correlation_matrices)
    
    # Create figure with size adjusted for number of subplots
    if n_subplots == 2:
        fig = plt.figure(figsize=(16, 8), facecolor='white')
        # Create GridSpec with wider spacing between subplots
        gs = plt.GridSpec(1, 2, width_ratios=[1, 1], wspace=0.2)
        axes = [plt.subplot(gs[0]), plt.subplot(gs[1])]
    elif n_subplots == 3:
        fig = plt.figure(figsize=(24, 8), facecolor='white')
        # Create GridSpec with wider spacing between subplots
        gs = plt.GridSpec(1, 3, width_ratios=[1, 1, 1], wspace=0.2)
        axes = [plt.subplot(gs[0]), plt.subplot(gs[1]), plt.subplot(gs[2])]
    elif n_subplots == 4:
        fig = plt.figure(figsize=(32, 8), facecolor='white')
        # Create GridSpec with wider spacing between subplots
        gs = plt.GridSpec(1, 4, width_ratios=[1, 1, 1, 1], wspace=0.2)
        axes = [plt.subplot(gs[0]), plt.subplot(gs[1]), plt.subplot(gs[2]), plt.subplot(gs[3])]
    elif n_subplots == 5:
        fig = plt.figure(figsize=(40, 8), facecolor='white')
        # Create GridSpec with wider spacing between subplots
        gs = plt.GridSpec(1, 5, width_ratios=[1, 1, 1, 1, 1], wspace=0.15)
        axes = [plt.subplot(gs[0]), plt.subplot(gs[1]), plt.subplot(gs[2]), plt.subplot(gs[3]), plt.subplot(gs[4])]
    else:
        raise ValueError(f"Unsupported number of subplots: {n_subplots}. Supported: 2, 3, 4, or 5")
    
    plt.rcParams['font.family'] = 'Calibri'
    plt.rcParams['font.size'] = 20  # Further increased base font size
    
    # Create a single colorbar for all subplots (adjust position based on number of subplots)
    if n_subplots == 2:
        cbar_ax = fig.add_axes([0.91, 0.15, 0.02, 0.7])
    elif n_subplots == 3:
        cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    elif n_subplots == 4:
        cbar_ax = fig.add_axes([0.93, 0.15, 0.02, 0.7])
    else:  # n_subplots == 5
        cbar_ax = fig.add_axes([0.94, 0.15, 0.02, 0.7])
    
    for idx, (ax, corr_matrix, p_values, title) in enumerate(zip(axes, correlation_matrices, p_values_list, titles)):
        # Create significance mask
        significance_mask = np.zeros_like(p_values, dtype=str)
        significance_mask[p_values < 0.001] = '***'
        significance_mask[p_values >= 0.001] = '**'
        significance_mask[p_values >= 0.01] = '*'
        significance_mask[p_values >= 0.05] = ''
        
        # Create mask for upper triangle and diagonal
        mask = np.zeros_like(corr_matrix, dtype=bool)
        mask[np.triu_indices_from(mask, k=0)] = True
        
        # Create heatmap with larger annotation size
        heatmap = sns.heatmap(corr_matrix,
                            mask=mask,
                            annot=True,
                            cmap="coolwarm",
                            vmin=-1,
                            vmax=1,
                            center=0,
                            square=True,
                            fmt='.2f',
                            annot_kws={'size': 20, 'weight': 'bold'},  # Further increased annotation size
                            xticklabels=variables,
                            yticklabels=variables,
                            linewidths=0.5,
                            cbar=idx == n_subplots - 1,  # Only show colorbar for the last subplot
                            cbar_ax=cbar_ax if idx == n_subplots - 1 else None,
                            ax=ax)
        
        # Add border to each subplot
        for spine in ax.spines.values():
            spine.set_linewidth(2)
            spine.set_color('black')
            spine.set_visible(True)
        
        # Customize text colors and add significance stars
        texts = heatmap.texts
        text_idx = 0
        for i in range(len(variables)):
            for j in range(len(variables)):
                if not mask[i, j]:
                    value = corr_matrix[i, j]
                    if text_idx < len(texts):
                        text = texts[text_idx]
                        if significance_mask[i, j]:
                            text.set_text(f'{value:.2f}{significance_mask[i, j]}')
                            text.set_color('black')
                        else:
                            text.set_text(f'{value:.2f}')
                            text.set_color('gray')
                        text_idx += 1
        
        ax.set_title(title, pad=20, fontsize=22, fontweight='bold')  # Further increased title size
        ax.tick_params(axis='both', which='major', labelsize=20)  # Further increased tick label size
        
        # Only show ylabel for the leftmost subplot
        if idx == 0:
            ax.set_ylabel('Different Dimensions', fontsize=22)  # Further increased label size
        else:
            ax.set_ylabel('')
        
        # Only show xlabel for the middle subplot or last subplot
        if n_subplots == 2 and idx == 1:
            ax.set_xlabel('Different Dimensions', fontsize=22)  # Further increased label size
        elif n_subplots == 3 and idx == 1:  # Middle subplot
            ax.set_xlabel('Different Dimensions', fontsize=22)  # Further increased label size
        elif n_subplots == 4 and idx == 2:  # Third subplot (middle of 4)
            ax.set_xlabel('Different Dimensions', fontsize=22)  # Further increased label size
        elif n_subplots == 5 and idx == 2:  # Third subplot (middle of 5)
            ax.set_xlabel('Different Dimensions', fontsize=22)  # Further increased label size
        else:
            ax.set_xlabel('')
    
    # Customize the colorbar
    cbar = heatmap.collections[0].colorbar
    cbar.set_ticks([-1, -0.5, 0, 0.5, 1])
    cbar.set_ticklabels(['-1.0', '-0.5', '0', '0.5', '1.0'])
    cbar.ax.tick_params(labelsize=20)  # Further increased colorbar label size
    
    # Add border to colorbar
    for spine in cbar_ax.spines.values():
        spine.set_linewidth(2)
        spine.set_color('black')
        spine.set_visible(True)
    
    # Adjust layout based on number of subplots using subplots_adjust instead of tight_layout
    # This avoids conflicts with manually created colorbar axes
    if n_subplots == 2:
        plt.subplots_adjust(left=0.08, right=0.88, top=0.95, bottom=0.1, wspace=0.2)
    elif n_subplots == 3:
        plt.subplots_adjust(left=0.05, right=0.9, top=0.95, bottom=0.1, wspace=0.2)
    elif n_subplots == 4:
        plt.subplots_adjust(left=0.04, right=0.91, top=0.95, bottom=0.1, wspace=0.2)
    else:  # n_subplots == 5
        plt.subplots_adjust(left=0.03, right=0.92, top=0.95, bottom=0.1, wspace=0.15)
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def spearman_correlation_analysis():
    """三分类相关性分析（Low, Medium, High）"""
    # Read data using the existing data_reader function
    file_path = os.path.join(project_root, "data", "SSI_golbal_data.csv")
    city_list = data_reader(file_path, 3, classification_strategy='tertiles')
    
    # Create results directory if it doesn't exist
    results_dir = os.path.join(project_root, "results_Quartile", "correlation_analysis")
    os.makedirs(results_dir, exist_ok=True)
    
    # Prepare data for all cities
    data = {
        'SES': [city.theme1 for city in city_list],
        'HCD': [city.theme2 for city in city_list],
        'MSL': [city.theme3 for city in city_list],
        'HT': [city.theme4 for city in city_list],
        'Comp.': [city.themes for city in city_list]
    }
    df = pd.DataFrame(data)
    
    # Variables to use in correlation analysis
    variables = ['SES', 'HCD', 'MSL', 'HT', 'Comp.']
    
    # Overall correlation analysis
    corr_matrix, p_values = calculate_correlations(df)
    create_correlation_heatmap(
        corr_matrix, p_values, variables,
        "",  # Empty title as requested
        os.path.join(results_dir, 'overall_correlation.png')
    )
    
    # Separate cities by segregation level
    segregation_levels = {
        'Low': [city for city in city_list if city.init_class == 0],
        'Medium': [city for city in city_list if city.init_class == 1],
        'High': [city for city in city_list if city.init_class == 2]
    }
    
    # Create individual heatmaps for each segregation level
    for level, cities in segregation_levels.items():
        if not cities:  # Skip if no cities in this category
            continue
            
        level_data = {
            'SES': [city.theme1 for city in cities],
            'HCD': [city.theme2 for city in cities],
            'MSL': [city.theme3 for city in cities],
            'HT': [city.theme4 for city in cities],
            'Comp.': [city.themes for city in cities]
        }
        df_level = pd.DataFrame(level_data)
        
        corr_matrix, p_values = calculate_correlations(df_level)
        create_correlation_heatmap(
            corr_matrix, p_values, variables,
            "",  # Empty title as requested
            os.path.join(results_dir, f'{level.lower()}_segregation_correlation.png')
        )
    
    # Prepare data for combined heatmap
    correlation_matrices = []
    p_values_list = []
    titles = []
    
    for level, cities in segregation_levels.items():
        if not cities:  # Skip if no cities in this category
            continue
            
        level_data = {
            'SES': [city.theme1 for city in cities],
            'HCD': [city.theme2 for city in cities],
            'MSL': [city.theme3 for city in cities],
            'HT': [city.theme4 for city in cities],
            'Comp.': [city.themes for city in cities]
        }
        df_level = pd.DataFrame(level_data)
        
        corr_matrix, p_values = calculate_correlations(df_level)
        correlation_matrices.append(corr_matrix)
        p_values_list.append(p_values)
        titles.append(f"{level} Segregation (n={len(cities)})")
    
    # Create combined heatmap
    create_combined_heatmap(
        correlation_matrices,
        p_values_list,
        variables,
        titles,
        os.path.join(results_dir, 'combined_segregation_correlation.png')
    )

def spearman_correlation_analysis_binary():
    """二分类相关性分析（Low, High）"""
    # Read data using the existing data_reader function with binary classification
    file_path = os.path.join(project_root, "data", "SSI_golbal_data.csv")
    city_list = data_reader(file_path, 2, classification_strategy='median')
    
    # Create results directory if it doesn't exist
    results_dir = os.path.join(project_root, "results_Quartile", "correlation_analysis_binary")
    os.makedirs(results_dir, exist_ok=True)
    
    # Prepare data for all cities
    data = {
        'SES': [city.theme1 for city in city_list],
        'HCD': [city.theme2 for city in city_list],
        'MSL': [city.theme3 for city in city_list],
        'H&T': [city.theme4 for city in city_list],
        'Comp.': [city.themes for city in city_list]
    }
    df = pd.DataFrame(data)
    
    # Variables to use in correlation analysis
    variables = ['SES', 'HCD', 'MSL', 'HT', 'Comp.']
    
    # Overall correlation analysis
    corr_matrix, p_values = calculate_correlations(df)
    create_correlation_heatmap(
        corr_matrix, p_values, variables,
        "",  # Empty title as requested
        os.path.join(results_dir, 'overall_correlation.png')
    )
    
    # Separate cities by segregation level (binary: Low and High)
    segregation_levels = {
        'Low': [city for city in city_list if city.init_class == 0],
        'High': [city for city in city_list if city.init_class == 1]
    }
    
    # Create individual heatmaps for each segregation level
    for level, cities in segregation_levels.items():
        if not cities:  # Skip if no cities in this category
            continue
            
        level_data = {
            'SES': [city.theme1 for city in cities],
            'HCD': [city.theme2 for city in cities],
            'MSL': [city.theme3 for city in cities],
            'H&T': [city.theme4 for city in cities],
            'Comp.': [city.themes for city in cities]
        }
        df_level = pd.DataFrame(level_data)
        
        corr_matrix, p_values = calculate_correlations(df_level)
        create_correlation_heatmap(
            corr_matrix, p_values, variables,
            "",  # Empty title as requested
            os.path.join(results_dir, f'{level.lower()}_segregation_correlation.png')
        )
    
    # Prepare data for combined heatmap
    correlation_matrices = []
    p_values_list = []
    titles = []
    
    for level, cities in segregation_levels.items():
        if not cities:  # Skip if no cities in this category
            continue
            
        level_data = {
            'SES': [city.theme1 for city in cities],
            'HCD': [city.theme2 for city in cities],
            'MSL': [city.theme3 for city in cities],
            'H&T': [city.theme4 for city in cities],
            'Comp.': [city.themes for city in cities]
        }
        df_level = pd.DataFrame(level_data)
        
        corr_matrix, p_values = calculate_correlations(df_level)
        correlation_matrices.append(corr_matrix)
        p_values_list.append(p_values)
        titles.append(f"{level} Segregation (n={len(cities)})")
    
    # Create combined heatmap
    create_combined_heatmap(
        correlation_matrices,
        p_values_list,
        variables,
        titles,
        os.path.join(results_dir, 'combined_segregation_correlation.png')
    )

def spearman_correlation_analysis_quartiles_4():
    """四分类相关性分析（Low, Medium-Low, Medium-High, High）"""
    # Read data using the existing data_reader function with quartiles_4 classification
    file_path = os.path.join(project_root, "data", "SSI_golbal_data.csv")
    city_list = data_reader(file_path, 4, classification_strategy='quartiles_4')
    
    # Create results directory if it doesn't exist
    results_dir = os.path.join(project_root, "results_Quartile", "correlation_analysis_quartiles_4")
    os.makedirs(results_dir, exist_ok=True)
    
    # Prepare data for all cities
    data = {
        'SES': [city.theme1 for city in city_list],
        'HCD': [city.theme2 for city in city_list],
        'MSL': [city.theme3 for city in city_list],
        'H&T': [city.theme4 for city in city_list],
        'Comp.': [city.themes for city in city_list]
    }
    df = pd.DataFrame(data)
    
    # Variables to use in correlation analysis
    variables = ['SES', 'HCD', 'MSL', 'HT', 'Comp.']
    
    # Overall correlation analysis
    corr_matrix, p_values = calculate_correlations(df)
    create_correlation_heatmap(
        corr_matrix, p_values, variables,
        "",  # Empty title as requested
        os.path.join(results_dir, 'overall_correlation.png')
    )
    
    # Separate cities by segregation level (4 classes)
    segregation_levels = {
        'Low': [city for city in city_list if city.init_class == 0],
        'Medium-Low': [city for city in city_list if city.init_class == 1],
        'Medium-High': [city for city in city_list if city.init_class == 2],
        'High': [city for city in city_list if city.init_class == 3]
    }
    
    # Create individual heatmaps for each segregation level
    for level, cities in segregation_levels.items():
        if not cities:  # Skip if no cities in this category
            continue
            
        level_data = {
            'SES': [city.theme1 for city in cities],
            'HCD': [city.theme2 for city in cities],
            'MSL': [city.theme3 for city in cities],
            'H&T': [city.theme4 for city in cities],
            'Comp.': [city.themes for city in cities]
        }
        df_level = pd.DataFrame(level_data)
        
        corr_matrix, p_values = calculate_correlations(df_level)
        create_correlation_heatmap(
            corr_matrix, p_values, variables,
            "",  # Empty title as requested
            os.path.join(results_dir, f'{level.lower().replace("-", "_")}_segregation_correlation.png')
        )
    
    # Prepare data for combined heatmap
    correlation_matrices = []
    p_values_list = []
    titles = []
    
    for level, cities in segregation_levels.items():
        if not cities:  # Skip if no cities in this category
            continue
            
        level_data = {
            'SES': [city.theme1 for city in cities],
            'HCD': [city.theme2 for city in cities],
            'MSL': [city.theme3 for city in cities],
            'HT': [city.theme4 for city in cities],
            'Comp.': [city.themes for city in cities]
        }
        df_level = pd.DataFrame(level_data)
        
        corr_matrix, p_values = calculate_correlations(df_level)
        correlation_matrices.append(corr_matrix)
        p_values_list.append(p_values)
        titles.append(f"{level} Segregation (n={len(cities)})")
    
    # Create combined heatmap
    create_combined_heatmap(
        correlation_matrices,
        p_values_list,
        variables,
        titles,
        os.path.join(results_dir, 'combined_segregation_correlation.png')
    )

def spearman_correlation_analysis_jenks(n_classes=3):
    """
    Jenks natural breaks 相关性分析
    
    Parameters:
    -----------
    n_classes : int
        分类数量，支持 2, 3, 4, 5 (默认: 3)
    """
    if n_classes not in [2, 3, 4, 5]:
        raise ValueError(f"n_classes must be 2, 3, 4, or 5, got {n_classes}")
    
    # 定义不同分类数对应的类别名称
    class_names_map = {
        2: ['Low', 'High'],
        3: ['Low', 'Medium', 'High'],
        4: ['Low', 'Medium-Low', 'Medium-High', 'High'],
        5: ['Low', 'Medium-Low', 'Medium', 'Medium-High', 'High']
    }
    
    # Read data using the existing data_reader function with Jenks natural breaks
    file_path = os.path.join(project_root, "data", "SSI_golbal_data.csv")
    city_list = data_reader(file_path, n_classes, classification_strategy='jenks')
    
    # Create results directory if it doesn't exist (包含分类数)
    results_dir = os.path.join(project_root, "results_Quartile", f"correlation_analysis_jenks_{n_classes}classes")
    os.makedirs(results_dir, exist_ok=True)
    
    # Prepare data for all cities
    data = {
        'SES': [city.theme1 for city in city_list],
        'HCD': [city.theme2 for city in city_list],
        'MSL': [city.theme3 for city in city_list],
        'HT': [city.theme4 for city in city_list],
        'Comp.': [city.themes for city in city_list]
    }
    df = pd.DataFrame(data)
    
    # Variables to use in correlation analysis
    variables = ['SES', 'HCD', 'MSL', 'HT', 'Comp.']
    
    # Overall correlation analysis
    corr_matrix, p_values = calculate_correlations(df)
    create_correlation_heatmap(
        corr_matrix, p_values, variables,
        "",  # Empty title as requested
        os.path.join(results_dir, 'overall_correlation.png')
    )
    
    # Separate cities by segregation level (Jenks classes)
    # 确定实际使用的类别数（可能少于指定的类别数）
    unique_classes = sorted(set(city.init_class for city in city_list))
    actual_n_classes = len(unique_classes)
    
    segregation_levels = {}
    class_names = class_names_map[n_classes]
    for i, class_id in enumerate(unique_classes):
        level_name = class_names[i] if i < len(class_names) else f'Class {i+1}'
        segregation_levels[level_name] = [city for city in city_list if city.init_class == class_id]
    
    # Create individual heatmaps for each segregation level
    for level, cities in segregation_levels.items():
        if not cities:  # Skip if no cities in this category
            continue
            
        level_data = {
            'SES': [city.theme1 for city in cities],
            'HCD': [city.theme2 for city in cities],
            'MSL': [city.theme3 for city in cities],
            'HT': [city.theme4 for city in cities],
            'Comp.': [city.themes for city in cities]
        }
        df_level = pd.DataFrame(level_data)
        
        corr_matrix, p_values = calculate_correlations(df_level)
        create_correlation_heatmap(
            corr_matrix, p_values, variables,
            "",  # Empty title as requested
            os.path.join(results_dir, f'{level.lower().replace("-", "_")}_segregation_correlation.png')
        )
    
    # Prepare data for combined heatmap
    correlation_matrices = []
    p_values_list = []
    titles = []
    
    for level, cities in segregation_levels.items():
        if not cities:  # Skip if no cities in this category
            continue
            
        level_data = {
            'SES': [city.theme1 for city in cities],
            'HCD': [city.theme2 for city in cities],
            'MSL': [city.theme3 for city in cities],
            'HT': [city.theme4 for city in cities],
            'Comp.': [city.themes for city in cities]
        }
        df_level = pd.DataFrame(level_data)
        
        corr_matrix, p_values = calculate_correlations(df_level)
        correlation_matrices.append(corr_matrix)
        p_values_list.append(p_values)
        titles.append(f"{level} Segregation (n={len(cities)})")
    
    # Create combined heatmap
    create_combined_heatmap(
        correlation_matrices,
        p_values_list,
        variables,
        titles,
        os.path.join(results_dir, 'combined_segregation_correlation.png')
    )

if __name__ == '__main__':
    # 可以选择运行不同的分类分析
    # 三分类分析（Low, Medium, High）
    #spearman_correlation_analysis()
    
    # 二分类分析（Low, High）
    #spearman_correlation_analysis_binary()
    
    # 四分类分析（Low, Medium-Low, Medium-High, High）
    #spearman_correlation_analysis_quartiles_4()
    
    # Jenks natural breaks 分析（支持 2, 3, 4, 5 类）
    # 可以选择运行不同分类数的分析
    for n in [2, 3, 4, 5]:
        spearman_correlation_analysis_jenks(n_classes=n)
