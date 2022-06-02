#!/usr/bin/python
import time, math
import subprocess

if __name__ == "__main__":

    import max31865

    db_url  = "http://130.92.128.162"
    db_port = 8086
    db_name = "singlemodule_nov2020"

    pos = "tpc1"

    misoPin = 9
    mosiPin = 10
    clkPin  = 11

    n_sens = 10

    cs0Pin = 26
    cs1Pin = 19
    cs2Pin = 13
    cs3Pin = 06
    cs4Pin = 05
    cs5Pin = 27
    cs6Pin = 17
    cs7Pin = 04
    cs8Pin = 03
    cs9Pin = 02

    utiPow = 21

    sens0 = max31865.max31865(cs0Pin,misoPin,mosiPin,clkPin)
    sens1 = max31865.max31865(cs1Pin,misoPin,mosiPin,clkPin)
    sens2 = max31865.max31865(cs2Pin,misoPin,mosiPin,clkPin)
    sens3 = max31865.max31865(cs3Pin,misoPin,mosiPin,clkPin)
    sens4 = max31865.max31865(cs4Pin,misoPin,mosiPin,clkPin)
    sens5 = max31865.max31865(cs5Pin,misoPin,mosiPin,clkPin)
    sens6 = max31865.max31865(cs6Pin,misoPin,mosiPin,clkPin)
    sens7 = max31865.max31865(cs7Pin,misoPin,mosiPin,clkPin)
    sens8 = max31865.max31865(cs8Pin,misoPin,mosiPin,clkPin)
    sens9 = max31865.max31865(cs9Pin,misoPin,mosiPin,clkPin)

    while 1:
        time.sleep(1)
        for sens in [0,1,2,3,5,6,7,8]:
            temp_C = eval('sens'+str(sens)+'.readTemp()')
            print("sens%d: %f degC\n" % (sens,temp_C))
            post = "temp,sens=" + str(sens) + ",pos=" + str(pos) + " value=" + str(temp_C)
            subprocess.call(["curl", "-i", "-XPOST", db_url+":"+str(db_port)+"/write?db="+db_name, "--data-binary", post])
    GPIO.cleanup()
