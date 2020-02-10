from typing import NamedTuple, Tuple
import numpy as np
import bitstring

ExtendedObservation = NamedTuple(
    'ExtendedObservation', [
        ('carrier_phase', float),
        ('pseudorange', float),
        ('doppler_shift', float),
        ('gnss_id', int),
        ('sv_id', int),
        ('freq_id', int),
        ('locktime', int),
        ('signal_strength', float),
        ('pr_st_dev', float),
        ('cp_st_dev', float),
        ('do_st_dev', float),
        ('tracking_status', int),
        ('wavelength', float)
    ]
)

RawxPacket = NamedTuple(
    'RawxPacket', [
        ('week_number', int),
        ('time_of_week', float),
        ('leap_seconds', int),
        ('rec_stat', int),
        ('satellite_observations', Tuple[ExtendedObservation])
    ]
)

SolutionPacket = NamedTuple(
    'SolutionPacket', [
        ('time_of_week', float),
        ('llh_position', np.ndarray),
        ('ned_velocity', np.ndarray),
        ('ground_speed', float),
        ('time_accuracy', float),
        ('whole_gps_time', int),
        ('frac_gps_time', int)
    ]
)

SimpleSolutionPacket = NamedTuple(
    'SimpleSolutionPacket', [
        ('time_of_week', float),
        ('llh_position', np.ndarray),
        ('ground_speed', float)
    ]
)

EphemerisData = NamedTuple(
    'EphemerisData', [
        ('gnss_id', int),
        ('sv_id', int),
        ('freq_id', int),
        ('raw_eph', Tuple[bitstring.BitArray])
    ]
)