import time
import csv
import obd


if __name__ == "__main__":
    connection=obd.OBD('/dev/rfcomm0')
    start_time=time.strftime("%d%H%M%S", time.localtime())
    print(start_time)
    outputfile = open('output' + start_time + '.csv', 'w')
    csvwriter = csv.writer(outputfile)
    print("Writing OBD-II csv file...\n")
    while True:
        try:
            t = time.time()
            OBD_speed = connection.query(obd.commands.SPEED).value.magnitude
            OBD_max_air_flow = connection.query(obd.commands.MAF).value.magnitude
            csvwriter.writerow([t,#time from record start
                                OBD_max_air_flow,#gram/sec
                                OBD_speed#m/s
                                ])

        except KeyboardInterrupt:
            outputfile.close()
