import time
import subprocess
from configparser import ConfigParser
from mpod_library import mpodPsu
import influxdb as ifd


if __name__ == "__main__":

    # placeholder config file to define global variables
    conf = ConfigParser()
    conf.read("../config.ini") # where is this file — ask livio

    # define variables
    db = conf["DATABASE"]
    meta = conf["METADATA"]
    para = conf["PARAMETERS"]

    # initialize module #
    meta["MODULE"]

    # initialize MPOD class
    mpod = mpodPsu('192.168.196.6')

    #activation procedures
    mpod.mpodSwitch(1)
    channels = [".u0", ".u1", ".u2", ".u3", ".u100", ".u101", ".u102", ".u103", ".u104", ".u105", ".u106", ".u107"]

mpod.channelSwitch(1, ".u0")
mpod.channelSwitch(1, ".u1")
mpod.channelSwitch(1, ".u2")
mpod.channelSwitch(1, ".u3")
mpod.channelSwitch(1, ".u100")
mpod.channelSwitch(1, ".u101")
mpod.channelSwitch(1, ".u102")
mpod.channelSwitch(1, ".u103")
mpod.channelSwitch(1, ".u104")
mpod.channelSwitch(1, ".u105")
mpod.channelSwitch(1, ".u106")
mpod.channelSwitch(1, ".u107")

'''
#setting procedures
'''

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

'''
#readout loop procedures
'''

    while True:
        time.sleep(float(para["CTIME"]))
        mpodVoltage = []
        mpodCurrent = []
        # Do we want to get all voltages separately?
        for ch in channels:

            mpodVoltage.append(mpod.getVoltage(ch))
            mpodCurrent.append(mpod.getCurrent(ch))

        print("Output I: %1.3f \n" % (mpodCurrent))
        post = "current,module=" + str(meta["MODULE"]) + ",var=I value=" + str(mpodCurrent)

        subprocess.call(["curl","--request","POST",db['IP']+":"+str(db['PORT'])+"/api/v2/write?bucket="+db['NAME']+"&org=lhep","-H", "Authorization: Token "+db['TOKEN'],"--data-binary", post])

        print("Output V: %1.3f \n" % (mpodVoltage)
        post = "current,module=" + str(meta["MODULE"]) + ",var=V value=" + str(mpodVoltage)

        subprocess.call(["curl", "-i", "-XPOST", db["URL"]+":"+str(db["PORT"])+"/write?db="+db["NAME"], "--data-binary", post])
        subprocess.call(["curl", "-i", "-XPOST", db_url+":"+str(db_port)+"/api/v2/write?org=lhep&bucket="+db_name,  header, post])
