import cv2
import myHand as mh
import function.myMouse as mm
import function.myVolume as mv
import function.myKey as mk
import numpy as np
import time

class manager:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)   # 自己的摄像头
        self.wCam=1280 # 视频显示窗口的宽和高
        self.hCam=720
        # self.plx, self.ply = 0, 0
        # self.clx, self.cly = 0, 0

        self.cap.set(3, self.wCam)    # 设置显示框的宽度
        self.cap.set(4, self.hCam)    # 设置显示框的高度
        
        self.myhand = mh.handDetector(detectionCon=0.8, minTrackCon=0.5)
        self.myVol = mv.myVol()
        self.myMou = mm.myMouse()
        self.myKeyboard = mk.myKeyBoard()
        
    
    def mainManage(self):
        pTime = 0
        
        while True:
            success, img = self.cap.read()
        
            img = cv2.flip(img, flipCode=1)
            
            img = self.myhand.findHand(img)
            lmList, bbox = self.myhand.findPositionBox(img, is_draw=True)
            
            img = self.selection(img, lmList, bbox)
            # img = self.myKeyboard.keybuttonCon(img, lmList, bbox, self.myhand)
            
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            
            cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)    
            
            
            cv2.imshow('img', img)
            if cv2.waitKey(1) & 0xFF==27:
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
        return
    
    def selection(self, img, lmList, bbox):
        finger = self.myhand.fingerup()
        
        if finger[0] == 1 and finger[1] == 1 and finger[2] == 1 and finger[3] == 0 and finger[4] == 0:
            img = self.myKeyboard.keybuttonCon(img, lmList, bbox, self.myhand)
        else:
            if finger[1] == 1 and finger[0] == 0:
                self.myMou.move(img, lmList, self.myhand)
            elif finger[0] == 1 and finger[1] == 1 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:
                img = self.myVol.volCon(img, lmList)
            
        return img