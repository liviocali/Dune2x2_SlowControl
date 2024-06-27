#!/usr/bin/python
import time
import json
import subprocess
import asyncio
from configparser import ConfigParser
from asyncua import Server, ua
import socket
import io
import fcntl

I2C_SLAVE = 0x0703
DEV = 0x48
BUS = 1
CONF = 0x8c

class i2c:
    def __init__(self, device, bus):
        self.fr = io.open("/dev/i2c-" + str(bus), "rb", buffering=0)
        self.fw = io.open("/dev/i2c-" + str(bus), "wb", buffering=0)

        # set device address
        fcntl.ioctl(self.fr, I2C_SLAVE, device)
        fcntl.ioctl(self.fw, I2C_SLAVE, device)

    def write(self, bytes):
        self.fw.write(bytes)

    def read(self, bytes):
        return self.fr.read(bytes)

    def close(self):
        self.fw.close()
        self.fr.close()

async def read_values(dev, shared, lock):
    while True:
        value = 0.0
        for i in range(20):
            sample = dev.read(3)
            value += sample[0] * 256 + sample[1]
            await asyncio.sleep(0.1)  # 10 Hz read on 15 Hz sample
        value = value / 20
        cur = value / 1506.62 - 0.03  # current in mA, gain and offset calibrated
        async with lock:
            shared['cur'] = cur
        await asyncio.sleep(0.1)  # Small delay to prevent tight loop

async def push_values(para, db, uavar, shared, lock):
    while True:
        await asyncio.sleep(int(para["CTIME"]))
        async with lock:
            cur = shared.get('cur', 0.0)
        print("current:", cur)
        post = f"lm,format=raw_cur value={cur}"
        subprocess.call(["curl", "-i", "-XPOST", f"{db['URL']}:{db['PORT']}/write?db={db['NAME']}", "--data-binary", post])
        await uavar.write_value(cur)

async def main():
    conf = ConfigParser()
    conf.read("/home/pi/Dune2x2_SlowControl/config.ini")

    db = conf["DATABASE"]
    meta = conf["METADATA"]
    para = conf["PARAMETERS"]

    # Read device IP
    ips = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ips.connect((db["PINGIP"], 80))
    ip = ips.getsockname()[0]
    ips.close()

    # Setup OPC UA server
    s = Server()
    await s.init()
    opc_port = "4841"
    s.set_endpoint("opc.tcp://" + ip + ":" + opc_port)
    idx = await s.register_namespace("http://" + ip + ":" + opc_port)
    uaobj = await s.nodes.objects.add_object(idx, db["OPCSERVERNAME"])
    uavar = await uaobj.add_variable(idx, "sens%02d" % 1, 4)  # Assuming sens is 1 for this example
    await uavar.set_writable()

    # Prepare dev
    dev = i2c(DEV, BUS)  # device 0x48, bus 1
    dev.write(CONF.to_bytes(1, 'big'))  # set to gain 2, 15Hz sample rate, continuous acquisition

    shared = {}
    lock = asyncio.Lock()
    
    async with s:
        reader_task = asyncio.create_task(read_values(dev, shared, lock))
        writer_task = asyncio.create_task(push_values(para, db, uavar, shared, lock))
        await asyncio.gather(reader_task, writer_task)

    dev.close()

if __name__ == "__main__":
    asyncio.run(main(), debug=True)