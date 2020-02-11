import serial
import time
import csv
import obd
from RecordGPS import UbxPacketizer,decode_packet,SolutionPacket


if __name__ == "__main__":
    GPS_ser = serial.Serial(port='/dev/ttyACM0')
    connection=obd.OBD('/dev/rfcomm0')

    outputfile = open('output' + time.strftime("%H%M%S", time.localtime()) + '.csv', 'w')
    csvwriter = csv.writer(outputfile)
    print("Writing csv file...\n")
    packetizer = UbxPacketizer()
    startTime = time.time()
    while True:
        try:
            l = GPS_ser.read(1)
            packet = packetizer.add_byte(l[0])
            if packet is not None:
                decoded_packet = decode_packet(packet)
                t = time.time() - startTime
                if type(decoded_packet) == SolutionPacket:
                    my_packet = decoded_packet
                    OBD_speed = connection.query(obd.commands.SPEED).value.to('mps').magnitude
                    OBD_fuel_rate = connection.query(obd.commands.FUEL_RATE).value.magnitude
                    OBD_max_air_flow = connection.query(obd.commands.MAF).value.magnitude

                    csvwriter.writerow([t,#time from record start
                                        my_packet.time_of_week,#GPS time
                                        my_packet.llh_position[0],#lat
                                        my_packet.llh_position[1],#lon
                                        my_packet.llh_position[2],#height
                                        my_packet.ground_speed,#GPS_speed(m/s)
                                        OBD_fuel_rate,#liter/hour
                                        OBD_max_air_flow,#gram/sec
                                        OBD_speed#m/s
                                        ])

        except KeyboardInterrupt:
            GPS_ser.close()
            outputfile.close()
