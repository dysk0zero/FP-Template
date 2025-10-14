"""Statistical analysis utilities for academic research.

This module provides common statistical tests and calculations used in
academic research, with proper error handling and type annotations.
"""

from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from scipy import stats


def descriptive_stats(
    data: Union[pd.Series, np.ndarray, List[float]],
) -> Dict[str, float]:
    """Calculate descriptive statistics for a dataset.

    Args:
        data: Input data as Series, array, or list

    Returns:
        Dictionary containing:
        - mean: Arithmetic mean
        - median: Median value
        - std: Standard deviation
        - sem: Standard error of the mean
        - min: Minimum value
        - max: Maximum value
        - q1: First quartile (25th percentile)
        - q3: Third quartile (75th percentile)
        - iqr: Interquartile range

    Raises:
        ValueError: If data is empty or contains only NaN values
    """
    if len(data) == 0:
        raise ValueError("Cannot compute statistics on empty data")

    series = pd.Series(data).dropna()
    if len(series) == 0:
        raise ValueError("Data contains only NaN values")

    return {
        "n": len(series),
        "mean": float(series.mean()),
        "median": float(series.median()),
        "std": float(series.std()),
        "sem": float(stats.sem(series)),
        "min": float(series.min()),
        "max": float(series.max()),
        "q1": float(series.quantile(0.25)),
        "q3": float(series.quantile(0.75)),
        "iqr": float(series.quantile(0.75) - series.quantile(0.25)),
    }


def independent_t_test(
    group1: Union[pd.Series, np.ndarray, List[float]],
    group2: Union[pd.Series, np.ndarray, List[float]],
    equal_var: bool = True,
) -> Dict[str, float]:
    """Perform independent samples t-test.

    Args:
        group1: First group data
        group2: Second group data
        equal_var: If True, assume equal population variances (default: True)

    Returns:
        Dictionary containing:
        - t_statistic: T-test statistic
        - p_value: Two-tailed p-value
        - df: Degrees of freedom
        - cohens_d: Cohen's d effect size

    Raises:
        ValueError: If groups are too small for t-test
    """
    group1_clean = pd.Series(group1).dropna()
    group2_clean = pd.Series(group2).dropna()

    if len(group1_clean) < 2 or len(group2_clean) < 2:
        raise ValueError("Each group must have at least 2 non-NaN values")

    t_stat, p_value = stats.ttest_ind(group1_clean, group2_clean, equal_var=equal_var)
    df = len(group1_clean) + len(group2_clean) - 2

    # Calculate Cohen's d
    pooled_std = np.sqrt(
        (
            (len(group1_clean) - 1) * group1_clean.std() ** 2
            + (len(group2_clean) - 1) * group2_clean.std() ** 2
        )
        / df
    )
    cohens_d = (group1_clean.mean() - group2_clean.mean()) / pooled_std

    return {
        "t_statistic": float(t_stat),
        "p_value": float(p_value),
        "df": float(df),
        "cohens_d": float(cohens_d),
    }


def paired_t_test(
    before: Union[pd.Series, np.ndarray, List[float]],
    after: Union[pd.Series, np.ndarray, List[float]],
) -> Dict[str, float]:
    """Perform paired samples t-test.

    Args:
        before: Measurements before treatment
        after: Measurements after treatment

    Returns:
        Dictionary containing:
        - t_statistic: T-test statistic
        - p_value: Two-tailed p-value
        - df: Degrees of freedom
        - mean_diff: Mean of differences

    Raises:
        ValueError: If paired data is incomplete or too small
    """
    before_clean = pd.Series(before).dropna()
    after_clean = pd.Series(after).dropna()

    # Ensure we have the same number of paired observations
    min_len = min(len(before_clean), len(after_clean))
    if min_len < 2:
        raise ValueError("Need at least 2 complete pairs for paired t-test")

    before_clean = before_clean.iloc[:min_len]
    after_clean = after_clean.iloc[:min_len]

    t_stat, p_value = stats.ttest_rel(before_clean, after_clean)
    mean_diff = (after_clean - before_clean).mean()

    return {
        "t_statistic": float(t_stat),
        "p_value": float(p_value),
        "df": float(min_len - 1),
        "mean_diff": float(mean_diff),
    }


