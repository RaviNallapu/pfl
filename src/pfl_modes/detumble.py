#!/usr/bin/env python3

import logging

from pfl_types.datagram import Msg, RequestType
from pfl_types.cmd_types import ADCSCmd, PowerCmd
from pfl_servers.fast_socket import FastSocket
from pfl_modes.base_mode import PFLMode
import numpy as np

SOCKET_PATH = '/tmp/mode/detumble'
COMMS_SOCKET_PATH = '/tmp/comms'
ADCS_SOCKET_PATH = '/tmp/adcs'
POWER_SOCKET_PATH = '/tmp/power'

logging.basicConfig(level=logging.INFO)
class Detumble(PFLMode):
    def start(self):
        # Check IMU rates
        # if low IMU
            # finish detumble 
        # if power:
            # power on mag coils
            # check receiver
            # if valid ground input
                # finish detumble
        # if timed out:
            # finish detumble
        # check_receiver
            # record telem
            # beacon

        is_tumbling = Msg(
            RequestType.COMMAND, 
            ADCSCmd.IS_TUMBLING
        ).send_and_recv(SOCKET_PATH, ADCS_SOCKET_PATH)
        
        

        if not is_tumbling:
            self.finish_detumble()

        low_power = Msg(
            RequestType.COMMAND,
            PowerCmd.LOW_POWER
        ).send_and_recv(SOCKET_PATH, POWER_SOCKET_PATH)

        if not low_power:
            detumble = Msg(
                RequestType.COMMAND,
                ADCSCmd.COILS_ON
            ).send_and_recv(SOCKET_PATH, ADCS_SOCKET_PATH)

            send_beacon = Msg(
                RequestType.COMMAND,
                CommsCmd.SEND_TLM_PKT
            ).send_and_recv(SOCKET_PATH, ADCS_SOCKET_PATH)


    def finish_detumble(self):
        get_attitude = Msg(
        RequestType.COMMAND, 
            ADCSCmd.GET_ATTITUDE
        ).send_and_recv(SOCKET_PATH, ADCS_SOCKET_PATH)
        
        get_mag_field = Msg(
        RequestType.COMMAND, 
            ADCSCmd.GET_MAG_Field
        ).send_and_recv(SOCKET_PATH, ADCS_SOCKET_PATH)
        
        
        B = get_mag_field
        q = get_attitude[0:4]
        qt = q[1:]
        qtb = np.cross(B,qt)
        w = get_attitude[4:]
        wb = np.cross(B,w)
        Kp = 0.02e-5;
        Kd = 0.02e-3;
        M = -(Kp*qtb + Kd*wb) 
        
        Msg(
        RequestType.COMMAND, 
            ADCSCmd.ACTUATE_MTORQUE
        ).send(SOCKET_PATH, ADCS_SOCKET_PATH)
        


        
        pass



if __name__ == '__main__':
    Detumble().start()


