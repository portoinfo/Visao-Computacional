import cv2
import serial
from cvzone.HandTrackingModule import HandDetector

conectado = False
porta = 'COM4'
velocidadeBaud = 115200

try: 
   SerialArduino = serial.Serial(porta, velocidadeBaud, timeout=0.5)
   conectado = True
except serial.SerialException as e: 
   print("Erro ao conectar. Verifique a porta " + porta + " serial ou religue o Arduino", e)


video = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.7)
while True:
   check, img = video.read()
   hands, img = detector.findHands(img)
   if hands:
      finges = detector.fingersUp(hands[0])
      if finges[0] == 0 and finges[1] == 1 and finges[2] == 1 and finges[3] == 0 and finges[4] == 0:
         SerialArduino.write('1\n'.encode())      
      if finges[0] == 0 and finges[1] == 0 and finges[2] == 0 and finges[3] == 0 and finges[4] == 0:
         SerialArduino.write('0\n'.encode())
   cv2.imshow('IMG', img)
   cv2.waitKey(1)