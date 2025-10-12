"""Main CLI entry point for academic data analysis scripts.

This module provides a command-line interface for the data analysis workflow,
integrating data loading, statistical analysis, and plot generation.
"""

import json
from pathlib import Path
from typing import Optional

import click

from data_loader import (
    create_sample_data,
    load_csv_data,
    load_excel_data,
    validate_numeric_data,
)
from plot_generator import (
    create_bar_plot,
    create_box_plot,
    create_correlation_heatmap,
    create_histogram,
    create_line_plot,
    create_scatter_plot,
    save_figure,
)
from statistical_analysis import (
    correlation_analysis,
    descriptive_stats,
    independent_t_test,
    normality_test,
    one_way_anova,
    paired_t_test,
)


@click.group()
def cli() -> None:
    """Academic Data Analysis Toolkit.

    A collection of tools for loading, analyzing, and visualizing academic data.
    """
    pass


@cli.command()
@click.option(
    "--size", default=100, help="Number of samples to generate", show_default=True
)
@click.option(
    "--output",
    type=click.Path(),
    default="sample_data.csv",
    help="Output file path",
    show_default=True,
)
def generate_sample_data(size: int, output: str) -> None:
    """Generate sample data for testing and demonstration."""
    click.echo(f"Generating {size} sample data points...")
    sample_df = create_sample_data(size)
    sample_df.to_csv(output, index=False)
    click.echo(f"Sample data saved to: {output}")
    click.echo(f"Data shape: {sample_df.shape}")
    click.echo("\nFirst 5 rows:")
    click.echo(sample_df.head().to_string())


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--file-type", type=click.Choice(["csv", "excel"]), default="csv")
@click.option("--sheet", default=0, help="Sheet name or index for Excel files")
def load_data(file_path: str, file_type: str, sheet: int) -> None:
    """Load and validate data from file."""
    click.echo(f"Loading {file_type.upper()} data from: {file_path}")

    try:
        if file_type == "csv":
            df = load_csv_data(file_path)
        else:
            df = load_excel_data(file_path, sheet_name=sheet)

        click.echo(f"Successfully loaded data with shape: {df.shape}")
        click.echo("\nColumn names:")
        for col in df.columns:
            click.echo(f"  - {col}")

        click.echo("\nData types:")
        click.echo(df.dtypes.to_string())

        click.echo("\nFirst 5 rows:")
        click.echo(df.head().to_string())

        # Validate numeric data
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        if numeric_cols:
            validation = validate_numeric_data(df, numeric_cols)
            click.echo("\nData validation results:")
            click.echo(json.dumps(validation, indent=2, default=str))

    except Exception as e:
        click.echo(f"Error loading data: {e}", err=True)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--file-type", type=click.Choice(["csv", "excel"]), default="csv")
@click.option("--sheet", default=0, help="Sheet name or index for Excel files")
@click.option("--column", required=True, help="Column name for analysis")
def analyze_column(file_path: str, file_type: str, sheet: int, column: str) -> None:
    """Perform descriptive statistics on a single column."""
    click.echo(f"Analyzing column '{column}' from: {file_path}")

    try:
        if file_type == "csv":
            df = load_csv_data(file_path, required_columns=[column])
        else:
            df = load_excel_data(file_path, sheet_name=sheet, required_columns=[column])

        if column not in df.columns:
            click.echo(f"Column '{column}' not found in data", err=True)
            return

        stats = descriptive_stats(df[column])
        click.echo(f"\nDescriptive statistics for '{column}':")
        for key, value in stats.items():
            click.echo(f"  {key}: {value:.4f}")

        # Normality test
        normality = normality_test(df[column])
        click.echo(f"\nNormality test (Shapiro-Wilk):")
        click.echo(f"  W-statistic: {normality['w_statistic']:.4f}")
        click.echo(f"  p-value: {normality['p_value']:.4f}")
        click.echo(f"  Is normal: {normality['is_normal']}")

        # Confidence interval
        ci = descriptive_stats(df[column]).get("ci_95", "N/A")
        if ci != "N/A":
            click.echo(f"  95% CI: ({ci[0]:.4f}, {ci[1]:.4f})")

    except Exception as e:
        click.echo(f"Error analyzing data: {e}", err=True)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--file-type", type=click.Choice(["csv", "excel"]), default="csv")
