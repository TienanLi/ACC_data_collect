#use python 2 because of the panda package

#!/usr/bin/env python
from __future__ import print_function
import binascii
import csv
import sys
from panda import Panda
from datetime import datetime
import sys

def can_logger():

  try:
    print("Trying to connect to Panda over USB...")
    p = Panda()

  except AssertionError:
    print("USB connection failed. Trying WiFi...")

    try:
      p = Panda("WIFI")
    except:
      print("WiFi connection timed out. Please make sure your Panda is connected and try again.")
      sys.exit(0)

  try:
      # SAFETY_NOOUTPUT = 0
      # SAFETY_HONDA = 1
      # SAFETY_TOYOTA = 2
      # SAFETY_GM = 3
      # SAFETY_HONDA_BOSCH = 4
      # SAFETY_FORD = 5
      # SAFETY_CADILLAC = 6
      # SAFETY_HYUNDAI = 7
      # SAFETY_TESLA = 8
      # SAFETY_CHRYSLER = 9
      # SAFETY_TOYOTA_IPAS = 0x1335
      # SAFETY_TOYOTA_NOLIMITS = 0x1336
      # SAFETY_ALLOUTPUT = 0x1337
      # SAFETY_ELM327 = 0xE327

    p.set_safety_mode(mode=0xE327)

    outputfile = open('output'+datetime.now().strftime('%H%M%S')+'.csv', 'wb')
    csvwriter = csv.writer(outputfile)
    #Write Header


    csvwriter.writerow(['hour', 'min', 'sec', 'microsec', 'Bus', 'MessageID', 'Message', 'MessageLength','unknown_data'])
    # csvwriter.writerow(['hour', 'min', 'sec', 'microsec', 'Raw_CAN_Info'])

    print("Writing csv file output.csv. Press Ctrl-C to exit...\n")

    bus0_msg_cnt = 0
    bus1_msg_cnt = 0
    bus2_msg_cnt = 0

    Read=False
    while True:
      can_recv = p.can_recv()
      # print(can_recv)
      # csvwriter.writerow([datetime.now().strftime('%H'), datetime.now().strftime('%M'), datetime.now().strftime('%S'),
      #                     datetime.now().strftime('%f'),can_recv])

      for address, unknown_data, dat, src  in can_recv:
        if Read==False:
          if address==742:
            print(datetime.now())
            print('YESSSSSSSSSSSS!')
            Read=True
        csvwriter.writerow([datetime.now().strftime('%H'),datetime.now().strftime('%M'), datetime.now().strftime('%S'),
                            datetime.now().strftime('%f'), str(src), str(hex(address)), "0x" + binascii.hexlify(dat),
                            len(dat), str(unknown_data)])

        if src == 0:
          bus0_msg_cnt += 1
        elif src == 1:
          bus1_msg_cnt += 1
        elif src == 2:
          bus2_msg_cnt += 1

      if datetime.now().second == 0:
        Read = False
    print("Message Counts... Bus 0: " + str(bus0_msg_cnt) + " Bus 1: " + str(bus1_msg_cnt) + " Bus 2: " + str(bus2_msg_cnt), end='\r')

  except KeyboardInterrupt:
    print("\nNow exiting. Final message Counts... Bus 0: " + str(bus0_msg_cnt) + " Bus 1: " + str(bus1_msg_cnt) + " Bus 2: " + str(bus2_msg_cnt))
    outputfile.close()

if __name__ == "__main__":
  can_logger()
