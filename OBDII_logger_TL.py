#use python 3 because of the obd package
# -*- coding: utf-8 -*-
import obd
import serial


def main():

    connection=obd.OBD('/dev/rfcomm0')
    obd.logger.setLevel(obd.logging.DEBUG)  # enables all debug information
    # r = connection.query(obd.commands.SPEED)
    # print(r.value.magnitude)
    r = connection.query(obd.commands.FUEL_RATE,force=True)
    print(r)
    # r = connection.query(obd.commands.RPM)
    # print(r)

if __name__ == '__main__':
    main()