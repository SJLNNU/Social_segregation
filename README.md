# Social Segregation Analysis

This repository contains the code for the paper **"A Mobility-Based Framework for Measuring Socio-Spatial Segregation in 30 U.S. Metropolitan Areas."**

## Overview

This project provides a comprehensive framework for analyzing socio-spatial segregation patterns across 30 U.S. metropolitan areas using mobility-based measurements. The analysis includes multiple dimensions of segregation (SES, HCD, MSL, HT) and employs various spatial statistical methods.

## Project Structure

```
Social_segregation_upload/
├── analysis/                      # Analysis modules
│   ├── Moran/                     # Spatial autocorrelation (Fig. 7)
│   │   └── Morans.py              # Moran's I
│   ├── Getis-Ord/                 # OHSA and overlap (Fig. 4. Extremely segregated tracts)
│   │   ├── OHSA_Filter_result.py  # OHSA tertile filter results
│   │   ├── Over_lap_OHSA_result.py # Overlap summary across themes
│   │   └── overlap_viz.py         # Overlap visualization
│   ├── Correlation_analysis/      # Statistical correlation (Fig. 5, 6)
│   │   ├── spearman_overall_heatmap.py       # 30 MSAs correlation (Fig. 5)
│   │   └── spearman_correlation_analysis_rolling.py  # Sliding-window (Fig. 6)
│   └── Census_Tract_level/        # Tract-level extreme cases
│       └── Find_mult_hotspot.py   # Common hotspots across dimensions
├── data_process/                  # Data processing
│   ├── Data_converter.py
│   ├── data_reader.py
│   └── data_struct.py
└── visual/                        # Visualization scripts
    ├── MSA_SSI_violin.py          # Violin plots (Fig. 3)
    ├── Four_D_visual.py           # MSAs segregation rankings (Fig. 4)
    ├── Moran_scatter_visual.py    # Moran scatter (Fig. 7)
    ├── Jaccard_similarity_OHSA.py # OHSA Jaccard similarity
    └── Jaccard_similarity_viz.py  # Jaccard similarity visualization
```

## Main Features

### 1.Visualization
- **Violin plots**: visual/MSA_SSI_violin.py (Figure 3)
- **MSAs Segregation rankings**: visual/Four_D_visual.py （Figure 4）

### 2.Statistical Correlation Analysis
- **Correlation analysis for 30 MSAs**:analysis/Correlation_analysis/spearman_overall_heatmap.py(Figure 5)
- **Shapiro-Wilk test**: Software:GraphPad Prism 10.1.2
- **Sliding-window correlation analysis**: analysis/Correlation_analysis/spearman_correlation_analysis_rolling.py(Figure 6)

### 3.Spatial Autocorrelation Analysis
- **Moran's I**:analysis/Moran/Morans.py
- **Moran's I Visualization**:visual/Moran_scatter_visual.py(Figure 7)

### 4. Extremely segregated census tracts detection
- **Optimised Hot Spot Analysis (OHSA)**: Software:ArcGIS Pro and analysis/Getis-Ord/OHSA_Filter_result.py
- **OHSA Jaccard similarity analysis**:visual/Jaccard_similarity_OHSA.py
- **Extreme cases**:analysis/Census_Tract_level/Find_mult_hotspot.py

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

# Citation

If you use this code in your research, please cite:

```
"A Mobility-Based Framework for Measuring Socio-Spatial Segregation in 30 U.S. Metropolitan Areas."
```
