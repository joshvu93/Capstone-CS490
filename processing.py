# Imports

import numpy as np


# ================================================
# Select good data region
# ================================================

def select_good_region(
    values,
    start_index,
    end_index
):


    return values[
        start_index:end_index
    ].copy()


# ================================================
# Remove bad point
# ================================================

def remove_bad_point(
    values,
    index
):


    cleaned_values = (
        values.copy()
    )


    cleaned_values[
        index
    ] = np.nan


    return cleaned_values


# ================================================
# Fill gaps
# ================================================

def fill_gaps(
    values
):


    # TODO:
    #
    # Implement professor's
    # spline interpolation.

    return values


# ================================================
# Convert units
# ================================================

def convert_units(
    values,
    calibration
):


    return (
        values
        *
        calibration
    )


# ================================================
# Convert units and invert axis
# ================================================

def convert_units_inverted(
    values,
    calibration
):


    return (
        -values
        *
        calibration
    )


# ================================================
# Detrend
# ================================================

def detrend_signal(
    time,
    values,
    polynomial_order
):


    # TODO:
    #
    # Implement professor's
    # polynomial detrending.

    return values


# ================================================
# Mean center
# ================================================

def mean_center(
    values
):


    return (
        values
        -
        np.nanmean(
            values
        )
    )


# ================================================
# Smooth
# ================================================

def smooth_signal(
    time,
    values
):


    # TODO:
    #
    # Implement professor's
    # smoothing spline.

    return values