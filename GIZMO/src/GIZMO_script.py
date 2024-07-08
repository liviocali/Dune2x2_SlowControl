import time 
from datetime import datetime
import numpy as np
from influxdb import InfluxDBClient
import paramiko
import warnings 
import threading
import traceback
import sys
import os
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
#from paramiko.py3compat import input

conf = ConfigParser()
conf.read("/home/pi/Dune2x2_SlowControl/config.ini")

class GIZMO():
    '''
    This class represents the template for an MPOD.
    '''
    def __init__(self, module, unit, dict_unit):
        self.conf = ConfigParser()
        self.conf.read("/home/pi/Dune2x2_SlowControl/config.ini")
        self.crate_status = self.getCrateStatus()
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
        client = InfluxDBClient(host = self.conf["DATABASE"]["IP"], port = int(self.conf["DATABASE"]["PORT"]), database = self.conf["DATABASE"]["NAME"])
        client.write_points(self.JSON_setup(measurement, value))
        client.close()

    def JSON_setup(self, measurement, value):
        '''
        Inputs:         - Measurement (i.e. resistance)
                        - Value (i.e. resistance value)

        Outputs:        - JSON file ready to be added to InfluxDB

        Description:    Provides new timestamp ready to be added to InfluxDB
        '''
        json_payload = []
        data = {
            # Table name
            "measurement" : measurement, 
            # Time stamp
            "time" : datetime.utcnow().strftime('%Y%m%d %H:%M:%S'),
            # Data fields 
            "fields" : {measurement : value}
        }
        json_payload.append(data)
        return json_payload

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
            client.connect(self.conf["GIZMO"]["IP"], self.conf["GIZMO"]["PORT"], self.conf["GIZMO"]["USERNAME"], self.conf["GIZMO"]["PW"], timeout=200)
            chan = client.invoke_shell()
            chan.send('./GIZMO.elf 1\n')
        except Exception as e:
            print("Something is wrong!")
            self.crate_status = False
            self.error_status = True
            print('*** Caught exception: %s: %s' % (e.__class__, e))

        # Take data while gizmo is ON
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
                        self.INFLUX_write(powering, mean)
                    # Set crate status if no error
                    self.crate_status = True
                    self.error_status = False
                    # Calculate operation time
                    elapsed_time = time.time() - start_time
                    #print("ELAPSED TIME : " + str(elapsed_time))

            except Exception as e:
                print("Something is wrong!")
                self.crate_status = False
                self.error_status = True
                print('*** Caught exception: %s: %s' % (e.__class__, e))
                chan.close()
                client.close()
                #traceback.print_exc()
                #sys.exit(1)

if __name__ == "__main__":
    giz = GIZMO() 
