#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
    MCC 134 HAT Temp reader

    Purpose:
        Read temp values from raspi hat and push to influxdb

"""

from __future__ import print_function
from time import sleep
from sys import stdout
import sys, os
#sys.path.append('/home/pi/daqhats')
from daqhats import mcc134,mcc118, OptionFlags, HatIDs, HatError, TcTypes
from daqhats_utils import select_hat_device, enum_mask_to_string, tc_type_to_string
import subprocess

db = conf["DATABASE"]
meta = conf["METADATA"]
para = conf["PARAMETERS"]

#INFLUXDB access string:
url = db["URL"]+":"+db["PORT"]+"/write?db="db["NAME"]

# Constants
CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'
OFFSET_SENS_A = 0.0
OFFSET_SENS_B = 0.0
OFFSET_SENS_C = 0.0
ped = [146.1,152.4,147.3,147.3]
kv = [0.01106,0.01098,0.01094,0.01092]


def main():
    """
    This function is executed automatically when the module is run directly.
    """
    tc_type = TcTypes.TYPE_K   # change this to the desired thermocouple type
    delay_between_reads = 2  # Seconds
    channels_tc = {0}
    channels_adc = {0,1,2,3}

    db_ip  = "130.92.128.162"
    db_port = 8086
    db_name = "argoncube"
#For Igor's laptop
#    db_org = "LHEP"
#    db_token = "CCxlqcKlunmaW2Fv2-fPuTn1FP4HOADkjP5olYu7nzqVaX4k6lJ8q_VlE2DZ4uzTHSt3g8aYLZ6l_Ho6zKMCRg=="
#For Lane's laptop
    db_org = "lhep"
    db_token = "k_9onv1l3ko1r5PB93mYIKH3eE7MVKJtxUuNHfen3e9OXiTzESUPdQvCDnEnPgwrisWE7F1vbWBuHizCW-e9vA=="


    try:
        # Get an instance of the selected hat device object.
        address_tc = select_hat_device(HatIDs.MCC_134)
        address_adc = select_hat_device(HatIDs.MCC_118)
        #address = 0
        hat_tc = mcc134(address_tc)
        hat_adc = mcc118(address_adc)
        for channel in channels_tc:
            hat_tc.tc_type_write(channel, tc_type)

        print('    Thermocouple type: ' + tc_type_to_string(tc_type))

        print('\nAcquiring data ... Press Ctrl-C to abort')

        # Display the header row for the data table.
        print('\n  Sample', end='')
        for channel in channels_tc:
            print('       TC ', channel, end='')
        for channel in channels_adc:
            print('          V',channel, end='')
        print('')

        try:
            samples_per_channel = 0
            while True:
                # Display the updated samples per channel count
                samples_per_channel += 1
                print('\r{:8d}'.format(samples_per_channel), end='')

                # Read TCs
                for channel in channels_tc:
                    value = hat_tc.t_in_read(channel)
		    #corr = (hat_tc.cjc_read(channel)-24.3)*1.7
		    #value=value - corr + 4.5
                    #value = hat.a_in_read(channel)*1000
                    #if channel == 0:
                    #    position = "A"
                    #    value += OFFSET_SENS_A
                    
                    #subprocess.call(["curl", "-i", "-XPOST", "http://130.92.128.162:8086/write?db=singlemodule_nov2020", "--data-binary", post])
                    if value == mcc134.OPEN_TC_VALUE:
                        print('     Open     ', end='')
                    elif value == mcc134.OVERRANGE_TC_VALUE:
                        print('     OverRange', end='')
                    elif value == mcc134.COMMON_MODE_TC_VALUE:
                        print('   Common Mode', end='')
                    else:
                        print('{:12.2f} '.format(value), end='')
                        post = "HV,chan=t"+" value=" + str(value)
                        
                        subprocess.call(["curl","--request","POST",db_ip+":"+str(db_port)+"/api/v2/write?bucket="+db_name+"&org="+db_org,"-H","Authorization: Token "+db_token,"--data-binary",post])
                # Read ADC
                for channel in channels_adc:
                    value_adc = hat_adc.a_in_read(channel)
                    value_adc = value_adc*1000.-ped[channel]
                    value_adc *= kv[channel]
                    print('{:12.2f} '.format(value_adc), end='')
                    post = "HV,chan="+str(channel+1)+" value=" + str(value_adc)
                    subprocess.call(["curl","--request","POST",db_ip+":"+str(db_port)+"/api/v2/write?bucket="+db_name+"&org="+db_org,"-H","Authorization: Token "+db_token,"--data-binary",post])


                stdout.flush()

                # Wait the specified interval between reads.
                sleep(delay_between_reads)

        except KeyboardInterrupt:
            # Clear the '^C' from the display.
            print(CURSOR_BACK_2, ERASE_TO_END_OF_LINE, '\n')

    except (HatError, ValueError) as error:
        print('\n', error)


if __name__ == '__main__':
    # This will only be run when the module is called directly.
    main()
