# -*- coding: utf-8 -*-
from .ADS8688_definitions import *
################  Raspberry Pi Physical Interface Properties  #################
# SPI bus configuration and GPIO pins used for the ADS1255/ADS8688.
# These defaults are used by the constructor of the ADS8688 class.
#
# To create multiple class instances for more than one AD converter, a unique
# configuration must be specified as argument for each instance.
#
# The following pins are compatible
# with the Waveshare High Precision AD/DA board on the Raspberry Pi 2B and 3B
#
# SPI_CHANNEL corresponds to the chip select hardware pin controlled by the
# SPI hardware. For the Waveshare board this pin is not even connected, so this
# code does not use hardware-controlled CS and this is a don't care value.
# FIXME: Implement hardware chip select as an option.
SPI_CHANNEL   = 1
# SPI_MODE specifies clock polarity and phase; MODE=1 <=> CPOL=0, CPHA=1
SPI_MODE      = 1
# SPI clock rate in Hz. The ADS8688 supports a minimum of 1/10th of the output
# sample data rate in Hz to 1/4th of the oscillator CLKIN_FREQUENCY which
# results in a value of 1920000 Hz for the Waveshare board. However, since
# the Raspberry pi only supports power-of-two fractions of the 250MHz system
# clock, the closest value would be 1953125 Hz, which is slightly out of spec
# for the ADS8688. Choosing 250MHz/256 = 976563 Hz is a safe choice.
SPI_FREQUENCY = 976563

CS_PIN      = 15 
RESET_PIN   = 12
LED_PIN     = 40

###############################################################################

##################  ADS8688 Constant Configuration Settings  ###################
# Seconds to wait in case DRDY pin is not connected or the chip
# does not respond. See table 21 of ADS8688 datasheet: When using a
# sample rate of 2.5 SPS and issuing a self calibration command,
# the timeout can be up to 1228 milliseconds:
#DRDY_TIMEOUT    = 2
# Optional delay in seconds to avoid busy wait and reduce CPU load when
# polling the DRDY pin. Default is 0.000001 or 1 µs (timing not accurate)
#DRDY_DELAY      = 0.000001
# Master clock rate in Hz. Default is 7680000:
CLKIN_FREQUENCY = 7680000
################################################################################


# All following settings are accessible through ADS8688 class properties

##############  ADS8688 Default Runtime Adjustable Properties  #################
range_flag = R0
################################################################################

####################  ADS8688 Default Register Settings  #######################

################################################################################
"""
################### CONSTANT DEFINITIONS for class ADS8688 ####################

#COMMAND REGISTER MAP --------------------------------------------------------------------------------------------

NO_OP      = 0x00  # Continue operation in previous mode
STDBY      = 0x82  # Device is placed into standby mode
PWR_DN     = 0x83  # Device is powered down
RST        = 0x85  # Program register is reset to default
AUTO_RST   = 0xA0  # Auto mode enabled following a reset
MAN_Ch_0   = 0xC0  # Channel 0 input is selected
MAN_Ch_1   = 0xC4  # Channel 1 input is selected
MAN_Ch_2   = 0xC8  # Channel 2 input is selected
MAN_Ch_3   = 0xCC  # Channel 3 input is selected
MAN_Ch_4   = 0xD0  # Channel 4 input is selected
MAN_Ch_5   = 0xD4  # Channel 5 input is selected
MAN_Ch_6   = 0xD8  # Channel 6 input is selected
MAN_Ch_7   = 0xDC  # Channel 7 input is selected
MAN_AUX    = 0xE0  # AUX channel input is selected

# PROGRAM REGISTER MAP -------------------------------------------------------------------------------------------

# AUTO SCAN SEQUENCING CONTROL
AUTO_SEQ_EN    = 0x01  # Auto Squencing Enable: default 0xFF - bitX to enable chX
CH_PWR_DN      = 0x02  # Channel Power Down: default 0x00 - bitX to power down chX

# DEVICE FEATURES SELECTION CONTROL
FT_SEL         = 0x03  # Feature Select: default 0x00
                            # bit 7-6 for daisy chain ID, bit 4 for ALARM feature, bit 2-0 SDO data format bits

# RANGE SELECT REGISTERS
RG_Ch_0        = 0x05   # Channel 0 Input Range: default 0x00 - bit 3-0 to select range
RG_Ch_1        = 0x06   # Channel 1 Input Range: default 0x00 - bit 3-0 to select range
RG_Ch_2        = 0x07   # Channel 2 Input Range: default 0x00 - bit 3-0 to select range
RG_Ch_3        = 0x08   # Channel 3 Input Range: default 0x00 - bit 3-0 to select range
RG_Ch_4        = 0x09   # Channel 4 Input Range: default 0x00 - bit 3-0 to select range
RG_Ch_5        = 0x0A   # Channel 5 Input Range: default 0x00 - bit 3-0 to select range
RG_Ch_6        = 0x0B   # Channel 6 Input Range: default 0x00 - bit 3-0 to select range
RG_Ch_7        = 0x0C   # Channel 7 Input Range: default 0x00 - bit 3-0 to select range

# ALARM FLAG REGISTERS (Read-only)
ALARM_OVERVIEW           = 0x10 # ALARM Overview Tripped Flag
ALARM_CH0_TRIPPED_FLAG   = 0x11 # ALARM Ch 0-3 Tripped-Flag
ALARM_CH0_ACTIVE_FLAG    = 0x12 # ALARM Ch 0-3 Active-Flag
ALARM_CH4_TRIPPED_FLAG   = 0x13 # ALARM Ch 4-7 Tripped-Flag
ALARM_CH4_ACTIVE_FLAG    = 0x14 # ALARM Ch 4-7 Active-Flag

# ALARM THRESHOLD REGISTERS
CH0_HYST       = 0x15   # Ch 0 Hysteresis
CH0_HT_MSB     = 0x16   # Ch 0 High Threshold MSB
CH0_HT_LSB     = 0x17   # Ch 0 High Threshold LSB
CH0_LT_MSB     = 0x18   # Ch 0 Low Threshold MSB
CH0_LT_LSB     = 0x19   # Ch 0 Low Threshold LSB
#... CHx register address are Ch0 + 5x

# COMMAND READ BACK (Read-Only)
CMD_READBACK   = 0x3F   # Command Read Back

# SPECIFIC VALUES -------------------------------------------------------------------------------------------

#RANGE SELECTION
R0             = 0x00   # Input range to -2.5/+2.5         Vref   +/- 10.24V
R1             = 0x01   # Input range to -1.25/+1.25       Vref   +/-  5.12V
R2             = 0x02   # Input range to -0.625/+0.625     Vref   +/-  2.56V
R3             = 0x03   # Input range to -0.3125/+0.3125   Vref   +/-  1.28V
R4             = 0x0B   # Input range to -0.15625/+0.15625 Vref   +/-  0.64V
R5             = 0x05   # Input range to +2.5    Vref   10.24V
R6             = 0x06   # Input range to +1.25   Vref    5.12V
R7             = 0x07   # Input range to +0.625  Vref    2.56V
R8             = 0x0F   # Input range to +0.3125 Vref    1.28V

# OPERATION MODES
MODE_IDLE        = 0
MODE_RESET       = 1
MODE_STANDBY     = 2
MODE_POWER_DN    = 3
MODE_PROG        = 4
MODE_MANUAL      = 5
MODE_AUTO        = 6
MODE_AUTO_RST    = 7
"""
