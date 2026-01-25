# Social Segregation Analysis

This repository contains the code for the paper **"A Mobility-Based Framework for Measuring Socio-Spatial Segregation in 30 U.S. Metropolitan Areas."**

## Overview

This project provides a comprehensive framework for analyzing socio-spatial segregation patterns across 30 U.S. metropolitan areas using mobility-based measurements. The analysis includes multiple dimensions of segregation (SES, HCD, MSL, HT) and employs various spatial statistical methods.

## Project Structure

```
Social_segregation/
├── analysis/              # Analysis modules
│   ├── Moran/            # Moran's I spatial autocorrelation analysis
│   ├── Getis-Ord/        # Getis-Ord hotspot analysis (OHSA)
│   ├── cluster_analysis/  # Clustering methods (K-means, Spectral, Decision Tree)
│   ├── Correlation_analysis/  # Spearman correlation analysis
│   ├── importance_analysis/  # Feature importance analysis
│   └── Census_Tract_level/   # Census tract level analysis (GWR, Hot/Cold spots)
├── data_process/         # Data processing utilities
│   ├── data_reader.py    # Data reading functions
│   └── data_struct.py    # Data structure definitions
└── visual/              # Visualization scripts
    ├── MSA_SSI_violin.py      # Violin plots for SSI distribution
    ├── Moran_scatter_visual.py # Moran scatter plots
    ├── Jaccard_similarity_viz.py # Jaccard similarity visualization
    └── Four_D_visual.py        # Multi-dimensional visualization
```

## Main Features

### 1. Spatial Analysis
- **Moran's I**: Spatial autocorrelation analysis for segregation patterns
- **Getis-Ord (OHSA)**: Optimized hotspot analysis to identify spatial clusters
- **Geographically Weighted Regression (GWR)**: Local regression analysis

### 2. Clustering Analysis
- K-means clustering
- Spectral clustering
- Hierarchical clustering
- Decision tree-based classification

### 3. Statistical Analysis
- Spearman correlation analysis
- Feature importance analysis (SHAP, relative importance)
- Hot/Cold spot identification

### 4. Visualization
- Violin plots for SSI distribution across themes
- Moran scatter plots
- Jaccard similarity heatmaps
- Multi-dimensional visualizations

## Data Description

The project analyzes four main themes of social segregation:
- **Theme1 (SES)**: Socioeconomic Status
- **Theme2 (HCD)**: Housing and Community Development
- **Theme3 (MSL)**: Mobility and Spatial Location
- **Theme4 (HT)**: Housing Type
- **Themes (Comp.)**: Composite/Overall segregation index

Data covers 30 U.S. metropolitan areas at the census tract level.

## Requirements

### Python Packages
- `pandas`
- `numpy`
- `geopandas`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `libpysal`
- `esda`
- `mgwr` (for GWR analysis)
- `shap` (for SHAP importance analysis)

### Installation

```bash
pip install pandas numpy geopandas matplotlib seaborn scikit-learn libpysal esda mgwr shap
```

## Usage

### Basic Data Reading

```python
from data_process.data_reader import data_reader

# Read global SSI data
city_list = data_reader(
    file_path='data/SSI_golbal_data.csv',
    init_classes=4,
    classification_strategy='quartiles'
)
```

### Spatial Analysis Example

```python
# Moran's I analysis
from analysis.Moran.Morans import Moran

# Getis-Ord hotspot analysis
from analysis.Getis-Ord.Getis-Ord import getis_ord_analysis
```

### Visualization Example

```python
from visual.MSA_SSI_violin import plot_raincloud_like, load_and_prepare_long

# Load and visualize SSI distribution
theme_map = {
    "Theme1": "SES",
    "Theme2": "HCD",
    "Theme3": "MSL",
    "Theme4": "HT",
    "Themes": "Comp."
}

long_df = load_and_prepare_long('data/SSI_golbal_data.csv', theme_map)
plot_raincloud_like(long_df, theme_order=["SES", "HCD", "MSL", "HT", "Comp."])
```

## Citation

If you use this code in your research, please cite:

```
"A Mobility-Based Framework for Measuring Socio-Spatial Segregation in 30 U.S. Metropolitan Areas."
```
