#!/usr/bin/python

import time
import subprocess
from configparser import ConfigParser
from tti_library import ttiPsu
#import sys, os
#sys.path.append("/home/pi/requests-main")
#import requests

if __name__ == "__main__":

    conf = ConfigParser()
    conf.read("../config.ini")

    db = conf["DATABASE"]
    meta = conf["METADATA"]
    para = conf["PARAMETERS"]
    meta["MODULE"]
    print(para["TTIIP"])
    #tti = ttiPsu(para["TTIIP"],0)
    tti = ttiPsu('192.168.1.42',1)


    while True:
        time.sleep(float(para["CTIME"]))
        sipmbias_V = tti.getOutputVolts()
        sipmbias_I = tti.getOutputAmps()
        print("I: %1.3f \n" % (sipmbias_I))
        post = "sipmbias,module=" + str(meta["MODULE"]) + ",var=I value=" + str(sipmbias_I)
#subprocess.call(["curl","--request","POST",db_ip+":"+str(db_port)+"/api/v2/write?bucket="+db_name+"&org=lhep","-H", "Authorization: Token "+db_token,"--data-binary", post])

#            subprocess.call(["curl", "-i", "-XPOST", db_url+":"+str(db_port)+"/api/v2/write?org=lhep&bucket="+db_name,  header, post])
#subprocess.call(["curl", "-i", "-XPOST", db["URL"]+":"+str(db["PORT"])+"/write?db="+db["NAME"], "--data-binary", post])
        print("V: %1.3f \n" % (sipmbias_V))
        post = "sipmbias,module=" + str(meta["MODULE"]) + ",var=V value=" + str(sipmbias_V)
