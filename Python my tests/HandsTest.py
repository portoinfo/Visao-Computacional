"""
Face Mesh Module
By: Computer Vision Zone
Website: https://www.computervision.zone/
"""

import cv2
import mediapipe as mp
import math
import serial
import time
from cvzone.HandTrackingModule import HandDetector


def processHands(img, detectorHands=None, SerialArduino = None, alreadyActivated11 = 0, alreadyActivated12 = 0, alreadyActivated21 = 0, alreadyActivated22 = 0):
	# Find hands in the current frame
	# The 'draw' parameter draws landmarks and hand outlines on the image if set to True
	# The 'flipType' parameter flips the image, making it easier for some detections
    hands, img = detectorHands.findHands(img, draw=True, flipType=True)

	# Check if any hands are detected
    if hands:
		# Information for the first hand detected
        hand1 = hands[0]  # Get the first hand detected
        lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        center1 = hand1['center']  # Center coordinates of the first hand
        handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

        # Count the number of fingers up for the first hand
        fingers1 = detectorHands.fingersUp(hand1)
        #print(f'H1 = {fingers1.count(1)}', end=" ")  # Print the count of fingers that are up

        # Calculate distance between specific landmarks on the first hand and draw it on the image
        length, info, img = detectorHands.findDistance(lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255),
                                                scale=10)
        #print("Distance betwwen hands: ", length)
        fingers1 = detectorHands.fingersUp(hands[0])
        if fingers1[0] == 0 and fingers1[1] == 1 and fingers1[2] == 1 and fingers1[3] == 1 and fingers1[4] == 1:
            if (alreadyActivated11 == 0):
                SerialArduino.write('0\n'.encode())    
                alreadyActivated11 = 1  
                print("ativou rele 1 para 4 dedos . . .")
        if fingers1[0] == 0 and fingers1[1] == 0 and fingers1[2] == 0 and fingers1[3] == 0 and fingers1[4] == 0:
            if (alreadyActivated11 == 1):
                SerialArduino.write('1\n'.encode())
                print("Desativou rele 1 para 4 dedos. . .")
                alreadyActivated11 = 0
        if fingers1[0] == 0 and fingers1[1] == 1 and fingers1[2] == 1 and fingers1[3] == 0 and fingers1[4] == 0:
            if (alreadyActivated12 == 0):
                SerialArduino.write('2\n'.encode()) 
                alreadyActivated12 = 1
                print("Ativou rele 2 para 2 dedos . . .")     
        if fingers1[0] == 0 and fingers1[1] == 0 and fingers1[2] == 0 and fingers1[3] == 0 and fingers1[4] == 0:
            if (alreadyActivated12 == 1):
                SerialArduino.write('3\n'.encode())
                alreadyActivated12 = 0
                print("Desativou rele 2 para 2 dedos. . .")

        # Check if a second hand is detected
        if len(hands) == 2:
            # Information for the second hand
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            center2 = hand2['center']
            handType2 = hand2["type"]

            # Count the number of fingers up for the second hand
            fingers2 = detectorHands.fingersUp(hand2)
            #print(f'H2 = {fingers2.count(1)}', end=" ")

            # Calculate distance between the index fingers of both hands and draw it on the image
            length, info, img = detectorHands.findDistance(lmList1[8][0:2], lmList2[8][0:2], img, color=(255, 0, 0),
                                                    scale=10)

            fingers2 = detectorHands.fingersUp(hands[1])
            if fingers2[0] == 0 and fingers2[1] == 1 and fingers2[2] == 1 and fingers2[3] == 1 and fingers2[4] == 1:
                if (alreadyActivated21 == 0):
                    SerialArduino.write('0\n'.encode())    
                    alreadyActivated21 = 1  
                    print("ativou rele 1 para 4 dedos . . .")
            if fingers2[0] == 0 and fingers2[1] == 0 and fingers2[2] == 0 and fingers2[3] == 0 and fingers2[4] == 0:
                if (alreadyActivated21 == 1):
                    SerialArduino.write('1\n'.encode())
                    print("Desativou rele 1 para 4 dedos. . .")
                    alreadyActivated21 = 0
            if fingers2[0] == 0 and fingers2[1] == 1 and fingers2[2] == 1 and fingers2[3] == 0 and fingers2[4] == 0:
                if (alreadyActivated22 == 0):
                    SerialArduino.write('2\n'.encode()) 
                    alreadyActivated22 = 1
                    print("Ativou rele 2 para 2 dedos . . .")     
            if fingers2[0] == 0 and fingers2[1] == 0 and fingers2[2] == 0 and fingers2[3] == 0 and fingers2[4] == 0:
                if (alreadyActivated22 == 1):
                    SerialArduino.write('3\n'.encode())
                    alreadyActivated22 = 0
                    print("Desativou rele 2 para 2 dedos. . .")

        #print(" ")  # New line for better readability of the printed output

    return img, alreadyActivated11, alreadyActivated12, alreadyActivated21, alreadyActivated22

def main():
    cap = cv2.VideoCapture(0)

    conectado = False
    porta = 'COM4'
    velocidadeBaud = 115200

    try: 
        SerialArduino = serial.Serial(porta, velocidadeBaud, timeout=0.5)
        conectado = True
    except serial.SerialException as e: 
        print("Erro ao conectar. Verifique a porta " + porta + " serial ou religue o Arduino", e)
        SerialArduino = None


# Initialize the HandDetector class with the given parameters
    detectorHands = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

    alreadyActivated11 = 0
    alreadyActivated12 = 0
    alreadyActivated21 = 0
    alreadyActivated22 = 0
    
    while True:
        success, img = cap.read()


        img, alreadyActivated11, alreadyActivated12, alreadyActivated21, alreadyActivated22 = processHands(img, detectorHands, SerialArduino, alreadyActivated11, alreadyActivated12, alreadyActivated21, alreadyActivated22)

		# show camera image with defined points
        cv2.imshow("Image", img)

        # Wait for 1 millisecond to check for any user input, keeping the window open
        cv2.waitKey(1)


if __name__ == "__main__":
    main()