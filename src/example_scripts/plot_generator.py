"""Plot generation utilities for academic publications.

This module provides functions to create publication-quality plots with
proper styling, labels, and formatting suitable for academic papers.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import rcParams


# Set publication-quality style
def set_publication_style() -> None:
    """Configure matplotlib for publication-quality plots."""
    rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman"],
            "font.size": 10,
            "axes.labelsize": 10,
            "axes.titlesize": 10,
            "legend.fontsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "figure.titlesize": 11,
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.1,
        }
    )


def create_bar_plot(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    hue_col: Optional[str] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    figsize: Tuple[int, int] = (6, 4),
    palette: str = "viridis",
    show_values: bool = True,
    output_path: Optional[Union[str, Path]] = None,
) -> plt.Figure:
    """Create a publication-quality bar plot.

    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        hue_col: Column name for grouping (optional)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        figsize: Figure size (width, height) in inches
        palette: Color palette name
        show_values: Whether to display values on bars
        output_path: Path to save the figure (optional)

    Returns:
        matplotlib Figure object
    """
    set_publication_style()
    fig, ax = plt.subplots(figsize=figsize)

    if hue_col:
        sns.barplot(data=data, x=x_col, y=y_col, hue=hue_col, palette=palette, ax=ax)
    else:
        sns.barplot(data=data, x=x_col, y=y_col, palette=palette, ax=ax)

    # Customize appearance
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Add value labels on bars if requested
    if show_values:
        for container in ax.containers:
            ax.bar_label(container, fmt="%.2f", padding=3, fontsize=8)

    # Improve layout
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")

    return fig


def create_line_plot(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    hue_col: Optional[str] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    figsize: Tuple[int, int] = (6, 4),
    palette: str = "viridis",
    marker: str = "o",
    linestyle: str = "-",
    error_bars: Optional[str] = None,
    output_path: Optional[Union[str, Path]] = None,
) -> plt.Figure:
    """Create a publication-quality line plot.

    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        hue_col: Column name for grouping (optional)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        figsize: Figure size (width, height) in inches
        palette: Color palette name
        marker: Marker style
        linestyle: Line style
        error_bars: Column name for error bars (optional)
        output_path: Path to save the figure (optional)

    Returns:
        matplotlib Figure object
    """
    set_publication_style()
    fig, ax = plt.subplots(figsize=figsize)

    if hue_col:
        # Get unique groups for consistent coloring
        groups = data[hue_col].unique()
        colors = sns.color_palette(palette, len(groups))

        for i, group in enumerate(groups):
            group_data = data[data[hue_col] == group]
            x = group_data[x_col]
            y = group_data[y_col]

            if error_bars and error_bars in group_data.columns:
                y_err = group_data[error_bars]
                ax.errorbar(
                    x,
                    y,
                    yerr=y_err,
                    marker=marker,
                    linestyle=linestyle,
                    color=colors[i],
                    label=group,
                    capsize=3,
                )
            else:
                ax.plot(
                    x,
                    y,
                    marker=marker,
                    linestyle=linestyle,
                    color=colors[i],
                    label=group,
                )
    else:
        if error_bars and error_bars in data.columns:
            y_err = data[error_bars]
            ax.errorbar(
                data[x_col],
                data[y_col],
                yerr=y_err,
                marker=marker,
                linestyle=linestyle,
                capsize=3,
            )
        else:
            ax.plot(data[x_col], data[y_col], marker=marker, linestyle=linestyle)

    # Customize appearance
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if hue_col:
        ax.legend()

    # Improve layout
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")

    return fig


def create_scatter_plot(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    hue_col: Optional[str] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    figsize: Tuple[int, int] = (6, 4),
    palette: str = "viridis",
    alpha: float = 0.7,
    regression_line: bool = False,
    output_path: Optional[Union[str, Path]] = None,
) -> plt.Figure:
    """Create a publication-quality scatter plot.

    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        hue_col: Column name for grouping (optional)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        figsize: Figure size (width, height) in inches
        palette: Color palette name
        alpha: Transparency of points
        regression_line: Whether to add a regression line
        output_path: Path to save the figure (optional)

    Returns:
        matplotlib Figure object
    """
    set_publication_style()
    fig, ax = plt.subplots(figsize=figsize)

    if hue_col:
        sns.scatterplot(
            data=data,
            x=x_col,
            y=y_col,
            hue=hue_col,
            palette=palette,
            alpha=alpha,
            ax=ax,
        )
    else:
        sns.scatterplot(data=data, x=x_col, y=y_col, alpha=alpha, ax=ax)

    # Add regression line if requested
    if regression_line:
        sns.regplot(
            data=data,
            x=x_col,
            y=y_col,
            scatter=False,
            line_kws={"color": "red", "alpha": 0.7},
            ax=ax,
        )

    # Customize appearance
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Improve layout
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")

    return fig


def create_box_plot(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    hue_col: Optional[str] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    figsize: Tuple[int, int] = (6, 4),
    palette: str = "viridis",
    show_points: bool = False,
    output_path: Optional[Union[str, Path]] = None,
) -> plt.Figure:
    """Create a publication-quality box plot.

    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        hue_col: Column name for grouping (optional)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        figsize: Figure size (width, height) in inches
        palette: Color palette name
        show_points: Whether to show individual data points
        output_path: Path to save the figure (optional)

    Returns:
        matplotlib Figure object
    """
    set_publication_style()
    fig, ax = plt.subplots(figsize=figsize)

    if hue_col:
        sns.boxplot(
            data=data,
            x=x_col,
            y=y_col,
            hue=hue_col,
            palette=palette,
            ax=ax,
            showfliers=not show_points,
        )
    else:
        sns.boxplot(
            data=data,
            x=x_col,
            y=y_col,
            palette=palette,
            ax=ax,
            showfliers=not show_points,
        )

    # Show individual points if requested
    if show_points:
        sns.stripplot(
            data=data,
            x=x_col,
            y=y_col,
            hue=hue_col,
            palette=palette,
            ax=ax,
            size=3,
            alpha=0.5,
            dodge=True,
        )

    # Customize appearance
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Improve layout
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")

    return fig


def create_histogram(
    data: Union[pd.DataFrame, pd.Series, List[float]],
    column: Optional[str] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "Frequency",
    figsize: Tuple[int, int] = (6, 4),
    bins: Union[int, str] = "auto",
    kde: bool = True,
    color: str = "skyblue",
    output_path: Optional[Union[str, Path]] = None,
) -> plt.Figure:
    """Create a publication-quality histogram.

    Args:
        data: Data for histogram (DataFrame, Series, or list)
        column: Column name if data is DataFrame (optional)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        figsize: Figure size (width, height) in inches
        bins: Number of bins or binning strategy
        kde: Whether to add kernel density estimate
        color: Color of histogram bars
        output_path: Path to save the figure (optional)

    Returns:
        matplotlib Figure object
    """
    set_publication_style()
    fig, ax = plt.subplots(figsize=figsize)

    # Extract data based on input type
    if isinstance(data, pd.DataFrame) and column:
        plot_data = data[column].dropna()
    elif isinstance(data, pd.Series):
        plot_data = data.dropna()
    else:
        plot_data = pd.Series(data).dropna()

    # Create histogram
    sns.histplot(
        plot_data,
        bins=bins,
        kde=kde,
        color=color,
        ax=ax,
        stat="density" if kde else "count",
    )

    # Customize appearance
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Improve layout
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")

    return fig


def create_correlation_heatmap(
    data: pd.DataFrame,
    title: str = "Correlation Matrix",
    figsize: Tuple[int, int] = (8, 6),
    cmap: str = "RdBu_r",
    annot: bool = True,
    output_path: Optional[Union[str, Path]] = None,
) -> plt.Figure:
    """Create a publication-quality correlation heatmap.

    Args:
        data: DataFrame with numeric columns
        title: Plot title
        figsize: Figure size (width, height) in inches
        cmap: Color map for the heatmap
        annot: Whether to annotate cells with correlation values
        output_path: Path to save the figure (optional)

    Returns:
        matplotlib Figure object
    """
    set_publication_style()
    fig, ax = plt.subplots(figsize=figsize)

    # Calculate correlation matrix
    corr_matrix = data.corr()

    # Create heatmap
    sns.heatmap(
        corr_matrix,
        annot=annot,
        cmap=cmap,
        center=0,
        square=True,
        ax=ax,
        fmt=".2f",
        cbar_kws={"shrink": 0.8},
    )

    # Customize appearance
    ax.set_title(title, fontweight="bold")

    # Improve layout
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")

    return fig


def save_figure(
    fig: plt.Figure,
    output_path: Union[str, Path],
    formats: List[str] = ["png", "pdf"],
    dpi: int = 300,
) -> None:
    """Save figure in multiple formats for publication.

    Args:
        fig: matplotlib Figure object
        output_path: Base path for saving (without extension)
        formats: List of formats to save (e.g., ['png', 'pdf', 'svg'])
        dpi: Resolution for raster formats
    """
    output_path = Path(output_path)

    for fmt in formats:
        save_path = output_path.with_suffix(f".{fmt}")
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        print(f"Saved: {save_path}")


if __name__ == "__main__":
    # Example usage
    from data_loader import create_sample_data

    # Generate sample data
    sample_df = create_sample_data(100)

    # Create example plots
    print("Creating example plots...")

    # Bar plot
    bar_data = sample_df.groupby("group")["measurement_1"].mean().reset_index()
    create_bar_plot(
        bar_data,
        "group",
        "measurement_1",
        title="Mean Measurement by Group",
        xlabel="Group",
        ylabel="Mean Measurement 1",
        output_path="example_bar_plot.png",
    )

    # Scatter plot
    create_scatter_plot(
        sample_df,
        "measurement_1",
        "measurement_2",
        hue_col="group",
        title="Measurement 1 vs Measurement 2",
        xlabel="Measurement 1",
        ylabel="Measurement 2",
        regression_line=True,
        output_path="example_scatter_plot.png",
    )

    # Box plot
    create_box_plot(
        sample_df,
        "group",
        "measurement_1",
        title="Measurement 1 Distribution by Group",
        xlabel="Group",
        ylabel="Measurement 1",
        show_points=True,
        output_path="example_box_plot.png",
    )

    print("Example plots created successfully!")
