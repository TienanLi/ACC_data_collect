import serial
from UBXManager import UBXManager
import ubx_tool


def GPS_logger():
    ser = serial.Serial('COM3', 115200, timeout=None)
    manager = UBXManager(ser, debug=True)
    manager.run()




if __name__ == "__main__":
    GPS_logger()
