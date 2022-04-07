import serial
from serial.tools import list_ports
import os
import time


class bluetooth:
    def __init__(self):
        bitrate = 9600
        ports = list_ports.comports()
        while True:
            port = [info.device for info in ports if 'Bluetooth' in info.description]
            print(port[0])
            if len(port) == 0:
                print('cannot get COM port name')
                time.sleep(0.1)
                continue
            else:
                break
        self.comport = serial.Serial(port[0], bitrate, timeout=2)
        print('success connect')

    def serial_send_data(self, dir: list, length: list):
        time.sleep(0.5)
        num_txt = str(len(dir)) + os.linesep
        print(num_txt)
        num_b = num_txt.encode('ascii')
        self.comport.write(num_b)
        self.comport.flush()
        time.sleep(0.5)
        for i in range(len(dir)):
            dir_txt = str(dir[i]) + os.linesep
            dis_txt = str(length[i]) + os.linesep
            self.comport.write(dir_txt.encode('ascii'))
            self.comport.flush()
            self.comport.write(dis_txt.encode('ascii'))
            self.comport.flush()
            time.sleep(0.1)

        # txt = str(duty) + os.linesep
        # print(txt)
        # self.comport.write(txt.encode('ascii'))

    def read_flag(self):
        # queue is empty ot not
        flag = self.comport.readline().decode('ascii')
        return int(flag.rstrip())

    def serial_close(self):
        self.comport.close()


if __name__ == '__main__':
    bt = bluetooth()
    # bt.serial_send_data(1, 3)
    dir_list = [1, 2, 4, 2, 1]
    dis_list = [3, 1, 1, 4, 5]
    for i in range(3):
        bt.serial_send_data(dir_list, dis_list)
    # flag = bt.read_flag()
    # print(flag)
    # bt.serial_close()
    bt.serial_close()
