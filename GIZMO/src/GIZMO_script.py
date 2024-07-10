import time 
from datetime import datetime
import numpy as np
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import paramiko
import warnings 
import threading
import traceback
import sys
import os
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
#from paramiko.py3compat import input

from configparser import ConfigParser
conf = ConfigParser()
conf.read("/home/pi/Dune2x2_SlowControl/config.ini")

class GIZMO():
    '''
    This class represents the template for an MPOD.
    '''
    def __init__(self):
        self.conf = ConfigParser()
        self.conf.read("config.ini")
        self.crate_status = True
        self.error_status = False

        # START CONTINUOUS MONITORING ON OBJECT CREATION
        if self.crate_status:
            threading.Thread(target=self.CONTINUOUS_monitoring, args=([]), kwargs={}).start()

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # GET METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def getOnMessage(self):
        return "Measuring impedance, magnitude, and phase."
    
    def getOffMessage(self):
        return "Turn ON/OFF GIZMO manually."

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # CONFIGURATION METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def powerSwitch(self, switch):
        return None

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # MEASURING METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def measure(self, chan):
        validation = True
        try:
            while validation:
                #time.sleep(5)
                line = chan.recv(1000).decode('ASCII').strip()
                if 'RES' == line[0:3]:
                    validation = False
    
        except Exception as e:
            print("SSH Connection Error")
        
        return line
    
    def CalculatePhase(self, qq, ii):
        '''
        Inputs:         - ii (in phase projection)
                        - qq (out of phase projection)
        Description:    Calculates arctan(qq/ii)
        '''
        return np.degrees(np.arctan(qq/ii))

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # INFLUXDB METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def INFLUX_write(self, measurement, value):
        '''
        Inputs:         - Measurement (i.e. resistance)
                        - Value (i.e. resistance value)

        Description:    Record timestamp on InfluxDB
        '''
        client = InfluxDBClient(url = self.conf["DATABASE"]["URL"]+":"+self.conf["DATABASE"]["PORT"], token = self.conf["DATABASE"]["TOKEN"], org = self.conf["DATABASE"]["ORG"])
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=self.conf["DATABASE"]["BUCKET"], record=self.dict_setup(measurement, value))
        client.close()

    def dict_setup(self, measurement, value):
        '''
        Inputs:         - Measurement (i.e. resistance)
                        - Value (i.e. resistance value)

        Outputs:        - JSON file ready to be added to InfluxDB

        Description:    Provides new timestamp ready to be added to InfluxDB
        '''
        data = {
            # Table name
            "measurement" : "gizmo", 
            # Time stamp
            "time" : datetime.utcnow().strftime('%Y%m%d %H:%M:%S'),
            # Data fields 
            "fields" : {measurement : value}
        }
        return data

    def CONTINUOUS_monitoring(self):
        '''
        Description:    Continuously record timestamp on InfluxDB
        '''
        powering_list = ["resistance","threshold","magnitude","current","charge","phase"]
        print("GIZMO Continuous DAQ Activated. Taking data in real time")
        # Setting up GIZMO client
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.conf["GIZMO"]["IP"], self.conf["GIZMO"]["PORT"], "root", "", timeout=200)
            chan = client.invoke_shell()
            chan.send('./GIZMO.elf 1\n')
        except Exception as e:
            print("Something is wrong (connection)!")
            self.crate_status = False
            self.error_status = True
            print('*** Caught exception: %s: %s' % (e.__class__, e))

        # Take data while gizmo is ON
        for powering in powering_list:
            print(f"{powering}",end="\t")
            if powering in ["current","charge"]:
                print("\t",end="")
        print("\n",end="")
        while self.crate_status:
            try:
                # Creating arrays for data 
                sampled_values = {}
                for powering in powering_list:
                    sampled_values[powering] = []
                # Record data for 5 seconds
                elapsed_time = 0
                start_time = time.time()
                while elapsed_time < 5:
                    # Measuring from gizmo
                    line = self.measure(chan)
                    if 'RES' == line[0:3]:
                        line = line.replace('(', ' ')
                        line = line.replace(')', ' ')
                        line = line.replace('= ', '=')
                        line = line.replace(', ', ' ')
                        sl = line.split() 
                        data = [float(sl[i].split('=')[1]) for i in range(0,5)]
                        data.append(0)
                        ii, qq = 0, 0
                        # Sending data to corresponding arrays
                        for powering, value in zip(powering_list, data):
                            if powering == "charge":
                                qq = value
                            if powering == "current":
                                ii = value
                            if powering == "phase":
                                value = self.CalculatePhase(qq, ii)
                            sampled_values[powering].append(value)
                    # Send data to influxDB
                    for powering in powering_list:
                        mean, RMS = np.mean(sampled_values[powering]), np.sqrt(np.mean(np.square(sampled_values[powering])))
                        print("%.2f" % mean, end="\t\t")
                        self.INFLUX_write(powering, mean)
                    print("\n",end="")
                    # Set crate status if no error
                    self.crate_status = True
                    self.error_status = False
                    # Calculate operation time
                    elapsed_time = time.time() - start_time
                    #print("ELAPSED TIME : " + str(elapsed_time))

            except Exception as e:
                print("Something is wrong (fetch data)!")
                self.crate_status = False
                self.error_status = True
                print('*** Caught exception: %s: %s' % (e.__class__, e))
                chan.close()
                client.close()
                #traceback.print_exc()
                #sys.exit(1)

if __name__ == "__main__":
    giz = GIZMO() 
