#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from . import can_kinds, can_utils, can_dll_interface, can_baud_rate, can_control_structure

from ctypes import *
from . import can_utils


class CanDevice:
    # 初始化Can设备
    def __init__(self, devType=can_kinds.CAN_KIND_USBCAN_2E_U, devIndex=can_utils.DEV_INDEX_DEFAULT):
        # 引用Can的dll文件
        self.canDLL = CDLL(can_utils.ControlCan_dll_64_Path)
        self.devType = devType
        self.devIndex = devIndex
        self.canControl = can_dll_interface.VCIControl(self.canDLL)

    def can_start(self, canIndex=can_utils.CAN_INDEX_DEFAULT, baud_rate=can_baud_rate.CAN_BAUD_RATE_125):
        self.canControl.VCI_OpenDevice(self.devType, self.devIndex)

        self.canControl.VCI_SetReference(self.devType, self.devIndex, canIndex,
                                         can_utils.VCI_SETREFERENCE_REFTYPE_DEFAULT,
                                         baud_rate)

        self.canControl.VCI_InitCAN(self.devType, self.devIndex, canIndex,
                                    can_control_structure.CanControlStructure().VCI_INIT_CONFIG(baud_rate))

        return self.canControl.VCI_StartCAN(self.devType, self.devIndex, canIndex)

    def can_close(self):
        return self.canControl.VCI_CloseDevice(self.devType, self.devIndex)
