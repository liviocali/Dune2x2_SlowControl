from pysnmp.hlapi import *
import os




class mpodPsu():

    def __init__(self, ip = "192.168.196.6", miblib='./mibs/'):
        self.ip = ip
        self.miblib = miblib

# Power switches

    def mpodSwitch(self, switch):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip + " sysMainSwitch.0 i " + str(switch))

    def channelSwitch(self, switch, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip + " outputSwitch" + channel + " i " + str(switch))

# Get commands:

    def getStatus(self, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip + " outputStatus" + channel)
        ret = data.read().split('\n')

        return ret

    def getVoltage(self, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip + " outputVoltage" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]

    def getCurrent(self, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip + " outputCurrent" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]

# Set commands:

    def setCurrent(self, I, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip + " outputCurrent" + channel + " F " + str(I))

    def setVoltage(self, V, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip + " outputVoltage" + channel + " F " + str(V))

    def setMaxCurrent(self, I, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip + " outputSupervisionMaxCurrent" + channel + " F " + str(I))

    def setMaxVoltage(self, V, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip + " outputSupervisionMaxTerminalVoltage" + channel + " F " + str(V))

    def setMaxPower(self, P, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip + " outputSupervisionMaxPower" + channel + " F " + str(P))

    def setVoltageRiseRate(self, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip + " outputVoltageRiseRate" + channel + " F " + str(rate))

    def setVoltageFallRate(self, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip + " outputVoltageFallRate" + channel + " F " + str(rate))

    def setCurrentRiseRate(self, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip + " outputCurrentRiseRate" + channel + " F " + str(rate))

    def setCurrentFallRate(self, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip + " outputCurrentFallRate" + channel + " F " + str(rate))

    def setMaxCurrentTripTime(self, delay, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip + " outputTripTimeMaxCurrent" + channel + " i " + str(delay))

# Example commands:

# Initialize MPOD class

mpod = mpodPsu()

# Switch MPOD on/off
mpod.mpodSwitch(1)

# Get the channel status
print(mpod.getStatus(".u0"))
print(mpod.getStatus(".u1"))
print(mpod.getStatus(".u2"))
print(mpod.getStatus(".u3"))
print(mpod.getStatus(".u100"))
print(mpod.getStatus(".u101"))
print(mpod.getStatus(".u102"))
print(mpod.getStatus(".u103"))
print(mpod.getStatus(".u104"))
print(mpod.getStatus(".u105"))
print(mpod.getStatus(".u106"))
print(mpod.getStatus(".u107"))

# Switch specific channel on
mpod.channelSwitch(1, ".u3")

# Set currents
mpod.setCurrent(2.5, ".u0")
mpod.setCurrent(2.5, ".u1")
mpod.setCurrent(2.5, ".u2")
mpod.setCurrent(2.5, ".u3")
mpod.setCurrent(0.5, ".u100")
mpod.setCurrent(0.5, ".u101")
mpod.setCurrent(0.5, ".u102")
mpod.setCurrent(0.5, ".u103")
mpod.setCurrent(0.5, ".u104")
mpod.setCurrent(0.5, ".u105")
mpod.setCurrent(0.5, ".u106")
mpod.setCurrent(0.5, ".u107")

# Set voltages
mpod.setVoltage(24, ".u0")
mpod.setVoltage(24, ".u1")
mpod.setVoltage(24, ".u2")
mpod.setVoltage(24, ".u3")
mpod.setVoltage(12, ".u100")
mpod.setVoltage(12, ".u101")
mpod.setVoltage(12, ".u102")
mpod.setVoltage(12, ".u103")
mpod.setVoltage(12, ".u104")
mpod.setVoltage(12, ".u105")
mpod.setVoltage(12, ".u106")
mpod.setVoltage(12, ".u107")

# Set max voltage
mpod.setMaxVoltage(30, ".u0")
mpod.setMaxVoltage(30, ".u1")
mpod.setMaxVoltage(30, ".u2")
mpod.setMaxVoltage(30, ".u3")
mpod.setMaxVoltage(30, ".u100")
mpod.setMaxVoltage(30, ".u101")
mpod.setMaxVoltage(30, ".u102")
mpod.setMaxVoltage(30, ".u103")
mpod.setMaxVoltage(30, ".u104")
mpod.setMaxVoltage(30, ".u105")
mpod.setMaxVoltage(30, ".u106")
mpod.setMaxVoltage(30, ".u107")

# Set max current
mpod.setMaxCurrent(5, ".u0")
mpod.setMaxCurrent(5, ".u1")
mpod.setMaxCurrent(5, ".u2")
mpod.setMaxCurrent(5, ".u3")
mpod.setMaxCurrent(2.5, ".u100")
mpod.setMaxCurrent(2.5, ".u100")
mpod.setMaxCurrent(2.5, ".u101")
mpod.setMaxCurrent(2.5, ".u102")
mpod.setMaxCurrent(2.5, ".u103")
mpod.setMaxCurrent(2.5, ".u104")
mpod.setMaxCurrent(2.5, ".u105")
mpod.setMaxCurrent(2.5, ".u106")
mpod.setMaxCurrent(2.5, ".u107")

# Set max power
mpod.setMaxPower(100, ".u0")
mpod.setMaxPower(100, ".u1")
mpod.setMaxPower(100, ".u2")
mpod.setMaxPower(100, ".u3")
mpod.setMaxPower(50, ".u100")
mpod.setMaxPower(50, ".u101")
mpod.setMaxPower(50, ".u102")
mpod.setMaxPower(50, ".u103")
mpod.setMaxPower(50, ".u104")
mpod.setMaxPower(50, ".u105")
mpod.setMaxPower(50, ".u106")
mpod.setMaxPower(50, ".u107")

# Print some voltages and currents for the first 12 channels
print('Output: ' + str(mpod.getVoltage(".u0")) + ' V')
print('Output: ' + str(mpod.getVoltage(".u1")) + ' V')
print('Output: ' + str(mpod.getVoltage(".u2")) + ' V')
print('Output: ' + str(mpod.getVoltage(".u3")) + ' V')
print('Output: ' + str(mpod.getVoltage(".u100")) + ' V')
print('Output: ' + str(mpod.getVoltage(".u101")) + ' V')
print('Output: ' + str(mpod.getVoltage(".u102")) + ' V')
print('Output: ' + str(mpod.getVoltage(".u103")) + ' V')
print('Output: ' + str(mpod.getVoltage(".u104")) + ' V')
print('Output: ' + str(mpod.getVoltage(".u105")) + ' V')
print('Output: ' + str(mpod.getVoltage(".u106")) + ' V')
print('Output: ' + str(mpod.getVoltage(".u107")) + ' V')

print('Output: ' + str(mpod.getCurrent(".u0")) + ' A')
print('Output: ' + str(mpod.getCurrent(".u1")) + ' A')
print('Output: ' + str(mpod.getCurrent(".u2")) + ' A')
print('Output: ' + str(mpod.getCurrent(".u3")) + ' A')
print('Output: ' + str(mpod.getCurrent(".u100")) + ' A')
print('Output: ' + str(mpod.getCurrent(".u101")) + ' A')
print('Output: ' + str(mpod.getCurrent(".u102")) + ' A')
print('Output: ' + str(mpod.getCurrent(".u103")) + ' A')
print('Output: ' + str(mpod.getCurrent(".u104")) + ' A')
print('Output: ' + str(mpod.getCurrent(".u105")) + ' A')
print('Output: ' + str(mpod.getCurrent(".u106")) + ' A')
print('Output: ' + str(mpod.getCurrent(".u107")) + ' A')


















