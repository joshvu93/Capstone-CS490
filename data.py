# Imports

import pandas as pd


# ================================================
# Load CSV files
# ================================================

def load_csv_files(
    file_paths
):


    datasets = []


    for file_path in file_paths:


        dataset = pd.read_csv(
            file_path,
            header=[0, 1, 2]
        )


        datasets.append(
            dataset
        )


    return datasets


# ================================================
# Extract one coordinate
# ================================================

def extract_coordinate(
    dataset,
    bodypart,
    coordinate
):


    # Search CSV headers

    for column in dataset.columns:


        # Ensure column has expected
        # multi-level header

        if len(column) < 3:

            continue


        # Check bodypart and coordinate

        if (
            column[1] == bodypart
            and
            column[2] == coordinate
        ):


            values = dataset[
                column
            ]


            # Convert to numeric array

            return pd.to_numeric(
                values,
                errors="coerce"
            ).to_numpy()


    return None


# ================================================
# Extract standardized variables
# ================================================

def extract_variables(
    dataset
):


    variables = {}


    # ============================================
    # Frame
    # ============================================

    variables["frame"] = (
        pd.to_numeric(
            dataset.iloc[:, 0],
            errors="coerce"
        ).to_numpy()
    )


    # ============================================
    # Tail Tip
    # ============================================

    variables["tail_tip_x"] = (
        extract_coordinate(
            dataset,
            "TailTip",
            "x"
        )
    )


    variables["tail_tip_y"] = (
        extract_coordinate(
            dataset,
            "TailTip",
            "y"
        )
    )


    # ============================================
    # Tail Base
    # ============================================

    variables["tail_base_x"] = (
        extract_coordinate(
            dataset,
            "TailBase",
            "x"
        )
    )


    variables["tail_base_y"] = (
        extract_coordinate(
            dataset,
            "TailBase",
            "y"
        )
    )


    # ============================================
    # Snout
    # ============================================

    variables["snout_x"] = (
        extract_coordinate(
            dataset,
            "SnoutTip",
            "x"
        )
    )


    variables["snout_y"] = (
        extract_coordinate(
            dataset,
            "SnoutTip",
            "y"
        )
    )


    # ============================================
    # MTP
    # ============================================

    variables["mtp_x"] = (
        extract_coordinate(
            dataset,
            "MTP",
            "x"
        )
    )


    variables["mtp_y"] = (
        extract_coordinate(
            dataset,
            "MTP",
            "y"
        )
    )


    # ============================================
    # Ankle
    # ============================================

    variables["ankle_x"] = (
        extract_coordinate(
            dataset,
            "Ankle",
            "x"
        )
    )


    variables["ankle_y"] = (
        extract_coordinate(
            dataset,
            "Ankle",
            "y"
        )
    )


    return variables