"""Kinematic measurements derived from processed tracking coordinates."""

import numpy as np
from scipy.signal import find_peaks


def calculate_time(frame, fps):
    if fps <= 0:
        raise ValueError("Frame rate must be greater than zero.")
    return np.asarray(frame, dtype=float) / float(fps)


def _finite(*arrays):
    return np.logical_and.reduce(
        [np.isfinite(np.asarray(a, dtype=float)) for a in arrays]
    )


def _peaks(values, fps):
    y = np.asarray(values, dtype=float)
    valid = np.isfinite(y)
    if valid.sum() < 5:
        return np.array([], dtype=int), np.array([], dtype=int)
    # Interpolated output should be continuous; center to avoid DC bias.
    centered = y - np.nanmedian(y)
    prominence = max(float(np.nanstd(centered)) * 0.35, np.finfo(float).eps)
    distance = max(1, int(round(fps * 0.08)))
    return (
        find_peaks(centered, distance=distance, prominence=prominence)[0],
        find_peaks(-centered, distance=distance, prominence=prominence)[0],
    )


def _frequency(peak_indices, time):
    t = np.asarray(time, dtype=float)
    if len(peak_indices) >= 2:
        intervals = np.diff(t[peak_indices])
        intervals = intervals[np.isfinite(intervals) & (intervals > 0)]
        return float(1 / np.mean(intervals)) if intervals.size else np.nan
    if len(peak_indices) == 1 and t.size > 1 and t[-1] > t[0]:
        return float(1 / (t[-1] - t[0]))
    return np.nan


