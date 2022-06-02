# -*- coding: utf-8 -*-

import time
import struct
import wiringpi as wp
from .ADS8688_definitions import *
from . import ADS8688_default_config
"""
RPi Pins used:
23 SCLK
21 MISO
19 MOSI
12 (GP18) RST
15 (GP22) CS
40 (GP21) LED
"""

class ADS8688(object):

    def __init__(self, conf=ADS8688_default_config):
        # Set up the wiringpi object to use physical pin numbers
        wp.wiringPiSetupPhys()
        # Config and initialize the SPI and GPIO pins used by the ADC.
        # The following four entries are actively used by the code:
        self.SPI_CHANNEL  = conf.SPI_CHANNEL
        self.CS_PIN       = conf.CS_PIN
        self.LED_PIN       = conf.LED_PIN
        # GPIO Outputs. 
        for pin in (conf.CS_PIN,
                    conf.RESET_PIN, conf.LED_PIN):
            if pin is not None:
                wp.pinMode(pin, wp.OUTPUT)
                wp.digitalWrite(pin, wp.HIGH)
        wp.digitalWrite(conf.LED_PIN, wp.LOW)
        # Initialize the wiringpi SPI setup. Return value is the Linux file
        # descriptor for the SPI bus device:
        fd = wp.wiringPiSPISetupMode(
                conf.SPI_CHANNEL, conf.SPI_FREQUENCY, conf.SPI_MODE)
        if fd == -1:
            raise IOError("ERROR: Could not access SPI device file")

        self._CS_TIMEOUT_US   = int(1 + (8*1000000)/conf.CLKIN_FREQUENCY)
        # Initialise class properties
        self.v_ref         = VREF
        # Device reset for defined initial state
        self.reset()

    def _chip_select(self):
        # If chip select hardware pin is connected to SPI bus hardware pin or
        # hardwired to GND, do nothing.
        if self.CS_PIN is not None:
            wp.digitalWrite(self.CS_PIN, wp.LOW)

    # Release chip select and implement  timeout
    def _chip_release(self):
        wp.delayMicroseconds(self._CS_TIMEOUT_US)
        wp.digitalWrite(self.CS_PIN, wp.HIGH)

    def LED_ctl(self, lead_on):
        if self.LED_PIN is not None:
            if lead_on == 0:
               wp.digitalWrite(self.LED_PIN, wp.LOW)  
            else:
               wp.digitalWrite(self.LED_PIN, wp.HIGH)  
       
    def read_reg(self, register):
        """Returns data byte from the specified register
        
        Argument: register address
        """
        self._chip_select()
        wp.wiringPiSPIDataRW(self.SPI_CHANNEL, ((register << 1) | 0x00).to_bytes(1,'big') )
        wp.wiringPiSPIDataRW(self.SPI_CHANNEL, b"\x00")
        _,data = wp.wiringPiSPIDataRW(self.SPI_CHANNEL, b"\x00")
        self._chip_release()
        return int.from_bytes(data, "big", signed=False)


    def write_reg(self, register, data):
        """Writes data byte to the specified register
        Arguments: register address, data byte (uint_8)
        """
        self._chip_select()
        wp.wiringPiSPIDataRW(self.SPI_CHANNEL, ((register << 1) | 0x01).to_bytes(1,'big'))
        wp.wiringPiSPIDataRW(self.SPI_CHANNEL, data.to_bytes(1,'big'))
        wp.wiringPiSPIDataRW(self.SPI_CHANNEL, b"\x00")
        # Release chip select and implement  timeout
        self._chip_release()

    def write_cmd(self, data):
        """Writes data byte to the command register
        Arguments: cmd data byte (uint_8)
        """
        ret = [0,0]
        self._chip_select()
        wp.wiringPiSPIDataRW(self.SPI_CHANNEL, data.to_bytes(1,'big'))
        wp.wiringPiSPIDataRW(self.SPI_CHANNEL, b"\x00")

        _,ret[0]=wp.wiringPiSPIDataRW(self.SPI_CHANNEL, b"\x00")
        _,ret[1]=wp.wiringPiSPIDataRW(self.SPI_CHANNEL, b"\x00")

        # Release chip select and implement  timeout
        self._chip_release()
        return ret

    def standby(self):
        self.write_cmd(STDBY)


    def wakeup(self):
        self.write_cmd(NO_OP)


    def reset(self):
        self.write_cmd(RST)

    def read_oneshot_raw(self, channel):
        self.LED_ctl(1)
        self.write_cmd((channel<<2) | 0xC0)
        ret=self.write_cmd(NO_OP)
        ints=[int.from_bytes(item, 'big') for item in ret]
        int16_result=(ints[1]+256*ints[0])
        self.LED_ctl(0)
        return int16_result

    def set_channel_range(self, channel, rge):
        self.write_reg(5+channel, rge)         


    def read_all_raw(self):
        ret=[]
        for ch in range(0,8):
            ret.append(self.read_oneshot_raw(ch))
        return ret

    def V_from_raw(self,raw, rge):
        switcher = {
        R0: [0x8000,10.24/32768],
        R1: [0x8000,5.12/32768],
        R2: [0x8000,2.56/32768],
        R3: [0x8000,1.28/32768],
        R4: [0x8000,0.64/32768],
        R5: [0x0,10.24/65536],
        R6: [0x0,5.12/65536],
        R7: [0x0,2.56/65536],
        R8: [0x0,1.28/65536],
        }
        fctrs=switcher.get(rge, [0x0,10.24/32768])
        V=(raw-fctrs[0])*fctrs[1]
        return V



