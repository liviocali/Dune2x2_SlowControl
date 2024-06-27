import io
import fcntl

I2C_SLAVE=0x0703

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

if __name__ == "__main__":

   import time

#   import struct
#   import i2c
   conf = 0x8c
   
   dev = i2c(0x48, 1) # device 0x48, bus 1
   dev.write(conf.to_bytes(1)) #set to gain 2, 15Hz sample rate, continuous acquisition
   sample=[(0,0,0)]
   while True:
      value = 0.0
      for i in range(20):
         sample =  dev.read(3)
         value =value + sample[0]*256+sample[1]
         time.sleep(0.1) #10hz read on 15hz sample
      value = value / 20
      cur = value / 1506.62 -0.03 # current in mA, gain and offset calibrated
      print( value, "current: " , cur)

   dev.close()