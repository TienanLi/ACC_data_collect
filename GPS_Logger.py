import serial
import time
import csv
import sys
from RecordGPS import UbxPacketizer,decode_packet,SolutionPacket


def write_GPS(GPS_ser,csvwriter,packetizer):
    l = GPS_ser.read(1)
    packet = packetizer.add_byte(l[0])
    if packet is not None:
        decoded_packet = decode_packet(packet)
        if type(decoded_packet) == SolutionPacket:
            t = time.time()
            # print(t)
            my_packet = decoded_packet
            csvwriter.writerow([t,  # time from record start
                                my_packet.time_of_week,  # GPS time
                                my_packet.llh_position[0],  # lat
                                my_packet.llh_position[1],  # lon
                                my_packet.llh_position[2],  # height
                                my_packet.ground_speed  # GPS_speed(m/s)
                                ])

def main(port_name):
    GPS_ser = serial.Serial(port=port_name)
    start_time = time.strftime("%d%H%M%S", time.localtime())
    outputfile = open('output' + start_time + '.csv', 'w')
    print("Writing GPS csv file...\n" + start_time)
    csvwriter = csv.writer(outputfile)
    packetizer = UbxPacketizer()
    while True:
        try:
            write_GPS(GPS_ser, csvwriter, packetizer)
        except KeyboardInterrupt:
            GPS_ser.close()
            outputfile.close()


if __name__ == "__main__":
    main(sys.argv[1])
    # main('COM3')

