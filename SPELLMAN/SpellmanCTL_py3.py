import socket
import sys
import os
import subprocess
import time

#INFLUXDB access string:
url = "http://130.92.128.162:8086/write?db=singlemodule_nov2020"

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
#print 'Arg1:', str(sys.argv[1])
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('130.92.128.186', 50001)
#print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    if len(sys.argv) == 1:
        print("Usage: ")
        print("python SpellmanCTL.py [CMD]")
        print(" Clear - clear fault flags, disable HV")
        print(" IsON  - returns 1 if HV is ON, 0 otherwise")
        print(" Enable  - enables HV (remote mode only)")
        print(" Disable - disables HV (remote mode only)")
        print(" GetSP_V - print set voltage")
        print(" GetSP_I - print set current limit")
        print(" GetVI - print actual voltage [kV] and current [mA]")
        print(" SetSP_V [kV] - set setpoint for voltage (remote mode only)")
        print(" SetSP_I [mA] - set current limit (remote mode only)")
        print(" OpMode - print operation mode (voltage/current limit)")
        print(" Status - prints status flags")

    elif str(sys.argv[1]) == 'IsON':     
        message = b"\x02"+b'22,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)==16: 
             val=data[9:10] 
             print(str(val))
        else: print('Error')  
    
    elif str(sys.argv[1]) == 'Clear':     
        message = b"\x02"+b'52,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)==16: 
             val=data[4:5] 
             print(str(val))
        else: print('Error')  

    elif str(sys.argv[1]) == 'Enable':     
        message = b"\x02"+b'99,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)==16: 
             val=data[4:5] 
             print(str(val))
        else: print('Error')  

    elif str(sys.argv[1]) == 'Disable':     
        message = b"\x02"+b'98,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)==16: 
             val=data[4:5] 
             print(str(val))
        else: print('Error')  
    
    elif str(sys.argv[1]) == 'GetSP_V':     
        message = b"\x02"+b'14,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)>=7 and len(data)<=20: 
#        if len(data)>=0 and len(data)<=100: 
             val=data.split(",")[1] 
             fval=50.0 / 4095 * float(str(val))
             print(str(fval))
        else: print('Error')  

    elif str(sys.argv[1]) == 'GetSP_I':     
        message = b"\x02"+b'15,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)>=7 and len(data)<=20: 
             val=data.split(",")[1] 
             fval=6.0 / 4095 * float(str(val))
             print(str(fval))
        else: print('Error')  

    elif str(sys.argv[1]) == 'GetVI':     
        message = b"\x02"+b'20,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(64))
        if len(data)>=7: 
             val=data.split(",")[9] 
             fval=50.0 / 3983 * float(str(val))
             print(str(fval))
             val=data.split(",")[2] 
             fval=6.0 / 3983 * float(str(val))
             print(str(fval))
        else: print('Error')  

    elif str(sys.argv[1]) == 'SetSP_V': 
        if len(sys.argv) == 2: 
             val=0
        else:
             val= int(float(sys.argv[2])/50.0*4095)
#        print 'Sending '+str(val)
        message = b"\x02"+b'10,' + bytes(str(val), 'utf-8') + b','+b"\x03"
#        print str(message)
        sock.sendall(message)
        data = str(sock.recv(32))
#        print str(data)
        if len(data)==16: 
             val=data[4:5] 
             print(str(val))
        else: print('Error. Works only in remote mode')  

    elif str(sys.argv[1]) == 'SetSP_I': 
        if len(sys.argv) == 2: 
             val=0
        else:
             val= int(float(sys.argv[2])/6.0*4095)
        message = b"\x02"+b'11,' + bytes(str(val),'utf-8') + b','+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)==16: 
             val=data[4:5] 
             print(str(val))
        else: print('Error. Works only in remote mode')  

    elif str(sys.argv[1]) == 'OpMode':     
        message = b"\x02"+b'69,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(64))
        if len(data)>=16: 
             val=data.split(",")[1] 
             print("Current mode " + str(val))
             val=data.split(",")[2] 
             print("Voltage mode " + str(val))
        else: print('Error')  


    elif str(sys.argv[1]) == 'Status':     
        message = b"\x02"+b'32,'+b"\x03"
        sock.sendall(message)
        data = sock.recv(32)
        if len(data)==27: 
             print(data)
             val=data[4:25]
             print(val) 
             print("Interlock OK "+str(val).split(",")[0]) 
             print("HV Inhibit (?) "+str(val).split(",")[1]) 
             print("Overvoltage  "+str(val).split(",")[2]) 
             print("Overcurrent  "+str(val).split(",")[3]) 
             print("Overpower    "+str(val).split(",")[4]) 
             print("Regulator error "+str(val).split(",")[5]) 
             print("Arcing detected "+str(val).split(",")[6]) 
             print("Overtemperature "+str(val).split(",")[7]) 
             print("Adj overload fault "+str(val).split(",")[8]) 
             print("System fault "+str(val).split(",")[9]) 
             print("Remote mode  "+str(val).split(",")[10]) 
        else: print('Error')  

    elif str(sys.argv[1]) == 'SendToDB':     
        message = b"\x02"+b'20,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(64))
        if len(data)>=7: 
             val=data.split(",")[9] 
             fval=50.0 / 3983 * float(str(val))
             print('Vmon: '+str(fval))
             FNULL = open(os.devnull, 'w')
             post = "HV,chan=HVPS_Vmon value=" + str(fval)
             subprocess.call(["curl", "-i", "-XPOST", url, "--data-binary", post], stdout=FNULL, stderr=subprocess.STDOUT)            
             val=data.split(",")[2] 
             fval=6.0 / 3983 * float(str(val))
             print('Imon: '+str(fval))
             post = "HV,chan=HVPS_Imon value=" + str(fval)
             subprocess.call(["curl", "-i", "-XPOST", url, "--data-binary", post], stdout=FNULL, stderr=subprocess.STDOUT)            
        else: print('Error')  
                
#            elif str(sys.argv[1]) == 'GetSP_V':     
        message = b"\x02"+b'14,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)>=7 and len(data)<=20: 
#        if len(data)>=0 and len(data)<=100: 
             val=data.split(",")[1] 
             fval=50.0 / 4095 * float(str(val))
             print('SP_V: '+str(fval))
             post = "HV,chan=HVPS_SP_V value=" + str(fval)
             subprocess.call(["curl", "-i", "-XPOST", url, "--data-binary", post], stdout=FNULL, stderr=subprocess.STDOUT)            
        else: print('Error')  

 #   elif str(sys.argv[1]) == 'GetSP_I':     
        message = b"\x02"+b'15,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)>=7 and len(data)<=20: 
             val=data.split(",")[1] 
             fval=6.0 / 4095 * float(str(val))
             print('SP_I: '+str(fval))
             post = "HV,chan=HVPS_SP_I value=" + str(fval)
             subprocess.call(["curl", "-i", "-XPOST", url, "--data-binary", post], stdout=FNULL, stderr=subprocess.STDOUT)            
        else: print('Error')  


        message = b"\x02"+b'22,'+b"\x03"
        sock.sendall(message)
        data = str(sock.recv(32))
        if len(data)==16: 
             val=data[9:10] 
             print('Enabled: '+str(val))
             post = "HV,chan=HVPS_ENA value=" + str(val)
             subprocess.call(["curl", "-i", "-XPOST", url, "--data-binary", post], stdout=FNULL, stderr=subprocess.STDOUT)            
        else: print('Error')  


    else: print('Unrecognized command')   
finally:
#    print >>sys.stderr, 'closing socket'
    sock.close()