def _amplitude(values, peaks, troughs):
    y = np.asarray(values, dtype=float)
    if not len(peaks) or not len(troughs):
        return np.nan
    pairs = []
    for p in peaks:
        nearest = troughs[np.argmin(np.abs(troughs - p))]
        if abs(nearest - p) > max(1, len(y) // 4):
            continue
        pairs.append(abs(y[p] - y[nearest]))
    return float(np.mean(pairs) / 2) if pairs else np.nan


def calculate_tail_frequency(number_of_waves, start_time, end_time):
    duration = end_time - start_time
    return number_of_waves / duration if duration > 0 else np.nan


def calculate_tail_wavelength(peak_x_positions):
    x = np.asarray(peak_x_positions, dtype=float)
    differences = np.diff(x[np.isfinite(x)])
    return float(np.mean(np.abs(differences))) if differences.size else np.nan


def calculate_wave_speed(frequency, wavelength):
    return frequency * wavelength


def calculate_swim_velocity(time, snout_x):
    t, x = np.asarray(time, dtype=float), np.asarray(snout_x, dtype=float)
    valid = _finite(t, x)
    if valid.sum() < 2:
        return np.nan
    return float(np.polyfit(t[valid], x[valid], 1)[0])


def calculate_tail_tip_amplitude(peaks, troughs):
    peaks, troughs = np.asarray(peaks, dtype=float), np.asarray(troughs, dtype=float)
    return (
        float(np.nanmean(np.abs(peaks - troughs)) / 2)
        if peaks.size and peaks.shape == troughs.shape
        else np.nan
    )


def calculate_tail_base_amplitude(peaks, troughs):
    return calculate_tail_tip_amplitude(peaks, troughs)


def calculate_tail_lateral_velocity(tail_tip_amplitude, mean_peak_to_peak_time):
    return (
        4 * tail_tip_amplitude / mean_peak_to_peak_time
        if mean_peak_to_peak_time > 0
        else np.nan
    )


def calculate_relative_velocity(lateral_velocity, wave_speed, swim_velocity):
    return (
        lateral_velocity * ((wave_speed - swim_velocity) / wave_speed)
        if wave_speed
        else np.nan
    )


def calculate_virtual_mass(tail_diameter):
    return 1000 * (tail_diameter**2 / 4)


def calculate_tail_thrust_power(
    virtual_mass, relative_velocity, swim_velocity, lateral_velocity
):
    return (
        virtual_mass * relative_velocity * swim_velocity * lateral_velocity
        - 0.5 * virtual_mass * relative_velocity**2 * swim_velocity
    )


def calculate_mtp_frequency(number_of_cycles, start_time, end_time):
    return calculate_tail_frequency(number_of_cycles, start_time, end_time)


def calculate_mtp_amplitude(peaks, troughs):
    return calculate_tail_tip_amplitude(peaks, troughs)


def calculate_mtp_wavelength(valley_x_positions):
    return calculate_tail_wavelength(valley_x_positions)


def calculate_stroke_length(swim_velocity, mtp_frequency):
    return swim_velocity / mtp_frequency if mtp_frequency else np.nan


def calculate_power_phase_duration(peak_times, valley_times):
    values = np.asarray(valley_times) - np.asarray(peak_times)
    return float(np.nanmean(values)) if values.size else np.nan


def calculate_recovery_phase_duration(next_peak_times, valley_times):
    values = np.asarray(next_peak_times) - np.asarray(valley_times)
    return float(np.nanmean(values)) if values.size else np.nan


def calculate_phase_ratio(power_duration, recovery_duration):
    return power_duration / recovery_duration if recovery_duration else np.nan


def calculate_hindfoot_length(mtp_x, mtp_y, ankle_x, ankle_y):
    d = np.hypot(
        np.asarray(mtp_x) - np.asarray(ankle_x), np.asarray(mtp_y) - np.asarray(ankle_y)
    )
    return float(np.nanmean(d)) if np.isfinite(d).any() else np.nan


def calculate_hindfoot_angle(mtp_x, mtp_y, ankle_x, ankle_y):
    return np.arctan2(
        np.asarray(mtp_y) - np.asarray(ankle_y), np.asarray(mtp_x) - np.asarray(ankle_x)
    )


def _unwrap_finite(values):
    """Unwrap each contiguous finite segment without spreading NaNs past gaps."""
    values = np.asarray(values, dtype=float)
    result = values.copy()
    valid = np.isfinite(values)
    starts = np.flatnonzero(valid & np.r_[True, ~valid[:-1]])
    ends = np.flatnonzero(valid & np.r_[~valid[1:], True]) + 1
    for start, end in zip(starts, ends):
        result[start:end] = np.unwrap(values[start:end])
    return result


def calculate_hindfoot_angular_velocity(angle, time):
    angle, time = np.asarray(angle, dtype=float), np.asarray(time, dtype=float)
    if angle.size < 2 or time.size != angle.size:
        return np.array([], dtype=float)
    unwrapped = _unwrap_finite(angle)
    delta_angle = np.diff(unwrapped)
    delta_time = np.diff(time)
    valid = (
        np.isfinite(unwrapped[:-1])
        & np.isfinite(unwrapped[1:])
        & np.isfinite(delta_time)
        & (delta_time > 0)
    )
    velocity = np.full(delta_angle.shape, np.nan, dtype=float)
    velocity[valid] = delta_angle[valid] / delta_time[valid]
    return velocity


def calculate_kinematic_results(processed, fps, tail_diameter):
    """Return scalar kinematics for landmarks available in the processed view.

    Dorsal and lateral datasets are analyzed independently; fields that require
    absent landmarks are left out rather than estimated from another camera.
    """
    t = np.asarray(processed["time_s"], dtype=float)
    out = {"duration_s": float(t[-1] - t[0]) if t.size > 1 else np.nan}

    def get(name):
        return processed[name].to_numpy(dtype=float) if name in processed else None

    snout_x, tip_y, base_y = (
        get("SnoutTip_x_m"),
        get("TailTip_y_smooth_m"),
        get("TailBase_y_smooth_m"),
    )
    if snout_x is not None:
        out["swim_velocity_m_s"] = calculate_swim_velocity(t, snout_x)
    if tip_y is not None:
        peaks, troughs = _peaks(tip_y, fps)
        out["tail_beat_frequency_hz"] = _frequency(peaks, t)
        out["tail_tip_amplitude_m"] = _amplitude(tip_y, peaks, troughs)
        out["tail_lateral_velocity_m_s"] = (
            4 * out["tail_tip_amplitude_m"] * out["tail_beat_frequency_hz"]
            if np.isfinite(out["tail_tip_amplitude_m"])
            and np.isfinite(out["tail_beat_frequency_hz"])
            else np.nan
        )
        out["tail_wave_count"] = int(len(peaks))
    if base_y is not None:
        peaks, troughs = _peaks(base_y, fps)
        out["tail_base_amplitude_m"] = _amplitude(base_y, peaks, troughs)
    mtp_x, mtp_y, ankle_x, ankle_y = (
        get(f"{part}_{axis}_smooth_m")
        for part, axis in (("MTP", "x"), ("MTP", "y"), ("Ankle", "x"), ("Ankle", "y"))
    )
    if all(v is not None for v in (mtp_x, mtp_y, ankle_x, ankle_y)):
        angle = calculate_hindfoot_angle(mtp_x, mtp_y, ankle_x, ankle_y)
        angular_velocity = calculate_hindfoot_angular_velocity(angle, t)
        out["hindfoot_length_m"] = calculate_hindfoot_length(
            mtp_x, mtp_y, ankle_x, ankle_y
        )
        out["hindfoot_angular_velocity_mean_rad_s"] = (
            float(np.nanmean(np.abs(angular_velocity)))
            if angular_velocity.size and np.isfinite(angular_velocity).any()
            else np.nan
        )
        out["hindfoot_angular_velocity_max_rad_s"] = (
            float(np.nanmax(np.abs(angular_velocity)))
            if angular_velocity.size and np.isfinite(angular_velocity).any()
            else np.nan
        )
        out["hindfoot_angular_velocity_rad_s"] = np.r_[angular_velocity, np.nan]
        unwrapped_angle = _unwrap_finite(angle)
        angle_peaks, angle_troughs = _peaks(unwrapped_angle, fps)
        out["mtp_cycle_frequency_hz"] = _frequency(angle_peaks, t)
        out["mtp_angle_amplitude_rad"] = _amplitude(
            unwrapped_angle, angle_peaks, angle_troughs
        )
        power_durations, recovery_durations = [], []
        for peak in angle_peaks:
            later_troughs = angle_troughs[angle_troughs > peak]
            later_peaks = angle_peaks[angle_peaks > peak]
            if not later_troughs.size or not later_peaks.size:
                continue
            trough = later_troughs[0]
            next_peak = later_peaks[0]
            if trough < next_peak:
                power_durations.append(t[trough] - t[peak])
                recovery_durations.append(t[next_peak] - t[trough])
        if power_durations and recovery_durations:
            power = float(np.mean(power_durations))
            recovery = float(np.mean(recovery_durations))
            out["hindlimb_power_phase_s"] = power
            out["hindlimb_recovery_phase_s"] = recovery
            out["hindlimb_phase_ratio"] = calculate_phase_ratio(power, recovery)
        if snout_x is not None:
            out["hindfoot_stroke_length_m"] = calculate_stroke_length(
                out["swim_velocity_m_s"], out["mtp_cycle_frequency_hz"]
            )
    if np.isfinite(tail_diameter) and tail_diameter > 0:
        out["tail_diameter_m"] = float(tail_diameter)
        out["tail_virtual_mass_kg"] = calculate_virtual_mass(float(tail_diameter))
    # Drop a time-series vector from the scalar results record; it is exported with processed data instead.
    out.pop("hindfoot_angular_velocity_rad_s", None)
    return out
