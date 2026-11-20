"""Loading helpers for DeepLabCut three-row-header CSV exports."""

from pathlib import Path
import pandas as pd


def load_csv_files(file_paths):
    """Load one or more DeepLabCut CSV files while preserving their headers."""
    datasets = []
    for file_path in file_paths:
        try:
            frame = pd.read_csv(file_path, header=[0, 1, 2])
        except (OSError, pd.errors.ParserError, UnicodeDecodeError) as exc:
            raise ValueError(f"Could not read {file_path}: {exc}") from exc
        if frame.empty or len(frame.columns) < 2:
            raise ValueError(f"{file_path} does not contain tracking coordinates.")
        datasets.append(frame)
    return datasets


def extract_variables(dataset):
    """Return frame and bodypart coordinate/likelihood arrays from DLC data."""
    if not isinstance(dataset.columns, pd.MultiIndex) or dataset.columns.nlevels < 3:
        raise ValueError("Expected a DeepLabCut CSV with three header rows.")
    variables = {"frame": pd.to_numeric(dataset.iloc[:, 0], errors="coerce").to_numpy()}
    for column in dataset.columns[1:]:
        _, bodypart, coordinate = column[:3]
        if not bodypart or not coordinate:
            continue
        key = f"{bodypart}_{coordinate.lower()}"
        variables[key] = pd.to_numeric(dataset[column], errors="coerce").to_numpy()
    return variables


def extract_coordinate(dataset, bodypart, coordinate):
    return extract_variables(dataset).get(f"{bodypart}_{coordinate.lower()}")
