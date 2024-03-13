import cv2
import time
import numpy as np
import autopy
import pyautogui

def cornerRect(img, bbox, l=30, t=5, rt=1, colorR=(255, 0, 255), colorC=(0, 255, 0)):
    x, y, w, h = bbox
    x1, y1 = x + w, y + h
    if rt != 0:
        cv2.rectangle(img, bbox, colorR, rt)
    # Top Left  x,y
    cv2.line(img, (x, y), (x + l, y), colorC, t)
    cv2.line(img, (x, y), (x, y + l), colorC, t)
    # Top Right  x1,y
    cv2.line(img, (x1, y), (x1 - l, y), colorC, t)
    cv2.line(img, (x1, y), (x1, y + l), colorC, t)
    # Bottom Left  x,y1
    cv2.line(img, (x, y1), (x + l, y1), colorC, t)
    cv2.line(img, (x, y1), (x, y1 - l), colorC, t)
    # Bottom Right  x1,y1
    cv2.line(img, (x1, y1), (x1 - l, y1), colorC, t)
    cv2.line(img, (x1, y1), (x1, y1 - l), colorC, t)

def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]), l=20, rt=0)
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 40, y + 60), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
    
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out

class Button:
    def __init__(self, pos, text, size=[90, 90]):
        self.pos = pos
        self.text = text
        self.size = size
        
    def draw(self, img):
        posx, posy = self.pos[0], self.pos[1]
        w, h = self.size[0], self.size[1]
        cv2.rectangle(img, (posx, posy), (posx + w, posy + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, self.text, (posx + 15, posy + 65), 
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 3)
        return img
    
class KeyButton:
    def __init__(self):
        self.myButtonList = []
        self.keys = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "K", ";"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
            ["enter"]
        ]

        for i in range(len(self.keys)):
            for j, key in enumerate(self.keys[i]):
                self.myButtonList.append(Button(pos=[100 * j + 50, 100 * i + 50], text=key))

    def drawKey(self, img):
        # for it in self.myButtonList:
        #     img = it.draw(img)
        
        img = drawAll(img, self.myButtonList)
        
        return img

class myKeyBoard:
    def __init__(self):
        self.keyButton = KeyButton()
        self.finaltext = ""
        
    def keybuttonCon(self, img, lmList, bbox, myhand):
        img = self.keyButton.drawKey(img)
        if len(lmList) != 0:
            for button in self.keyButton.myButtonList:
                x, y = button.pos
                w, h = button.size
                
                if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 15, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        
                    l, _, _ = myhand.fingerdistance(img, 8, 12)
                    
                    if l < 50:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        if len(self.finaltext) < 25:
                            # self.finaltext += button.text
                            pyautogui.press(button.text)
                        time.sleep(0.15)
                    
        # cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
        # cv2.putText(img, self.finaltext, (60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 4)
        
        return img