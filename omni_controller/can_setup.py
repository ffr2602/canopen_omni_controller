import time
import can
import numpy as np

CAN_ID = [0x401, 0x402, 0x403, 0x404]

class setup_can():
    def __init__(self):

        self.can_open = False
        self.motor_velocity_rpm = np.zeros(4).astype(int)
        self.motor_velocity_position = np.zeros(4).astype(int)

        try:
            self.bus = can.Bus(interface='socketcan', channel='can0', bitrate=500000)
            self.can_open = True
        except OSError:
            self.can_open = False
            exit()

    def send_data_can(self, data):
        for i in range(len(data)):
            a = hex(data[i] & 0xff)
            b = hex(data[i] >> 8 & 0xff)
            c = hex(data[i] >> 16 & 0xff)
            d = hex(data[i] >> 32 & 0xff)
            self.bus.send(can.Message(arbitration_id=CAN_ID[i], data=[0x0f, 0x00, 0x03, int(a, 16), int(b, 16), int(c, 16), int(d, 16), 0x00], is_extended_id=False))
            
    def read_speed_data_can(self):
        if self.can_open == True:   
            msg_recv = self.bus.recv()
            if msg_recv.arbitration_id == 897:
                a =  msg_recv.data[msg_recv.dlc - 6]
                b =  msg_recv.data[msg_recv.dlc - 5] * 0x100 
                c =  msg_recv.data[msg_recv.dlc - 4] * 0x10000
                d =  msg_recv.data[msg_recv.dlc - 3] * 0x1000000
                convert = a + b + c + d
                self.motor_velocity_position[0] = convert
            if msg_recv.arbitration_id == 898:
                a =  msg_recv.data[msg_recv.dlc - 6]
                b =  msg_recv.data[msg_recv.dlc - 5] * 0x100 
                c =  msg_recv.data[msg_recv.dlc - 4] * 0x10000
                d =  msg_recv.data[msg_recv.dlc - 3] * 0x1000000
                convert = a + b + c + d
                self.motor_velocity_position[1] = convert
            if msg_recv.arbitration_id == 899:
                a =  msg_recv.data[msg_recv.dlc - 6]
                b =  msg_recv.data[msg_recv.dlc - 5] * 0x100 
                c =  msg_recv.data[msg_recv.dlc - 4] * 0x10000
                d =  msg_recv.data[msg_recv.dlc - 3] * 0x1000000
                convert = a + b + c + d
                self.motor_velocity_position[2] = convert
            if msg_recv.arbitration_id == 900:
                a =  msg_recv.data[msg_recv.dlc - 6]
                b =  msg_recv.data[msg_recv.dlc - 5] * 0x100 
                c =  msg_recv.data[msg_recv.dlc - 4] * 0x10000
                d =  msg_recv.data[msg_recv.dlc - 3] * 0x1000000
                convert = a + b + c + d
                self.motor_velocity_position[3] = convert
            print(self.motor_velocity_position)


    def read_position_data_can(self):
        if self.can_open == True:
            self.bus.send(can.Message(arbitration_id=CAN_ID[0], data=[0x40, 0x63, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00], is_extended_id=False))
            msg_recv = self.bus.recv()  
            if msg_recv.arbitration_id == 1410:
                a =  msg_recv.data[msg_recv.dlc - 4]
                b =  msg_recv.data[msg_recv.dlc - 3] * 0x100 
                c =  msg_recv.data[msg_recv.dlc - 2] * 0x10000
                d =  msg_recv.data[msg_recv.dlc - 1] * 0x1000000
                data = a + b + c + d
                print(data)
    