@click.option("--sheet", default=0, help="Sheet name or index for Excel files")
@click.option("--group-col", required=True, help="Column name for grouping")
@click.option("--value-col", required=True, help="Column name for values")
def compare_groups(
    file_path: str, file_type: str, sheet: int, group_col: str, value_col: str
) -> None:
    """Compare groups using statistical tests."""
    click.echo(f"Comparing groups in '{group_col}' for values in '{value_col}'")

    try:
        if file_type == "csv":
            df = load_csv_data(file_path, required_columns=[group_col, value_col])
        else:
            df = load_excel_data(
                file_path, sheet_name=sheet, required_columns=[group_col, value_col]
            )

        groups = df[group_col].unique()
        click.echo(f"\nGroups found: {list(groups)}")

        if len(groups) == 2:
            # Independent t-test for two groups
            group1_data = df[df[group_col] == groups[0]][value_col]
            group2_data = df[df[group_col] == groups[1]][value_col]

            t_test = independent_t_test(group1_data, group2_data)
            click.echo("\nIndependent t-test results:")
            click.echo(f"  t-statistic: {t_test['t_statistic']:.4f}")
            click.echo(f"  p-value: {t_test['p_value']:.4f}")
            click.echo(f"  Cohen's d: {t_test['cohens_d']:.4f}")

        elif len(groups) > 2:
            # One-way ANOVA for multiple groups
            group_data = [df[df[group_col] == group][value_col] for group in groups]
            anova = one_way_anova(group_data)
            click.echo("\nOne-way ANOVA results:")
            click.echo(f"  F-statistic: {anova['f_statistic']:.4f}")
            click.echo(f"  p-value: {anova['p_value']:.4f}")
            click.echo(f"  DF between: {anova['df_between']}")
            click.echo(f"  DF within: {anova['df_within']}")

        else:
            click.echo("Need at least 2 groups for comparison", err=True)

    except Exception as e:
        click.echo(f"Error comparing groups: {e}", err=True)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--file-type", type=click.Choice(["csv", "excel"]), default="csv")
@click.option("--sheet", default=0, help="Sheet name or index for Excel files")
@click.option("--x-col", required=True, help="X-axis column name")
@click.option("--y-col", required=True, help="Y-axis column name")
@click.option("--plot-type", type=click.Choice(["scatter", "line", "bar", "box"]))
@click.option("--hue-col", help="Column for color grouping")
@click.option("--output", type=click.Path(), help="Output file path")
@click.option("--title", help="Plot title")
def create_plot(
    file_path: str,
    file_type: str,
    sheet: int,
    x_col: str,
    y_col: str,
    plot_type: str,
    hue_col: Optional[str],
    output: Optional[str],
    title: Optional[str],
) -> None:
    """Create various types of plots from data."""
    click.echo(f"Creating {plot_type} plot from: {file_path}")

    try:
        required_cols = [x_col, y_col]
        if hue_col:
            required_cols.append(hue_col)

        if file_type == "csv":
            df = load_csv_data(file_path, required_columns=required_cols)
        else:
            df = load_excel_data(
                file_path, sheet_name=sheet, required_columns=required_cols
            )

        if not title:
            title = f"{y_col} vs {x_col}"

        output_path = Path(output) if output else None

        if plot_type == "scatter":
            fig = create_scatter_plot(
                df, x_col, y_col, hue_col=hue_col, title=title, output_path=output_path
            )
        elif plot_type == "line":
            fig = create_line_plot(
                df, x_col, y_col, hue_col=hue_col, title=title, output_path=output_path
            )
        elif plot_type == "bar":
            # For bar plots, we typically want aggregated data
            if hue_col:
                bar_data = df.groupby([x_col, hue_col])[y_col].mean().reset_index()
            else:
                bar_data = df.groupby(x_col)[y_col].mean().reset_index()
            fig = create_bar_plot(
                bar_data,
                x_col,
                y_col,
                hue_col=hue_col,
                title=title,
                output_path=output_path,
            )
        elif plot_type == "box":
            fig = create_box_plot(
                df, x_col, y_col, hue_col=hue_col, title=title, output_path=output_path
            )

        if output_path:
            click.echo(f"Plot saved to: {output_path}")
        else:
            click.echo(
                "Plot created successfully (displayed if in interactive environment)"
            )

    except Exception as e:
        click.echo(f"Error creating plot: {e}", err=True)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--file-type", type=click.Choice(["csv", "excel"]), default="csv")
