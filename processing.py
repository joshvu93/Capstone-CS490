"""Coordinate cleaning and signal processing for swimming kinematics."""

import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator
from scipy.signal import savgol_filter


def select_good_region(values, start_index, end_index):
    return np.asarray(values)[start_index:end_index].copy()


def remove_bad_point(values, index):
    cleaned = np.asarray(values, dtype=float).copy()
    cleaned[index] = np.nan
    return cleaned


def apply_manual_outliers(frame, outliers):
    """Set manually selected (row position, DLC column) samples to NaN."""
    result = frame.copy()
    for row, column in outliers:
        if not 0 <= row < len(result):
            continue
        column_position = next(
            (
                index
                for index, candidate in enumerate(result.columns)
                if candidate == column
            ),
            None,
        )
        if column_position is not None:
            result.iloc[row, column_position] = np.nan
    return result


def filter_data(frame, likelihood_threshold=0.2, jump_sigma=8.0):
    """Mask low-confidence detections and isolated implausible jumps.

    Keep the original DLC table shape so this output can still be inspected
    against the raw CSV. Invalid coordinates are represented as NaN for the
    interpolation stage that follows.
    """
    result = frame.copy()
    bodyparts = {
        str(c[1]) for c in result.columns if isinstance(c, tuple) and len(c) >= 3
    }
    for part in bodyparts:
        coords = {}
        for axis in ("x", "y"):
            col = next(
                (
                    c
                    for c in result.columns
                    if isinstance(c, tuple)
                    and len(c) >= 3
                    and c[1] == part
                    and c[2].lower() == axis
                ),
                None,
            )
            if col is not None:
                result[col] = pd.to_numeric(result[col], errors="coerce")
                coords[axis] = col
        likelihood = next(
            (
                c
                for c in result.columns
                if isinstance(c, tuple)
                and len(c) >= 3
                and c[1] == part
                and c[2].lower() == "likelihood"
            ),
            None,
        )
        invalid = pd.Series(False, index=result.index)
        if likelihood is not None:
            invalid |= (
                pd.to_numeric(result[likelihood], errors="coerce").fillna(0)
                < likelihood_threshold
            )
        for axis, col in coords.items():
            values = result[col].astype(float)
            delta = values.diff().abs()
            center = delta.median(skipna=True)
            mad = (delta - center).abs().median(skipna=True)
            if pd.notna(mad) and mad > 0:
                invalid |= delta > center + jump_sigma * 1.4826 * mad
        for col in coords.values():
            result.loc[invalid, col] = np.nan
    return result


def fill_gaps(values, max_gap=None):
    """Shape-preserving cubic interpolation; extrapolated ends stay missing."""
    arr = np.asarray(values, dtype=float).copy()
    valid = np.isfinite(arr)
    if valid.sum() < 2:
        return arr
    indices = np.arange(arr.size)
    interpolator = PchipInterpolator(indices[valid], arr[valid], extrapolate=False)
    filled = arr.copy()
    missing = ~valid
    filled[missing] = interpolator(indices[missing])
    if max_gap is not None:
        # Restore missing runs longer than the configured maximum.
        starts = np.flatnonzero(missing & np.r_[True, ~missing[:-1]])
        ends = np.flatnonzero(missing & np.r_[~missing[1:], True])
        for start, end in zip(starts, ends):
            if end - start + 1 > max_gap:
                filled[start : end + 1] = np.nan
    return filled


def convert_units(values, calibration):
    return np.asarray(values, dtype=float) * calibration


def convert_units_inverted(values, calibration):
    return -np.asarray(values, dtype=float) * calibration


def detrend_signal(time, values, polynomial_order=2):
    """Remove a polynomial trend, fitting only finite observations."""
    t = np.asarray(time, dtype=float)
    y = np.asarray(values, dtype=float)
    valid = np.isfinite(t) & np.isfinite(y)
    if valid.sum() <= polynomial_order:
        return y.copy()
    center = np.mean(t[valid])
    scale = np.ptp(t[valid]) or 1.0
    x = (t - center) / scale
    coeffs = np.polyfit(x[valid], y[valid], int(polynomial_order))
    trend = np.polyval(coeffs, x)
    baseline = np.mean(y[valid]) if polynomial_order > 0 else 0.0
    return y - trend + baseline


def mean_center(values):
    arr = np.asarray(values, dtype=float)
    valid = np.isfinite(arr)
    if not valid.any():
        return arr.copy()
    return arr - np.mean(arr[valid])


