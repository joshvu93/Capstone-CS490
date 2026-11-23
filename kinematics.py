# Imports

import numpy as np


# ================================================
# Time
# ================================================

def calculate_time(
    frame,
    fps
):

    return (
        frame
        /
        fps
    )


# ================================================
# Tail Tip Frequency
# ================================================

def calculate_tail_frequency(
    number_of_waves,
    start_time,
    end_time
):


    elapsed_time = (
        end_time
        -
        start_time
    )


    return (
        number_of_waves
        /
        elapsed_time
    )


# ================================================
# Tail Tip Wavelength
# ================================================

def calculate_tail_wavelength(
    peak_x_positions
):


    differences = np.diff(
        peak_x_positions
    )


    return np.mean(
        differences
    )


# ================================================
# Tail Wave Speed
# ================================================

def calculate_wave_speed(
    frequency,
    wavelength
):


    return (
        frequency
        *
        wavelength
    )


# ================================================
# Swimming Velocity
# ================================================

def calculate_swim_velocity(
    time,
    snout_x
):


    slope, intercept = np.polyfit(
        time,
        snout_x,
        1
    )


    return slope


# ================================================
# Tail Tip Amplitude
# ================================================

def calculate_tail_tip_amplitude(
    peaks,
    troughs
):


    return (
        np.mean(
            peaks - troughs
        )
        /
        2
    )


# ================================================
# Tail Base Amplitude
# ================================================

def calculate_tail_base_amplitude(
    peaks,
    troughs
):


    return (
        np.mean(
            peaks - troughs
        )
        /
        2
    )


# ================================================
# Tail Lateral Velocity
# ================================================

def calculate_tail_lateral_velocity(
    tail_tip_amplitude,
    mean_peak_to_peak_time
):


    return (
        4
        *
        tail_tip_amplitude
    ) / mean_peak_to_peak_time


# ================================================
# Relative Tail Velocity
# ================================================

def calculate_relative_velocity(
    lateral_velocity,
    wave_speed,
    swim_velocity
):


    return lateral_velocity * (

        (
            wave_speed
            -
            swim_velocity
        )

        /

        wave_speed
    )


# ================================================
# Virtual Mass
# ================================================

def calculate_virtual_mass(
    tail_diameter
):


    return (

        1000

        *

        (
            tail_diameter ** 2
            /
            4
        )
    )


# ================================================
# Tail Thrust Power
# ================================================

def calculate_tail_thrust_power(
    virtual_mass,
    relative_velocity,
    swim_velocity,
    lateral_velocity
):


    return (

        virtual_mass

        *

        relative_velocity

        *

        swim_velocity

        *

        lateral_velocity

    ) - (

        0.5

        *

        virtual_mass

        *

        relative_velocity ** 2

        *

        swim_velocity
    )


# ================================================
# MTP Frequency
# ================================================

def calculate_mtp_frequency(
    number_of_cycles,
    start_time,
    end_time
):


    elapsed_time = (
        end_time
        -
        start_time
    )


    return (
        number_of_cycles
        /
        elapsed_time
    )


# ================================================
# MTP Amplitude
# ================================================

def calculate_mtp_amplitude(
    peaks,
    troughs
):


    return (
        np.mean(
            peaks - troughs
        )
        /
        2
    )


# ================================================
# MTP Wavelength
# ================================================

def calculate_mtp_wavelength(
    valley_x_positions
):


    differences = np.diff(
        valley_x_positions
    )


    return np.mean(
        differences
    )


# ================================================
# Hindfoot Stroke Length
# ================================================

def calculate_stroke_length(
    swim_velocity,
    mtp_frequency
):


    return (
        swim_velocity
        /
        mtp_frequency
    )


# ================================================
# Power Phase Duration
# ================================================

def calculate_power_phase_duration(
    peak_times,
    valley_times
):


    return np.mean(
        valley_times
        -
        peak_times
    )


# ================================================
# Recovery Phase Duration
# ================================================

def calculate_recovery_phase_duration(
    next_peak_times,
    valley_times
):


    return np.mean(
        next_peak_times
        -
        valley_times
    )


# ================================================
# Phase Ratio
# ================================================

def calculate_phase_ratio(
    power_duration,
    recovery_duration
):


    return (
        power_duration
        /
        recovery_duration
    )


# ================================================
# Hindfoot Length
# ================================================

def calculate_hindfoot_length(
    mtp_x,
    mtp_y,
    ankle_x,
    ankle_y
):


    distances = np.sqrt(

        (
            mtp_x
            -
            ankle_x
        ) ** 2

        +

        (
            mtp_y
            -
            ankle_y
        ) ** 2
    )


    return np.mean(
        distances
    )


# ================================================
# Hindfoot Angle
# ================================================

def calculate_hindfoot_angle(
    mtp_x,
    mtp_y,
    ankle_x,
    ankle_y
):


    return np.arctan2(

        mtp_y
        -
        ankle_y,

        mtp_x
        -
        ankle_x
    )


# ================================================
# Hindfoot Angular Velocity
# ================================================

def calculate_hindfoot_angular_velocity(
    angle,
    time
):


    return (

        np.diff(
            angle
        )

        /

        np.diff(
            time
        )
    )