import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.7, maxHands=2)
while True:
   success, img = cap.read()
   img = cv2.flip(img,1)
   img = detector.findHands(img)
   #lmList, bbox = detector.findPosition(img,draw=False)
   #if lmList:
   #myHandType = detector.handType()
   cv2.putText(img, 0, (50, 50),cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
   cv2.imshow('IMG', img)
   cv2.waitKey(1)