def smooth_signal(time, values, window_seconds=0.04, polynomial_order=3):
    """Smooth finite segments with Savitzky-Golay filtering."""
    t = np.asarray(time, dtype=float)
    y = np.asarray(values, dtype=float).copy()
    valid = np.isfinite(t) & np.isfinite(y)
    idx = np.flatnonzero(valid)
    if idx.size < 5:
        return y
    dt = np.median(np.diff(t[idx]))
    window = max(5, int(round(window_seconds / dt)) | 1) if dt > 0 else 5
    window = min(window, idx.size if idx.size % 2 else idx.size - 1)
    order = min(polynomial_order, window - 2)
    if window >= 3 and order >= 1:
        y[idx] = savgol_filter(y[idx], window, order, mode="interp")
    return y


def process_tracking_frame(
    frame,
    calibration,
    fps,
    detrend_order=2,
    likelihood_threshold=0.2,
    smooth_seconds=0.04,
):
    """Apply filter, gap-fill, unit conversion, detrending and smoothing."""
    cleaned = filter_data(frame, likelihood_threshold=likelihood_threshold)
    frame_values = pd.to_numeric(cleaned.iloc[:, 0], errors="coerce").to_numpy(
        dtype=float
    )
    time = frame_values / float(fps)
    processed = pd.DataFrame({"frame": frame_values, "time_s": time})
    measurements = {}
    for col in cleaned.columns[1:]:
        if not isinstance(col, tuple) or len(col) < 3:
            continue
        _, bodypart, coordinate = col[:3]
        coordinate = coordinate.lower()
        raw = pd.to_numeric(cleaned[col], errors="coerce").to_numpy(dtype=float)
        if coordinate in ("x", "y"):
            filled = fill_gaps(raw)
            converted = (
                convert_units_inverted(filled, calibration)
                if coordinate == "y"
                else convert_units(filled, calibration)
            )
            detrended = detrend_signal(time, converted, detrend_order)
            smooth = smooth_signal(time, detrended, smooth_seconds)
            key = f"{bodypart}_{coordinate}"
            processed[key + "_raw_px"] = raw
            processed[key + "_filtered_px"] = filled
            processed[key + "_m"] = converted
            processed[key + "_detrended_m"] = detrended
            processed[key + "_smooth_m"] = smooth
            measurements[key] = smooth
        elif coordinate == "likelihood":
            processed[f"{bodypart}_likelihood"] = raw
    return processed, measurements


def fill_frame_gaps(frame):
    """Interpolate missing x/y detections in a raw DLC table."""
    result = frame.copy()
    for col in result.columns:
        if (
            isinstance(col, tuple)
            and len(col) >= 3
            and str(col[2]).lower() in ("x", "y")
        ):
            result[col] = fill_gaps(
                pd.to_numeric(result[col], errors="coerce").to_numpy(dtype=float)
            )
    return result


def convert_and_detrend_frame(frame, calibration, fps, polynomial_order=2):
    """Convert filled coordinates to meters and remove body translation/trend.

    This stage changes the wide, multi-index DLC table into a flat table that is
    convenient for plotting, calculating kinematics, and exporting.
    """
    frames = pd.to_numeric(frame.iloc[:, 0], errors="coerce").to_numpy(dtype=float)
    time = frames / float(fps)
    result = pd.DataFrame({"frame": frames, "time_s": time})
    for col in frame.columns[1:]:
        if not isinstance(col, tuple) or len(col) < 3:
            continue
        _, part, axis = col[:3]
        axis = str(axis).lower()
        if axis not in ("x", "y"):
            if axis == "likelihood":
                result[f"{part}_likelihood"] = pd.to_numeric(
                    frame[col], errors="coerce"
                ).to_numpy(dtype=float)
            continue
        raw = pd.to_numeric(frame[col], errors="coerce").to_numpy(dtype=float)
        scaled = (
            convert_units_inverted(raw, calibration)
            if axis == "y"
            else convert_units(raw, calibration)
        )
        result[f"{part}_{axis}_m"] = scaled
        result[f"{part}_{axis}_detrended_m"] = detrend_signal(
            time, scaled, polynomial_order
        )
    return result


def standardize_smooth_frame(frame, smooth_seconds=0.04):
    """Mean-center and smooth every detrended coordinate time series.

    Keep both standardized and smoothed columns so the final CSV preserves
    intermediate products rather than hiding a processing step.
    """
    result = frame.copy()
    time = result["time_s"].to_numpy(dtype=float)
    for col in result.columns:
        if col.endswith("_detrended_m"):
            centered = mean_center(result[col].to_numpy(dtype=float))
            smooth = smooth_signal(time, centered, smooth_seconds)
            stem = col.removesuffix("_detrended_m")
            result[f"{stem}_standardized_m"] = centered
            result[f"{stem}_smooth_m"] = smooth
    return result
