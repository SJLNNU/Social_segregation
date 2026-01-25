import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Union, Dict


# -----------------------------
# 0) Data prep helpers
# -----------------------------
def load_and_prepare_long(
    csv_path: str,
    theme_map: dict,
    value_colname: str = "Value",
    theme_colname: str = "Theme",
) -> pd.DataFrame:
    """
    Read csv, select theme columns, rename, melt to long format.
    """
    df = pd.read_csv(csv_path)

    missing = [c for c in theme_map.keys() if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    wide = df[list(theme_map.keys())].rename(columns=theme_map)
    long = wide.melt(var_name=theme_colname, value_name=value_colname)
    return long


def set_publication_style(font_family: str = "Calibri", font_size: int = 10):
    """
    Set a clean, publication-friendly matplotlib style.
    """
    plt.rcParams["font.family"] = font_family
    plt.rcParams["font.size"] = font_size
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False


def _finalize_axes(ax, xlabel: str, ylabel: str, title: Optional[str] = None):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.grid(axis="y", alpha=0.2)
    return ax


def _maybe_save(fig, save_path: Optional[str], dpi: int = 300):
    if save_path:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")


# -----------------------------
# 1) Violin plot (your baseline, slightly refined)
# -----------------------------
def plot_violin(
    long_df: pd.DataFrame,
    theme_order: Optional[List[str]] = None,
    palette: Optional[Union[List[str], Dict]] = None,
    figsize=(6, 4),
    dpi=300,
    alpha=0.55,
    inner="box",   # "box" / "quartile" / None
    cut=0,
    bw="scott",
    xlabel="Social Dimensions",
    ylabel="Global SSI Value",
    title=None,
    save_path=None,
):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    sns.violinplot(
        data=long_df,
        x="Theme",
        y="Value",
        order=theme_order,
        palette=palette,
        cut=cut,
        bw=bw,
        inner=inner,
        linewidth=1,
        ax=ax
    )

    # control violin transparency
    for coll in ax.collections:
        try:
            coll.set_alpha(alpha)
        except Exception:
            pass

    _finalize_axes(ax, xlabel, ylabel, title)
    fig.tight_layout()
    _maybe_save(fig, save_path, dpi=dpi)
    plt.show()


# -----------------------------
# 2) Raincloud-style: violin + box + jitter (robust, no extra libs)
#    (严格来说是“raincloud-like”，因为半小提琴需要额外裁剪实现)
# -----------------------------
def plot_raincloud_like(
    long_df: pd.DataFrame,
    theme_order: Optional[List[str]] = None,
    palette: Optional[Union[List[str], Dict]] = None,
    figsize=(6.4, 4.2),
    dpi=300,
    violin_alpha=0.35,
    jitter_alpha=0.35,
    jitter_size=2.5,
    jitter=0.18,
    box_width=0.15,
    xlabel="Social Dimensions",
    ylabel="Global SSI Value",
    title=None,
    save_path=None,
):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # Layer 1: violin (distribution)
    sns.violinplot(
        data=long_df, x="Theme", y="Value",
        order=theme_order, palette=palette,
        inner=None, cut=0, linewidth=0.8, ax=ax
    )
    for coll in ax.collections:
        try:
            coll.set_alpha(violin_alpha)
        except Exception:
            pass

    # Layer 2: box (summary)
    sns.boxplot(
        data=long_df, x="Theme", y="Value",
        order=theme_order,
        width=box_width,
        showcaps=True,
        boxprops={"facecolor": "white", "edgecolor": "black", "linewidth": 1},
        medianprops={"color": "black", "linewidth": 1.2},
        whiskerprops={"color": "black", "linewidth": 1},
        capprops={"color": "black", "linewidth": 1},
        showfliers=False,
        ax=ax
    )

    # Layer 3: jittered points (raw data)
    sns.stripplot(
        data=long_df, x="Theme", y="Value",
        order=theme_order,
        color="black",
        alpha=jitter_alpha,
        size=jitter_size,
        jitter=jitter,
        ax=ax
    )

    _finalize_axes(ax, xlabel, ylabel, title)
    fig.tight_layout()
    _maybe_save(fig, save_path, dpi=dpi)
    plt.show()


# -----------------------------
# 3) Boxplot + swarm/strip (most "journal-safe")
# -----------------------------
def plot_box_with_points(
    long_df: pd.DataFrame,
    theme_order: Optional[List[str]] = None,
    palette: Optional[Union[List[str], Dict]] = None,
    point_mode: str = "strip",  # "strip" or "swarm"
    figsize=(6, 4),
    dpi=300,
    box_width=0.5,
    point_alpha=0.35,
    point_size=2.7,
    jitter=0.18,
    xlabel="Social Dimensions",
    ylabel="Global SSI Value",
    title=None,
    save_path=None,
):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    sns.boxplot(
        data=long_df, x="Theme", y="Value",
        order=theme_order, palette=palette,
        width=box_width, showfliers=False,
        linewidth=1, ax=ax
    )

    if point_mode.lower() == "swarm":
        # swarm can be slow for huge N; if too slow, switch to strip
        sns.swarmplot(
            data=long_df, x="Theme", y="Value",
            order=theme_order,
            color="black", alpha=point_alpha, size=point_size,
            ax=ax
        )
    else:
        sns.stripplot(
            data=long_df, x="Theme", y="Value",
            order=theme_order,
            color="black", alpha=point_alpha, size=point_size,
            jitter=jitter, ax=ax
        )

    _finalize_axes(ax, xlabel, ylabel, title)
    fig.tight_layout()
    _maybe_save(fig, save_path, dpi=dpi)
    plt.show()


# -----------------------------
# 4) Point-interval plot (median + IQR or mean + CI)
# -----------------------------
def _bootstrap_ci(x: np.ndarray, stat_func=np.mean, n_boot=2000, ci=0.95, seed=42):
    rng = np.random.default_rng(seed)
    x = x[~np.isnan(x)]
    if len(x) == 0:
        return np.nan, np.nan
    boots = [stat_func(rng.choice(x, size=len(x), replace=True)) for _ in range(n_boot)]
    lo = np.quantile(boots, (1 - ci) / 2)
    hi = np.quantile(boots, 1 - (1 - ci) / 2)
    return lo, hi


def plot_point_interval(
    long_df: pd.DataFrame,
    theme_order: Optional[List[str]] = None,
    point_stat: str = "median",     # "median" or "mean"
    interval: str = "IQR",          # "IQR" or "CI"
    ci_level: float = 0.95,
    n_boot: int = 2000,
    figsize=(6, 3.6),
    dpi=300,
    xlabel="Social Dimensions",
    ylabel="Global SSI Value",
    title=None,
    save_path=None,
):
    if theme_order is None:
        theme_order = list(long_df["Theme"].unique())

    summary = []
    for th in theme_order:
        vals = long_df.loc[long_df["Theme"] == th, "Value"].to_numpy(dtype=float)

        if point_stat.lower() == "mean":
            center = np.nanmean(vals)
            stat_func = np.mean
        else:
            center = np.nanmedian(vals)
            stat_func = np.median

        if interval.upper() == "CI":
            lo, hi = _bootstrap_ci(vals, stat_func=stat_func, n_boot=n_boot, ci=ci_level)
        else:
            lo = np.nanquantile(vals, 0.25)
            hi = np.nanquantile(vals, 0.75)

        summary.append((th, center, lo, hi))

    s = pd.DataFrame(summary, columns=["Theme", "Center", "Lo", "Hi"])

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # x positions
    x = np.arange(len(theme_order))
    y = s["Center"].to_numpy()
    yerr_low = y - s["Lo"].to_numpy()
    yerr_high = s["Hi"].to_numpy() - y

    ax.errorbar(
        x, y,
        yerr=[yerr_low, yerr_high],
        fmt="o",
        capsize=4,
        elinewidth=1.2,
        markersize=5
    )

    ax.set_xticks(x)
    ax.set_xticklabels(theme_order)

    interval_label = "IQR (25–75%)" if interval.upper() != "CI" else f"{int(ci_level*100)}% bootstrap CI"
    stat_label = "Median" if point_stat.lower() != "mean" else "Mean"
    if title is None:
        title = f"{stat_label} with {interval_label}"

    _finalize_axes(ax, xlabel, ylabel, title)
    fig.tight_layout()
    _maybe_save(fig, save_path, dpi=dpi)
    plt.show()


# -----------------------------
# 5) Example usage (keep your mapping & colors)
# -----------------------------
if __name__ == "__main__":
    # your original mapping
    theme_map = {
        "Theme1": "SES",
        "Theme2": "HCD",
        "Theme3": "MSL",
        "Theme4": "HT",   # 你原来写 HT；建议统一成 H&T
        "Themes": "Comp."
    }

    # your palette (可替换为更“期刊友好”的 muted/cb-safe)
    theme_colors = ["#1f77b4", "#6a3d9a", "#e377c2", "#2ca02c", "#17becf"]

    # your CSV path
    csv_path = r"D:\Code\Social_segregation\data\SSI_golbal_data.csv"

    set_publication_style(font_family="Calibri", font_size=10)

    long_df = load_and_prepare_long(csv_path, theme_map)
    theme_order = ["SES", "HCD", "MSL", "HT", "Comp."]

    # 1) violin
    # plot_violin(
    #     long_df, theme_order=theme_order, palette=theme_colors,
    #     inner="box", alpha=0.5,
    #     title=None
    # )

    # 2) raincloud-like (violin + box + jitter)
    plot_raincloud_like(
        long_df, theme_order=theme_order, palette=theme_colors,
        box_width=0.12,
        title=None
    )

    # 3) box + points (strip)
    # plot_box_with_points(
    #     long_df, theme_order=theme_order, palette=theme_colors,
    #     point_mode="strip",
    #     title=None
    # )

    # # 4) point-interval: median + IQR
    # plot_point_interval(
    #     long_df, theme_order=theme_order,
    #     point_stat="median", interval="IQR",
    #     title=None
    # )

    # # 4b) point-interval: mean + 95% bootstrap CI
    # plot_point_interval(
    #     long_df, theme_order=theme_order,
    #     point_stat="mean", interval="CI", ci_level=0.95, n_boot=2000,
    #     title=None
    # )
