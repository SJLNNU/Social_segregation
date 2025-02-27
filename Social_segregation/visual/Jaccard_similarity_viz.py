import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define themes and confidence levels
themes = ["theme1", "theme2", "theme3", "theme4", "themes"]
confidence_levels = ["90%", "95%", "99%"]
types = ["Hotspot", "Coldspot"]  # Two categories

# Base directory where the files are stored
base_dir = r"D:/Code/Social_segregation/data/Jaccard_similarity/"

# Initialize dictionary to store data
similarity_data = {level: {t: pd.DataFrame(index=themes, columns=themes) for t in types} for level in confidence_levels}

# Iterate over theme combinations
for theme_x in themes:
    for theme_y in themes:
        if theme_x != theme_y:
            file_path = os.path.join(base_dir, theme_x, f"Jaccard_Similarity_{theme_x}-{theme_y}.csv")

            if os.path.exists(file_path):
                df = pd.read_csv(file_path)

                for level in confidence_levels:
                    for t in types:
                        col_name = f"{t}_{level}"
                        if col_name in df.columns:
                            similarity_data[level][t].loc[theme_x, theme_y] = df[col_name].mean()
                            similarity_data[level][t].loc[theme_y, theme_x] = df[col_name].mean()# Ensure symmetry

# Generate heatmaps
for level in confidence_levels:
    for t in types:
        plt.figure(figsize=(8, 6))
        sns.heatmap(similarity_data[level][t].astype(float), annot=True, cmap="coolwarm", linewidths=0.5)
        plt.title(f"Jaccard Similarity ({t}) at {level} Confidence Level")
        plt.xlabel("Themes")
        plt.ylabel("Themes")
        plt.show()
