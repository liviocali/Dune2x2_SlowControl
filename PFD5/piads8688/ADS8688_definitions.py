################### CONSTANT DEFINITIONS for class ADS8688 ####################
VREF = 4.096

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


