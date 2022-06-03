#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from time import sleep



import subprocess
from sys import stdout
#from daqhats import mcc134, HatIDs, HatError, TcTypes
#from daqhats_utils import select_hat_device, tc_type_to_string


from piads8688.ADS8688_definitions import *
from piads8688 import ADS8688

conf = ConfigParser()
conf.read("../../config.ini")

db = conf["DATABASE"]
meta = conf["METADATA"]
para = conf["PARAMETERS"]
 
#HV_pedestal = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
HV_pedestal = [0.022, 0.022, 0.022, 0.022, 0.022, 0.022, 0.022, 0.022 ]
HV_factor =   [9.995,10.01,10.0,9.994,10.003,10.002,10.0,10.0]

#INFLUXDB access string:
url = db["URL"]+":"+db["PORT"]+"/write?db="db["NAME"]
ads = ADS8688()

range_HV=R0 # range for HV divider inputs 0 to 5
range_TC=R4 # range for thermocouple inputs 6 and 7
#range_TC=R0 # range for thermocouple inputs 6 and 7
"""
R0             = 0x00   # Input range to -2.5/+2.5         Vref   +/- 10.24V
R1             = 0x01   # Input range to -1.25/+1.25       Vref   +/-  5.12V
R2             = 0x02   # Input range to -0.625/+0.625     Vref   +/-  2.56V
R3             = 0x03   # Input range to -0.3125/+0.3125   Vref   +/-  1.28V
R4             = 0x0B   # Input range to -0.15625/+0.15625 Vref   +/-  0.64V
R5             = 0x05   # Input range to +2.5    Vref   10.24V
R6             = 0x06   # Input range to +1.25   Vref    5.12V
R7             = 0x07   # Input range to +0.625  Vref    2.56V
R8             = 0x0F   # Input range to +0.3125 Vref    1.28V

"""

if not os.path.exists("/dev/spidev0.1"):
    raise IOError("Error: No SPI device. Check settings in /boot/config.txt")

##tc_type = TcTypes.TYPE_K   # change this to the desired thermocouple type
channels = (0, 1, 2, 3)
samples = 0


try:

#    address = select_hat_device(HatIDs.MCC_134)
#    hat = mcc134(address)
#    for channel in channels:
#       hat.tc_type_write(channel, tc_type)

    print("\033[2J\033[H") # Clear screen
    print(__doc__)
    print("\nPress CTRL-C to exit.")
    for ch in range(0,6):
        ads.set_channel_range(ch,range_HV)
    for ch in range(6,8):
        ads.set_channel_range(ch,range_TC)
    while(1):
      samples +=1
      print("\033[2J\033[H") # Clear screen
      print("Sample "+str(samples))
#ADS8688
      rawvals=ads.read_all_raw()
      print(rawvals)
      varr=[ads.V_from_raw(raw, range_HV) for raw in rawvals[0:6]]
      print("HV inputs (CH0-CH5),  V: "+str(["{0:0.3f}".format(i) for i in varr]))
      for i in range(0,6):
          post = "HV,chan="+str(i) + " value=" + str((varr[i]-HV_pedestal[i])*HV_factor[i])
          print(post)
          subprocess.call(["curl", "-i", "-XPOST", url, "--data-binary", post], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)            

      varr=[1000*ads.V_from_raw(raw, range_TC) for raw in rawvals[6:8]]
      varr=[((raw*76.1/75.0-307.5)+307)*9.9 for raw in varr[0:2]]
      print("LV inputs (CH6-CH7), mV: "+str(["{0:0.1f}".format(i) for i in varr]))

      post = "HV,chan=t0" + " value=" + str(varr[0])
      print(post)
      subprocess.call(["curl", "-i", "-XPOST", url, "--data-binary", post], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)            
      post = "HV,chan=t1" + " value=" + str(varr[1])
      print(post)
      subprocess.call(["curl", "-i", "-XPOST", url, "--data-binary", post], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)            
      
      
#MCC134
      """
      print('TC Type: '+tc_type_to_string(tc_type), end='') 
      for channel in channels:
          value = hat.t_in_read(channel)
          if value == mcc134.OPEN_TC_VALUE:
             print('     Open     ', end='')
             post = "HV,chan=t"+str(channel) + " value=-999"
          elif value == mcc134.OVERRANGE_TC_VALUE:
             print('     OverRange ', end='')
             post = "HV,chan=t"+str(channel) + " value=999"
          elif value == mcc134.COMMON_MODE_TC_VALUE:
             print('   Common Mode ', end='')
             post = "HV,chan=t"+str(channel) + " value=-555"
          else:
             print('{:12.2f} C '.format(value), end='')
             post = "HV,chan=t"+str(channel) + " value=" + '{:0.2f}'.format(value)
          print(post)
          subprocess.call(["curl", "-i", "-XPOST", url, "--data-binary", post], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)            
      """
      stdout.flush()

      sleep(para["CTIME"])

except (KeyboardInterrupt):
    print("\n"*3 + "User exit.\n")
    sys.exit(0)
