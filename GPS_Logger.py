import serial
import time
import csv
from RecordGPS import UbxPacketizer,decode_packet,SolutionPacket


if __name__ == "__main__":
    GPS_ser = serial.Serial(port='/dev/ttyACM0')
    start_time=time.strftime("%d%H%M%S", time.localtime())
    print(start_time)
    outputfile = open('output' + start_time + '.csv', 'w')
    csvwriter = csv.writer(outputfile)
    print("Writing GPS csv file...\n")
    packetizer = UbxPacketizer()
    while True:
        try:
            l = GPS_ser.read(1)
            packet = packetizer.add_byte(l[0])
            if packet is not None:
                decoded_packet = decode_packet(packet)
                if type(decoded_packet) == SolutionPacket:
                    t = time.time()
                    # print(t)
                    my_packet = decoded_packet
                    csvwriter.writerow([t,#time from record start
                                        my_packet.time_of_week,#GPS time
                                        my_packet.llh_position[0],#lat
                                        my_packet.llh_position[1],#lon
                                        my_packet.llh_position[2],#height
                                        my_packet.ground_speed#GPS_speed(m/s)
                                        ])

        except KeyboardInterrupt:
            GPS_ser.close()
            outputfile.close()