def one_way_anova(
    groups: List[Union[pd.Series, np.ndarray, List[float]]],
) -> Dict[str, float]:
    """Perform one-way ANOVA test.

    Args:
        groups: List of groups to compare

    Returns:
        Dictionary containing:
        - f_statistic: F-test statistic
        - p_value: P-value for the F-test
        - df_between: Degrees of freedom between groups
        - df_within: Degrees of freedom within groups

    Raises:
        ValueError: If fewer than 2 groups or groups are too small
    """
    if len(groups) < 2:
        raise ValueError("ANOVA requires at least 2 groups")

    # Clean and validate groups
    clean_groups = [pd.Series(group).dropna() for group in groups]
    if any(len(group) < 2 for group in clean_groups):
        raise ValueError("Each group must have at least 2 non-NaN values")

    f_stat, p_value = stats.f_oneway(*clean_groups)

    # Calculate degrees of freedom
    total_n = sum(len(group) for group in clean_groups)
    df_between = len(clean_groups) - 1
    df_within = total_n - len(clean_groups)

    return {
        "f_statistic": float(f_stat),
        "p_value": float(p_value),
        "df_between": float(df_between),
        "df_within": float(df_within),
    }


def correlation_analysis(
    x: Union[pd.Series, np.ndarray, List[float]],
    y: Union[pd.Series, np.ndarray, List[float]],
    method: str = "pearson",
) -> Dict[str, float]:
    """Calculate correlation between two variables.

    Args:
        x: First variable
        y: Second variable
        method: Correlation method ('pearson', 'spearman', or 'kendall')

    Returns:
        Dictionary containing:
        - correlation: Correlation coefficient
        - p_value: P-value for the correlation test
        - n: Number of complete pairs

    Raises:
        ValueError: If method is invalid or data is insufficient
    """
    valid_methods = {"pearson", "spearman", "kendall"}
    if method not in valid_methods:
        raise ValueError(f"Method must be one of {valid_methods}")

    x_clean = pd.Series(x).dropna()
    y_clean = pd.Series(y).dropna()

    # Align the data by index
    aligned_data = pd.DataFrame({"x": x_clean, "y": y_clean}).dropna()
    if len(aligned_data) < 2:
        raise ValueError("Need at least 2 complete pairs for correlation")

    if method == "pearson":
        corr, p_value = stats.pearsonr(aligned_data["x"], aligned_data["y"])
    elif method == "spearman":
        corr, p_value = stats.spearmanr(aligned_data["x"], aligned_data["y"])
    else:  # kendall
        corr, p_value = stats.kendalltau(aligned_data["x"], aligned_data["y"])

    return {
        "correlation": float(corr),
        "p_value": float(p_value),
        "n": len(aligned_data),
    }


def normality_test(data: Union[pd.Series, np.ndarray, List[float]]) -> Dict[str, float]:
    """Test for normality using Shapiro-Wilk test.

    Args:
        data: Data to test for normality

    Returns:
        Dictionary containing:
        - w_statistic: Shapiro-Wilk test statistic
        - p_value: P-value for the normality test
        - is_normal: Boolean indicating if data is normal (p > 0.05)

    Raises:
        ValueError: If data has fewer than 3 observations
    """
    data_clean = pd.Series(data).dropna()
    if len(data_clean) < 3:
        raise ValueError("Normality test requires at least 3 observations")

    w_stat, p_value = stats.shapiro(data_clean)

    return {
        "w_statistic": float(w_stat),
        "p_value": float(p_value),
        "is_normal": p_value > 0.05,
    }


def confidence_interval(
    data: Union[pd.Series, np.ndarray, List[float]],
    confidence: float = 0.95,
) -> Tuple[float, float]:
    """Calculate confidence interval for the mean.

    Args:
        data: Input data
        confidence: Confidence level (default: 0.95)

    Returns:
        Tuple of (lower_bound, upper_bound)

    Raises:
        ValueError: If data is insufficient or confidence level is invalid
    """
    if not 0 < confidence < 1:
        raise ValueError("Confidence level must be between 0 and 1")

    data_clean = pd.Series(data).dropna()
    if len(data_clean) < 2:
        raise ValueError("Need at least 2 observations for confidence interval")

    mean = data_clean.mean()
    sem = stats.sem(data_clean)
    margin = sem * stats.t.ppf((1 + confidence) / 2, len(data_clean) - 1)

    return (float(mean - margin), float(mean + margin))


if __name__ == "__main__":
    # Example usage
    sample_data = [1.2, 2.3, 3.1, 4.5, 5.2, 6.1, 7.3, 8.2, 9.1, 10.5]
    group_a = [1.2, 2.3, 3.1, 4.5, 5.2]
    group_b = [6.1, 7.3, 8.2, 9.1, 10.5]

    print("Descriptive statistics:")
    print(descriptive_stats(sample_data))

    print("\nIndependent t-test:")
    print(independent_t_test(group_a, group_b))

    print("\nCorrelation analysis:")
    print(correlation_analysis(group_a, group_b))

    print("\nNormality test:")
    print(normality_test(sample_data))

    print("\n95% Confidence interval:")
    ci = confidence_interval(sample_data)
    print(f"({ci[0]:.3f}, {ci[1]:.3f})")
