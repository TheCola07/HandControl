import cv2
import math
import numpy as np
import autopy
import pyautogui
import time

class myMouse:
    def __init__(self, 
                 smoothening=5, 
                 wCam=1280, # 视频显示窗口的宽和高
                 hCam=720,
                 frameR = 100):
        
        self.smoothening = smoothening
        self.wCam = wCam
        self.hCam = hCam
        self.frameR = frameR
        self.wScr, self.hScr = autopy.screen.size()   # 获取屏幕实际长宽高
        
        self.plx = 0
        self.ply = 0
        self.clx = 0
        self.cly = 0
        
        self.dragflag = 0
    
    def move(self, img, lmList, myhand):
        cv2.rectangle(img, (self.frameR, self.frameR), 
                      (self.wCam - self.frameR, self.hCam - self.frameR), 
                      (255, 255, 0), 3)
        
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            
            fingers = myhand.fingerup()
            # print(finger)
            
            if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                
                cv2.circle(img, (x1, y1), 15, (255, 255, 0), cv2.FILLED)
                
                x3 = np.interp(x1, (self.frameR, self.wCam - self.frameR), (0, self.wScr))
                y3 = np.interp(y1, (self.frameR, self.hCam - self.frameR), (0, self.hScr))
                
                self.clx = self.plx + (x3 - self.plx) / self.smoothening
                self.cly = self.ply + (y3 - self.ply) / self.smoothening
                
                autopy.mouse.move(self.clx, self.cly)
                
                # pyautogui.move(self.clx, self.cly)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                self.plx, self.ply = self.clx, self.cly
                
                
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                length, img, _ = myhand.fingerdistance(img, 8, 12)
                print(length)
                if length < 40:
                    autopy.mouse.click()
                    # pyautogui.click(interval=0.1, duration=3.0)
            
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                length, img, _ = myhand.fingerdistance(img, 8, 16)
                print(length)
                if length < 80:
                    self.dragflag = (self.dragflag + 1) % 2
                    time.sleep(0.6)
                        
                    if self.dragflag == 0:
                        # pyautogui.mouseUp(x3, y3)
                        autopy.mouse.toggle(None,False)
                    else:
                        autopy.mouse.toggle(None,True)
                        # pyautogui.mouseDown(x3, y3) 
                        
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                length, img, _ = myhand.fingerdistance(img, 8, 20)
                print(length)
                if length < 100:
                    
                    cv2.circle(img, (x1, y1), 15, (255, 255, 0), cv2.FILLED)
                
                    x3 = np.interp(x1, (self.frameR, self.wCam - self.frameR), (0, self.wScr))
                    y3 = np.interp(y1, (self.frameR, self.hCam - self.frameR), (0, self.hScr))
                    
                    self.clx = self.plx + (x3 - self.plx) / self.smoothening
                    self.cly = self.ply + (y3 - self.ply) / self.smoothening
                    
                    if abs(self.cly - self.ply) < 20:
                        if self.cly - self.ply < 0:
                            pyautogui.scroll(+50)
                        elif self.cly - self.ply > 0:
                            pyautogui.scroll(-50)
                    
                    # pyautogui.move(self.clx, self.cly)
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    self.plx, self.ply = self.clx, self.cly
                    
                