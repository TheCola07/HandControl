import cv2
import myHand as mh
import time
import myVolume as mv
import os

filePath = 'E:\pyLearn\mediapipeLearn\controll\piture'
file = os.listdir(filePath)
print(file)

overlist = []
for imlist in file:
    image = cv2.imread(f"{filePath}\{imlist}")
    overlist.append(image)

header = overlist[0]
# print(header)

cap = cv2.VideoCapture(0)   # 自己的摄像头
wCam, hCam = 1280, 720   # 视频显示窗口的宽和高
cap.set(3, wCam)    # 设置显示框的宽度
cap.set(4, hCam)    # 设置显示框的高度

def main():
    
    myhand = mh.handDetector(detectionCon=0.8, minTrackCon=0.5)
    myVol = mv.myVol()
    
    pTime = 0
    
    while True:
        success, img = cap.read()
    
        img = cv2.flip(img, flipCode=1)
        
        img[0:125, 0:1280] = header
        
        img = myhand.findHand(img)
        lmList = myhand.findPosition(img, is_draw=False)
        
        if len(lmList) != 0:
            # print(lmList)
            
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            
            fingers = myhand.fingerup()
            # print(fingers)
            
            if fingers[1] and fingers[2]:
                print("move")
            elif fingers[1]:
                print("draw")
            
        
        
        
        # img = myVol.volCon(img, lmList)
        
        # finger = myhand.fingerup(lmList)
        # print(finger)
        
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)    
        
        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF==27:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    return

if __name__ == "__main__":
    main()