@click.option("--sheet", default=0, help="Sheet name or index for Excel files")
@click.option("--output", type=click.Path(), help="Output file path for heatmap")
def correlation_matrix(
    file_path: str, file_type: str, sheet: int, output: Optional[str]
) -> None:
    """Create a correlation matrix heatmap."""
    click.echo(f"Creating correlation matrix from: {file_path}")

    try:
        if file_type == "csv":
            df = load_csv_data(file_path)
        else:
            df = load_excel_data(file_path, sheet_name=sheet)

        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        if len(numeric_cols) < 2:
            click.echo(
                "Need at least 2 numeric columns for correlation matrix", err=True
            )
            return

        click.echo(f"Numeric columns: {numeric_cols}")

        output_path = Path(output) if output else None
        fig = create_correlation_heatmap(
            df[numeric_cols], output_path=output_path, title="Correlation Matrix"
        )

        if output_path:
            click.echo(f"Correlation heatmap saved to: {output_path}")

        # Print correlation values
        corr_matrix = df[numeric_cols].corr()
        click.echo("\nCorrelation matrix values:")
        click.echo(corr_matrix.round(3).to_string())

    except Exception as e:
        click.echo(f"Error creating correlation matrix: {e}", err=True)


@cli.command()
def demo_workflow() -> None:
    """Run a complete demonstration workflow with sample data."""
    click.echo("Starting academic data analysis demonstration workflow...")

    # Step 1: Generate sample data
    click.echo("\n1. Generating sample data...")
    sample_df = create_sample_data(100)
    sample_path = "demo_sample_data.csv"
    sample_df.to_csv(sample_path, index=False)
    click.echo(f"   Sample data saved to: {sample_path}")

    # Step 2: Descriptive statistics
    click.echo("\n2. Calculating descriptive statistics...")
    stats = descriptive_stats(sample_df["measurement_1"])
    click.echo("   Measurement 1 statistics:")
    for key, value in stats.items():
        if key != "n":
            click.echo(f"     {key}: {value:.4f}")

    # Step 3: Group comparison
    click.echo("\n3. Comparing groups...")
    groups = sample_df["group"].unique()
    if len(groups) >= 2:
        group_data = [
            sample_df[sample_df["group"] == group]["measurement_1"]
            for group in groups[:2]
        ]
        t_test = independent_t_test(group_data[0], group_data[1])
        click.echo(f"   T-test between {groups[0]} and {groups[1]}:")
        click.echo(f"     p-value: {t_test['p_value']:.4f}")

    # Step 4: Create plots
    click.echo("\n4. Creating demonstration plots...")

    # Bar plot
    bar_data = sample_df.groupby("group")["measurement_1"].mean().reset_index()
    create_bar_plot(
        bar_data,
        "group",
        "measurement_1",
        title="Mean Measurement by Group",
        xlabel="Group",
        ylabel="Mean Measurement 1",
        output_path="demo_bar_plot.png",
    )
    click.echo("   Created: demo_bar_plot.png")

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
        output_path="demo_scatter_plot.png",
    )
    click.echo("   Created: demo_scatter_plot.png")

    # Correlation heatmap
    create_correlation_heatmap(
        sample_df[["measurement_1", "measurement_2", "time_point"]],
        title="Demo Correlation Matrix",
        output_path="demo_correlation_heatmap.png",
    )
    click.echo("   Created: demo_correlation_heatmap.png")

    click.echo("\nDemonstration workflow completed successfully!")
    click.echo("Check the generated files for results.")


if __name__ == "__main__":
    cli()
