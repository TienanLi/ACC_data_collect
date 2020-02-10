#use python 3 because of the obd package
# -*- coding: utf-8 -*-
import obd
import serial


from typing import List, Generator
from contextlib import contextmanager


SERVICE_01 = 0xC4 # 196
IFACE = '/dev/rfcomm0'
BAUDRATE = 9600


@contextmanager
def encodePIDs(pid_range: int) -> Generator[List[bytes], None, None]:
    try:
        if 0 > pid_range >= 0xFF:
            raise ValueError(f'Expected a value less than {0xFF}, received '
                             f'{pid_range}')
        yield list(map(lambda b: format(b, '02x').encode(), range(pid_range)))
    finally:
        pass


def main() -> None:
    """
    Create tables of PIDs.
    """
    # Generate
    # with encodePIDs(SERVICE_01) as pids, \
    #      serial.Serial(IFACE, baudrate=BAUDRATE, bytesize=8, timeout=1) as ser:
    #
    #     if not ser.writable():
    #         raise RuntimeError(f'Unable to write to serial bus {IFACE}')
    #
    #     ser.write('AL'.encode())
    #
    #     for pid in pids:
    #         if pid!=b'12':
    #             continue
    #         print(pid)
    #         ser.write(pid)
    #         response = ser.read()
    #         print(response)

    connection=obd.OBD(portstr='/dev/rfcomm0', baudrate=9600,timeout=1)

    # connection=obd.OBD()

if __name__ == '__main__':
    main()