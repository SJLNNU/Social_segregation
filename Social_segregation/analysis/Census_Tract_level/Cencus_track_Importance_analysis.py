# 在Census Track Level 我们同样进行一次重要性分析，看一下结果

from data_process.data_reader import data_reader_census_tract

from analysis.importance_analysis.Importance_analysis import*
import os
import pandas as pd
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind_from_stats
from sklearn.linear_model import LinearRegression
from data_process.data_reader import data_reader_census_tract
from analysis.importance_analysis.Importance_analysis import relative_importance_analysis, relative_importance_analysis_with_selected_initclass


def plot_importance_comparison(trend_df, output_path):
    """ Visualize the comparison of variable importance and coefficient changes """
    fig, ax1 = plt.subplots(figsize=(12, 6))

    variables = trend_df["Variable"].unique()
    x = np.arange(len(variables))  # X positions
    width = 0.35  # Bar width

    global_importance = trend_df["Global Importance"].values
    high_iso_importance = trend_df["High Isolation Importance"].values
    coefficient_changes = trend_df["Change"].values  # Coefficient differences

    bars1 = ax1.bar(x - width / 2, global_importance, width, label="Global Importance", alpha=0.7)
    bars2 = ax1.bar(x + width / 2, high_iso_importance, width, label="High Isolation Importance", alpha=0.7)

    ax1.set_xlabel("Variable")
    ax1.set_ylabel("Importance")
    ax1.set_title("Global vs High Isolation Variable Importance and Coefficient Changes")
    ax1.set_xticks(x)
    ax1.set_xticklabels(variables, rotation=45)
    ax1.legend()

    # Second y-axis for coefficient changes
    ax2 = ax1.twinx()
    ax2.plot(x, coefficient_changes, color='red', marker='o', linestyle='dashed', label="Coefficient Change")
    ax2.set_ylabel("Coefficient Change")
    ax2.legend(loc='upper right')

    plt.tight_layout()

    plot_path = os.path.join(output_path, 'importance_coefficient_comparison.png')
    plt.savefig(plot_path)
    plt.show()
    print(f"✅ Importance and Coefficient Comparison plot saved to {plot_path}")


def analyze_all_csv_in_folder(folder_path):
    """ Process all CSV files in the folder, compute variable importance, and analyze trends """
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    all_results = []

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        print(f"📂 Processing file: {file_path}")

        # Read data
        census_track_list = data_reader_census_tract(file_path)

        # Compute global variable importance
        global_results = relative_importance_analysis(census_track_list)

        # Compute high isolation area (init_class=2) variable importance
        high_iso_results = relative_importance_analysis_with_selected_initclass(census_track_list, 2)
        if global_results is None or high_iso_results is None:
            continue
        if high_iso_results is not None and isinstance(high_iso_results, dict):
            # Compute variable trends (compare global and high isolation importance changes)
            trend_results = []
            for var in global_results.keys():
                global_importance = global_results[var]
                high_importance = high_iso_results.get(var, None)

                if high_importance is not None:
                    change = high_importance - global_importance

                    # Compute standard errors (assuming equal sample size for simplicity)
                    global_se = np.std(list(global_results.values())) / np.sqrt(len(global_results))
                    high_se = np.std(list(high_iso_results.values())) / np.sqrt(len(high_iso_results))

                    # t-test
                    t_stat, p_value = ttest_ind_from_stats(mean1=global_importance, std1=global_se,
                                                           nobs1=len(global_results),
                                                           mean2=high_importance, std2=high_se,
                                                           nobs2=len(high_iso_results))

                    trend_results.append({
                        "Filename": file,
                        "Variable": var,
                        "Global Importance": global_importance,
                        "High Isolation Importance": high_importance,
                        "Change": change,
                        "t-value": t_stat,
                        "p-value": p_value
                    })

            all_results.extend(trend_results)

    # Aggregate results
    trend_df = pd.DataFrame(all_results)
    print("\n📊 **Final Analysis Results:**")
    print(trend_df)

    # Save results
    output_path = folder_path
    trend_df.to_csv(os.path.join(output_path, 'trend_analysis_results.csv'), index=False)
    print(f"✅ Results saved to {output_path}")

    # Generate visualization
    plot_importance_comparison(trend_df, output_path)

    return trend_df
if __name__ == '__main__':
    # Census_tract_file_path=r'D:\data\social segregation\SSI\Data\Step2_SSI\Austin_LocalSSI.csv'
    #
    # cencus_track_list=data_reader_census_tract(Census_tract_file_path)
    # relative_importance_analysis(cencus_track_list)
    #
    # relative_importance_analysis_with_selected_initclass(cencus_track_list,2)
    folder_path = r'D:\data\social segregation\SSI\Data\Step2_SSI'
    analyze_all_csv_in_folder(folder_path)