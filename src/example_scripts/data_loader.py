"""Data loading and validation utilities for academic data analysis.

This module provides functions to load various data formats commonly used in
academic research, with built-in validation and error handling.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd


def load_csv_data(
    file_path: Union[str, Path],
    required_columns: Optional[List[str]] = None,
    **kwargs: Any,
) -> pd.DataFrame:
    """Load CSV data with validation and error handling.

    Args:
        file_path: Path to the CSV file
        required_columns: List of column names that must be present
        **kwargs: Additional arguments passed to pandas.read_csv

    Returns:
        Loaded DataFrame

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If required columns are missing
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    try:
        df = pd.read_csv(file_path, **kwargs)
    except Exception as e:
        raise ValueError(f"Error reading CSV file {file_path}: {e}") from e

    if required_columns:
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

    return df


def load_excel_data(
    file_path: Union[str, Path],
    sheet_name: Optional[Union[str, int]] = 0,
    required_columns: Optional[List[str]] = None,
    **kwargs: Any,
) -> pd.DataFrame:
    """Load Excel data with validation and error handling.

    Args:
        file_path: Path to the Excel file
        sheet_name: Sheet to load (name or index)
        required_columns: List of column names that must be present
        **kwargs: Additional arguments passed to pandas.read_excel

    Returns:
        Loaded DataFrame

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If required columns are missing or sheet doesn't exist
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Excel file not found: {file_path}")

    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
    except Exception as e:
        raise ValueError(f"Error reading Excel file {file_path}: {e}") from e

    if required_columns:
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

    return df


def load_json_data(file_path: Union[str, Path]) -> Any:
    """Load JSON data with error handling.

    Args:
        file_path: Path to the JSON file

    Returns:
        Parsed JSON data (dict, list, or other JSON-serializable types)

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If JSON is invalid
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file {file_path}: {e}") from e
    except Exception as e:
        raise ValueError(f"Error reading JSON file {file_path}: {e}") from e


def validate_numeric_data(
    df: pd.DataFrame, columns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Validate numeric data for common issues.

    Args:
        df: DataFrame to validate
        columns: Specific columns to validate (default: all numeric columns)

    Returns:
        Dictionary with validation results including:
        - missing_values: Count of missing values per column
        - infinite_values: Count of infinite values per column
        - outliers: Count of outliers (beyond 3 standard deviations) per column
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()

    validation_results: Dict[str, Any] = {
        "missing_values": {},
        "infinite_values": {},
        "outliers": {},
    }

    for col in columns:
        if col not in df.columns:
            continue

        series = df[col]

        # Count missing values
        validation_results["missing_values"][col] = series.isna().sum()

        # Count infinite values
        validation_results["infinite_values"][col] = np.isinf(series).sum()

        # Count outliers (beyond 3 standard deviations)
        if len(series) > 1:
            mean = series.mean()
            std = series.std()
            if std > 0:  # Avoid division by zero
                outliers = ((series - mean).abs() > 3 * std).sum()
                validation_results["outliers"][col] = outliers
            else:
                validation_results["outliers"][col] = 0

    return validation_results


def create_sample_data(size: int = 100) -> pd.DataFrame:
    """Create sample data for testing and demonstration.

    Args:
        size: Number of samples to generate

    Returns:
        DataFrame with sample data including:
        - group: Categorical variable (A, B, C)
        - measurement_1: Normally distributed values
        - measurement_2: Log-normally distributed values
        - time_point: Sequential time points
    """
    np.random.seed(42)  # For reproducible results

    data = {
        "group": np.random.choice(["A", "B", "C"], size=size),
        "measurement_1": np.random.normal(10, 2, size=size),
        "measurement_2": np.random.lognormal(2, 0.5, size=size),
        "time_point": np.arange(size),
    }

    return pd.DataFrame(data)


if __name__ == "__main__":
    # Example usage
    sample_df = create_sample_data(50)
    print("Sample data created:")
    print(sample_df.head())
    print("\nData validation results:")
    validation = validate_numeric_data(sample_df)
    print(validation)
