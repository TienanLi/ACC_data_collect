#!/usr/bin/python

import warnings
import struct
import GnssConstants
import bitstring
from sensor import (ExtendedObservation,
                                  EphemerisData,
                                  RawxPacket,
                                  SolutionPacket)
import serial

def decode_sfrbx(packet):
    payload = packet[6:-2]
    gnss_id = struct.unpack("B", bytes([payload[0]]))[0]
    sv_id = struct.unpack("B", bytes([payload[1]]))[0]
    freq_id = struct.unpack("B", bytes([payload[3]]))[0]
    num_words = struct.unpack("B", bytes([payload[4]]))[0]

    data_words = struct.unpack("<{}L".format(num_words), payload[8:])

    if gnss_id == 0:
        gps_words = []
        for word in data_words:
            b = bitstring.BitArray(uint=word, length=32)
            gps_words.append(b[2:26])
        return EphemerisData(gnss_id, sv_id, freq_id, gps_words)
    elif gnss_id == 6:
        glonass_string = bitstring.BitArray()
        for word in data_words:
            b = bitstring.BitArray(uint=word, length=32)
            glonass_string.append(b)
        return EphemerisData(gnss_id, sv_id, freq_id, glonass_string[0:85])


def decode_rawx(packet):
    payload = packet[6:]
    time_of_week = struct.unpack("<d", payload[0:8])[0]
    week = struct.unpack("<H", payload[8:10])[0]
    leap_seconds = struct.unpack("b", bytes([payload[10]]))[0]
    num_meas = struct.unpack("B", bytes([payload[11]]))[0]
    rec_stat = (payload[12] & 0x000000FF)

    satellite_observations = []
    for i in range(0, num_meas):
        pr_meas = struct.unpack("<d", payload[16 + 32 * i: 24 + 32 * i])[0]
        cp_meas = struct.unpack("<d", payload[24 + 32 * i: 32 + 32 * i])[0]
        do_meas = struct.unpack("<f", payload[32 + 32 * i: 36 + 32 * i])[0]
        gnss_id = struct.unpack("B", bytes([payload[36 + 32 * i]]))[0]
        sv_id = struct.unpack("B", bytes([payload[37 + 32 * i]]))[0]
        freq_id = struct.unpack("B", bytes([payload[39 + 32 * i]]))[0]
        locktime = struct.unpack("<H", payload[40 + 32 * i: 42 + 32 * i])[0]
        cno = struct.unpack("B", bytes([payload[42 + 32 * i]]))[0]
        pr_st_dev = .01 * (2 ** struct.unpack(
            "B", bytes([payload[43 + 32 * i]]))[0])
        cp_st_dev = .004 * struct.unpack(
            "B", bytes([payload[44 + 32 * i]]))[0]
        do_st_dev = .002 * (2 ** struct.unpack(
            "B", bytes([payload[45 + 32 * i]]))[0])
        trk_stat = (payload[46 + 32 * i] & 0x000000FF)

        wavelength = GnssConstants.LAMBDA_L1
        if gnss_id == 6:
            wavelength = (GnssConstants.SPEED_OF_LIGHT /
                          (1602e6 + (freq_id - 7) * 562.5e3))

        observation = ExtendedObservation(
            carrier_phase=cp_meas,
            pseudorange=pr_meas,
            doppler_shift=do_meas,
            gnss_id=gnss_id,
            sv_id=sv_id,
            freq_id=freq_id,
            locktime=locktime,
            signal_strength=cno,
            pr_st_dev=pr_st_dev,
            cp_st_dev=cp_st_dev,
            do_st_dev=do_st_dev,
            tracking_status=trk_stat,
            wavelength=wavelength
        )
        satellite_observations.append(observation)

    return RawxPacket(week, time_of_week, leap_seconds,
                      rec_stat, satellite_observations)


def decode_solution(packet):
    payload = packet[6:]
