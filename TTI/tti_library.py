import socket, datetime, time

default_psu_ip ='192.168.0.100' #change ip
sample_interval_secs = 2.5

class ttiPsu(object):

    def __init__(self, ip, channel=1):
        self.ip = ip
        self.port = 9221 #default port for socket control
        #channel=1 for single PSU and right hand of Dual PSU
        self.channel = channel
        self.ident_string = ''
        self.sock_timeout_secs = 4
        self.packet_end = bytes('\r\n','ascii')
        #self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.mysocket.settimeout(self.sock_timeout_secs)
        #self.mysocket.connect((self.ip, self.port))
        print('Using port', self.port)

    def send(self, cmd):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.sock_timeout_secs)
            s.connect((self.ip, self.port))
            s.sendall(bytes(cmd,'ascii'))

    def recv_end(self, the_socket):
        total_data=[]
        data=''
        while True:
            data=the_socket.recv(1024)
            if self.packet_end in data:
                total_data.append(data[:data.find(self.packet_end)])
                break
            total_data.append(data)
            if len(total_data)>1:
                #check if end_of_data was split
                last_pair=total_data[-2]+total_data[-1]
                if self.packet_end in last_pair:
                    total_data[-2]=last_pair[:last_pair.find(self.packet_end)]
                    total_data.pop()
                    break
        return b''.join(total_data)

    def send_receive_string(self, cmd):
        #print('Cmd', repr(cmd))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.sock_timeout_secs)
            s.connect((self.ip, self.port))
            s.sendall(bytes(cmd,'ascii'))
            s.sendall(bytes(cmd,'ascii'))
            data = self.recv_end(s)
        #print('Received', repr(data))
        return data.decode('ascii')
    '''
    def send_receive_string(self, cmd):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.sock_timeout_secs)
            s.connect((self.ip, self.port))
            s.sendall(bytes(cmd,'ascii'))
            data = s.recv(1024)
        #print('Received', repr(data))
        return data.decode('ascii')
    '''

    def send_receive_float(self, cmd):
        r = self.send_receive_string(cmd)
        #Eg. '-0.007V\r\n'  '31.500\r\n'  'V2 3.140\r\n'
        r=r.rstrip('\r\nVA') #Strip these trailing chars
        l=r.rsplit() #Split to array of strings
        if len(l) > 0:
            return float(l[-1]) #Convert number in last string to float
        return 0.0

    def send_receive_integer(self, cmd):
        r = self.send_receive_string(cmd)
        return int(r)

    def send_receive_boolean(self, cmd):
        if self.send_receive_integer(cmd) > 0:
            return True
        return False

    def getIdent(self):
        self.ident_string = self.send_receive_string('*IDN?')
        return self.ident_string.strip()

    def getConfig(self):
        cmd = 'CONFIG?'
        v = self.send_receive_integer(cmd)
        return v

    def getAmpRange(self):
        #Supported on PL series
        #Not supported on MX series
        r=0
        try:
            cmd = 'IRANGE{}?'.format(self.channel)
            r = self.send_receive_integer(cmd)
        except:
            pass
        #The response is 1 for Low (500/800mA) range,
        # 2 for High range (3A or 6A parallel)
        # or 0 for no response / not supported
        return r

    def setAmpRangeLow(self):
        #Supported on PL series
        #Not supported on MX series
        cmd = 'IRANGE{} 1'.format(self.channel)
        self.send(cmd)

    def setAmpRangeHigh(self):
        #Supported on PL series
        #Not supported on MX series
        cmd = 'IRANGE{} 2'.format(self.channel)
        self.send(cmd)

    def getOutputIsEnabled(self):
        cmd = 'OP{}?'.format(self.channel)
        v = self.send_receive_boolean(cmd)
        return v

    def getOutputVolts(self):
        cmd = 'V{}O?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v

    def getOutputAmps(self):
        cmd = 'I{}O?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v

    def getTargetVolts(self):
        cmd = 'V{}?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v

    def getTargetAmps(self):
        cmd = 'I{}?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v

    def getOverVolts(self):
        cmd = 'OVP{}?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v

    def getOverAmps(self):
        cmd = 'OCP{}?'.format(self.channel)
        v = self.send_receive_float(cmd)
        return v

    def setOutputEnable(self, ON):
        cmd=''
        if ON == True:
            cmd = 'OP{} 1'.format(self.channel)
        else:
            cmd = 'OP{} 0'.format(self.channel)
        self.send(cmd)

    def setTargetVolts(self, volts):
        cmd = 'V{0} {1:1.3f}'.format(self.channel, volts)
        self.send(cmd)

    def setTargetAmps(self, amps):
        cmd = 'I{0} {1:1.3f}'.format(self.channel, amps)
        self.send(cmd)

    def setLocal(self):
        cmd = 'LOCAL'
        self.send(cmd)

    def GetData(self):
        # Gather data from PSU
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.mysocket = s
            self.mysocket.settimeout(self.sock_timeout_secs)
            self.mysocket.connect((self.ip, self.port))

            dtime = datetime.datetime.now()
            identity = self.getIdent()
            out_volts = self.getOutputVolts()
            out_amps = self.getOutputAmps()
            target_volts = self.getTargetVolts()
            target_amps = self.getTargetAmps()
            is_enabled = self.getOutputIsEnabled()
            amp_range = self.getAmpRange()
            #dataset = DataToGui(True, dtime, identity,
            #                        out_volts, out_amps,
            #                        target_volts, target_amps,
            #                        is_enabled, amp_range)
            return 1

    def chooseStaticIP(self):
        cmd = 'NETCONFIG STATIC'
        self.send(cmd)


    def setStaticIP(self):
        cmd = 'IPADDR 192.168.1.42'
        self.send(cmd)

'''
#Example usage:
tti = ttiPsu('192.168.128.30', channel=2)
print(tti.getIdent())
print('Output: {0:2.2f} V'.format(tti.getOutputVolts()))
print('Output: {0:2.2f} A'.format(tti.getOutputAmps()))
print('OverV: {0:2.2f} V'.format(tti.getOverVolts()))
print('OverI: {0:2.2f} A'.format(tti.getOverAmps()))
print('Config: {}'.format(tti.getConfig()))
print('isEnabled: {}'.format(tti.getOutputIsEnabled()))
print('AmpRange: {}'.format(tti.getAmpRange()))
print('TargetV: {0:2.2f} V'.format(tti.getTargetVolts()))
print('TargetI: {0:2.2f} A'.format(tti.getTargetAmps()))
tti.setTargetVolts(3.14)
tti.setTargetAmps(1.234)
tti.setOutputEnable(True)
tti.setAmpRangeHigh()
tti.setLocal()
'''


   #tti = ttiPsu('192.168.128.30', channel=2)
