# 通过对比

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind_from_stats

# 读取数据
file_path = r"D:\data\social segregation\SSI\Data\Step2_SSI\trend_analysis_results.csv"
trend_df = pd.read_csv(file_path, encoding="latin1")

# Rename columns
trend_df.columns = ["File Name", "Variable", "Global Coefficient", "High Isolation Coefficient", "Change Magnitude",
                    "t Value", "p Value"]


# Compute Cohen's d effect size
def cohens_d(mean1, mean2, std1, std2):
    pooled_std = np.sqrt((std1 ** 2 + std2 ** 2) / 2)
    return (mean1 - mean2) / pooled_std


effect_sizes = []
coef_means = []

for var in ["SES", "HCD", "MSL", "HTT"]:
    subset = trend_df[trend_df["Variable"] == var]
    cohen_d_list = []
    global_coeff_list = []
    high_iso_coeff_list = []

    for _, row in subset.iterrows():
        d = cohens_d(row["Global Coefficient"], row["High Isolation Coefficient"], row["Global Coefficient"],
                     row["High Isolation Coefficient"])
        cohen_d_list.append(d)
        global_coeff_list.append(row["Global Coefficient"])
        high_iso_coeff_list.append(row["High Isolation Coefficient"])

    effect_sizes.append({
        "Variable": var,
        "Mean Cohen's d": np.mean(cohen_d_list),
        "Standard Deviation": np.std(cohen_d_list)
    })

    coef_means.append({
        "Variable": var,
        "Mean Global Coefficient": np.mean(global_coeff_list),
        "Mean High Isolation Coefficient": np.mean(high_iso_coeff_list)
    })

effect_df = pd.DataFrame(effect_sizes)
coef_df = pd.DataFrame(coef_means)

# Plot Cohen's d effect sizes
plt.figure(figsize=(10, 5))
sns.barplot(data=effect_df, x="Variable", y="Mean Cohen's d", palette="coolwarm", capsize=0.2)
plt.axhline(0.2, color='grey', linestyle="dashed", label="Small Effect")
plt.axhline(0.5, color='black', linestyle="dashed", label="Medium Effect")
plt.axhline(0.8, color='red', linestyle="dashed", label="Large Effect")
plt.legend()
plt.title("Cohen's d Effect Size Analysis (Global vs. High Isolation)")
plt.ylabel("Cohen's d")
plt.show()

# Compute p-value heatmap
p_matrix = trend_df.pivot(index="Variable", columns="File Name", values="p Value")

plt.figure(figsize=(12, 6))
sns.heatmap(p_matrix, annot=True, cmap="coolwarm", cbar=True, fmt=".2g")
plt.title("p-Value Heatmap for Theme1-4 in High Isolation")
plt.ylabel("Variable")
plt.xlabel("City")
plt.show()

# Plot coefficient change trends (Global vs. High Isolation)
plt.figure(figsize=(10, 5))
sns.boxplot(data=trend_df, x="Variable", y="Change Magnitude", palette="coolwarm")
plt.axhline(0, color="black", linestyle="dashed")
plt.title("Coefficient Changes for Theme1-4 in High Isolation")
plt.ylabel("Change Magnitude (High Isolation - Global)")
plt.xlabel("Variable")
plt.show()

# Plot absolute coefficient comparison
plt.figure(figsize=(10, 5))
sns.barplot(data=coef_df.melt(id_vars=["Variable"], var_name="Category", value_name="Coefficient"),
            x="Variable", y="Coefficient", hue="Category", palette="coolwarm")
plt.title("Comparison of Mean Coefficients (Global vs. High Isolation)")
plt.ylabel("Mean Coefficient Value")
plt.legend(title="Coefficient Type")
plt.show()


# Print results
def print_dataframe(df):
    print(df.to_string(index=False))


print("\nCohen's d Effect Analysis:")
print_dataframe(effect_df)

print("\nMean Coefficients Comparison:")
print_dataframe(coef_df)
