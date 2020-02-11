#use python 3 because of the obd package
# -*- coding: utf-8 -*-
import obd
import serial


def main():
    connection=obd.OBD('/dev/rfcomm0',baudrate=118400)
    while True:
        r = connection.query(obd.commands.RPM)
        print(r)

if __name__ == '__main__':
    main()