#    print('The packet is: ')
#    print(packet)
#     print('The payload is: ')
#     print(payload)
    i_tow = (struct.unpack("<L", payload[0:4])[0] / 1000)
    # year = struct.unpack("<H", payload[4:6])[0]
    # month = struct.unpack("B", bytes([payload[6]]))[0]
    # day = struct.unpack("B", bytes([payload[7]]))[0]
    #
    # hour = struct.unpack("B", bytes([payload[8]]))[0]
    # minuite = struct.unpack("B", bytes([payload[9]]))[0]
    # sec = struct.unpack("B", bytes([payload[10]]))[0]
#     valid = struct.unpack("B", bytes([payload[11]]))[0]

    # tAcc = struct.unpack("<I", payload[12:16])[0]
    # nanosecond = struct.unpack("<i", payload[16:20])[0]

    # utc_time = Time("{}-{}-{} {}:{}:{}.0".format(year, month, day,
    #                                              hour, minuite, sec))
    # whole_gps_time = int(utc_time.gps)
    # frac_gps_time = int(nanosecond)
    # fixtype = struct.unpack("B", bytes([payload[20]]))[0]
    # fixflags = struct.unpack("B", bytes([payload[21]]))[0]

    # numSV = struct.unpack("B", bytes([payload[23]]))[0]

    lon = struct.unpack("<l", payload[24:28])[0] * 1e-7
    lat = struct.unpack("<l", payload[28:32])[0] * 1e-7
    height_mean_sea_level = struct.unpack("<l", payload[36:40])[0] / 1000.0

    # velN = struct.unpack("<l", payload[48:52])[0]
    # velE = struct.unpack("<l", payload[52:56])[0]
    # velD = struct.unpack("<l", payload[56:60])[0]

    ground_speed = struct.unpack("<l", payload[60:64])[0] / 1000.0

    return SolutionPacket(
        time_of_week=i_tow,
        llh_position=[lat, lon, height_mean_sea_level],
        # ned_velocity=np.array([velN, velE, velD]),
        ground_speed=ground_speed,
        # time_accuracy=tAcc,
        # whole_gps_time=whole_gps_time,
        # frac_gps_time=frac_gps_time
    )


def create_checksum(packet):
    CK_A = 0
    CK_B = 0
    for current_byte in packet:
        CK_A += current_byte
        CK_A = (CK_A & 0x000000FF)
        CK_B += CK_A
        CK_B = (CK_B & 0x000000FF)
    return CK_A, CK_B

_PACKET_DECODERS = {
    # '0x02 0x15': decode_rawx,
    # '0x02 0x13': decode_sfrbx,
    '0x01 0x07': decode_solution
}


def decode_packet(packet):
    class_type = format(packet[2], '#004x')
    packet_id = format(packet[3], '#004x')
    command = " ".join([class_type, packet_id])
    if command in _PACKET_DECODERS:
        return _PACKET_DECODERS[command](packet)


class UbxPacketizer:

    def __init__(self):
        self._states = {
            'initial': self._initial,
            'preamble': self._preamble,
            'header': self._header,
            'payload': self._payload
        }
        self._current_state = self._states['initial']
        self._current_packet = bytearray([])
        self._payload_length = 0
        self._byte_counter = 0

    def add_byte(self, input_byte):
        return self._current_state(input_byte)

    def _initial(self, input_byte):
        if input_byte == 0xB5:
            self._current_packet = bytearray([])
            self._current_packet.append(input_byte)
            self._current_state = self._states['preamble']

        self._byte_counter = 0
        return None

    def _preamble(self, input_byte):
        if input_byte == 0x62:
            self._current_packet.append(input_byte)
            self._current_state = self._states['header']
        else:
            self._current_state = self._states['initial']
            warnings.warn("Broken UBX Packet")

        self._byte_counter = 0
        return None

    def _header(self, input_byte):
        self._current_packet.append(input_byte)
        self._byte_counter += 1
        if self._byte_counter == 4:
            packet_length_bytes = self._current_packet[-2:]
            self._payload_length = \
                struct.unpack('<h', packet_length_bytes)[0]
            self._current_state = self._states['payload']
            self._byte_counter = 0
        return None

    def _payload(self, input_byte):
        self._current_packet.append(input_byte)
        self._byte_counter += 1
        if self._byte_counter == (self._payload_length + 2):
            self._byte_counter = 0
            self._current_state = self._states['initial']
            return self._current_packet
        else:
            return None


