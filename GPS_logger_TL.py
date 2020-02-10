import serial



def GPS_logger():
    ser = serial.Serial('COM4')
    if not ser.is_open:
        ser.open()

    ser.write('B5 62 06 08 06 00 64 00 01 00 01 00 7A 12'.encode())
    response = ser.read()
    print(response)


if __name__ == "__main__":
    GPS_logger()
