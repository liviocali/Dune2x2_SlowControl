#!/usr/bin/python
import time, math, json
import subprocess
import asyncio
from configparser import ConfigParser

from asyncua import Server, ua
import socket

import io
import fcntl

I2C_SLAVE=0x0703
DEV = 0x48
BUS = 1
CONF = 0x8c

class i2c:

   def __init__(self, device, bus):
      self.fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
      self.fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)
      
      # set device address
      fcntl.ioctl(self.fr, I2C_SLAVE, device)
      fcntl.ioctl(self.fw, I2C_SLAVE, device)

   def write(self, bytes):
      self.fw.write(bytes)

   def read(self, bytes):
      return self.fr.read(bytes)

   def close(self):
      self.fw.close()
      self.fr.close()

async def main():
   conf = ConfigParser()
   conf.read("/home/pi/Dune2x2_SlowControl/config.ini")

   db = conf["DATABASE"]
   meta = conf["METADATA"]
   para = conf["PARAMETERS"]
   
   #Prepare dev
   dev = i2c(DEV, BUS) # device 0x48, bus 1
   dev.write(CONF.to_bytes(1)) #set to gain 2, 15Hz sample rate, continuous acquisition
   sample=[(0,0,0)]
   
   
   #Do read
   async with s:
      while True:
         await asyncio.sleep(int(para["CTIME"]))
         value = 0.0
         for i in range(20):
            sample =  dev.read(3)
            value =value + sample[0]*256+sample[1]
            time.sleep(0.1) #10hz read on 15hz sample
         value = value / 20
         cur = value / 1506.62 -0.03 # current in mA, gain and offset calibrated
         print( value, "current: " , cur)
         post = "lm,format=raw_cur value=" + str(cur)
         #subprocess.call(["curl", "-i", "-XPOST", db["URL"]+":"+str(db["PORT"])+"/write?db="+db["NAME"], "--data-binary", post])
   
   dev.close()
   
if __name__ == "__main__":
    asyncio.run(main(), debug=True)

