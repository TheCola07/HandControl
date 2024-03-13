# 音量操作
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import cv2
import math
import numpy as np

# print(volume.GetMute())
# print(volume.GetMasterVolumeLevel())
# print(volume.GetVolumeRange())        # 音量范围-65.25 ~ 0.0
# print(volume.SetMasterVolumeLevel(0, None))

class myVol:
    def __init__(self):
        # 初始化（对音量控制）
        devices = AudioUtilities.GetSpeakers()
        self.interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        
        # 设置初始值，便于可视化
        self.vol = 0
        self.volbar = 150
        self.volpar = 0
        
        # 获取音量操作范围
        self.volRange = self.volume.GetVolumeRange()
        self.minvol = self.volRange[0]
        self.maxvol = self.volRange[1]
        
    def volCon(self, img, lmList):
        if len(lmList) != 0:
            # 获取两个手指指尖的坐标
            x1, y1 = lmList[8][1], lmList[8][2]
            x2, y2 = lmList[4][1], lmList[4][2]
            cv2.circle(img, (x1, y1), 15, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 255, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0), 3)
            cv2.circle(img, (int((x1 + x2) / 2), int((y1 + y2) / 2)), 15, (255, 255, 0), cv2.FILLED)
            
            # 使用自带函数计算两指间距
            length = math.hypot(x2 - x1, y2 - y1)
            # print(length)
            
            # 将间距映射至音量范围（假设手指指尖间距范围为50至300）
            self.vol = np.interp(length, [50, 300], [self.minvol, self.maxvol])
            self.volbar = np.interp(length, [50, 300], [400, 150])              # 显示范围
            self.volpar = np.interp(length, [50, 300], [0, 100])
            # print(self.vol)
            self.volume.SetMasterVolumeLevel(self.vol, None)    # 设置音量
            
            if length < 50:
                cv2.circle(img, (int((x1 + x2) / 2), int((y1 + y2) / 2)), 15, (0, 255, 0), 3)
        
        # 进行可视化
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(self.volbar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(self.volpar)}%', (50, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        
        return img