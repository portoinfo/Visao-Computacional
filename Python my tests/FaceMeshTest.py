"""
Face Mesh Module
By: Computer Vision Zone
Website: https://www.computervision.zone/
"""

import cv2
import mediapipe as mp
import math
import serial
from cvzone.HandTrackingModule import HandDetector


class FaceMeshDetector:

    def __init__(self, staticMode=False, maxFaces=2, minDetectionCon=0.5, minTrackCon=0.5, initial_mouth_distance=0, initial_left_eye_distance=0):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon
        self.initial_mouth_distance = initial_mouth_distance
        self.initial_left_eye_distance = initial_left_eye_distance

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(static_image_mode=self.staticMode,
                                                 max_num_faces=self.maxFaces,
                                                 min_detection_confidence=self.minDetectionCon,
                                                 min_tracking_confidence=self.minTrackCon)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2)
        self.count=0
        self.totalMouth=0
        self.totalLeftEye=0
        self.valueToAverage = 100
        self.countLeftEyeClosed = 0
        self.countHeadBalanced = 0
        self.countMouthOpened = 0
        self.relay1AlreadyActived = 0
        self.relay2AlreadyActived = 0
        self.relay3AlreadyActived = 0
        self.totalCountClosed = 10
        self.totalCountBalanced = 10
        self.headBalancedPointOld = None
        self.horizBalanceTrigger = 70
        self.maxHeadDistance = 0

    def findFaceMesh(self, img, draw=True, SerialArduino = None):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        faces = []
        if self.results.multi_face_landmarks: 
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS,
                                               self.drawSpec, self.drawSpec)
                face = []
                for id, lm in enumerate(faceLms.landmark):
                    ih, iw, ic = img.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    point_mouth_1 = 72
                    point_mouth_2 = 84
                    point_left_eye_1 = 104
                    point_left_eye_2 = 226
                    if (point_mouth_2 > point_mouth_2):
                        point_max = point_mouth_2
                    else:
                        point_max = point_left_eye_2
                    #if (id%4 == 0):
                    if (id == point_mouth_1) or (id == point_mouth_2) or (id == point_left_eye_1) or (id == point_left_eye_2):
                        cv2.putText(img, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN,
                                 0.5, (0, 255, 0), 1)
                    face.append([x, y])
                    if (id == point_max):
						# calculate distance for lefteye points
                    	leftEyeUpPoint = face[point_left_eye_1]
                    	leftEyeDownPoint = face[point_left_eye_2]
                    	leftEyeVerticalDistance, info = self.findDistance(leftEyeUpPoint, leftEyeDownPoint)
                    	self.totalLeftEye += leftEyeVerticalDistance
                    	if (self.initial_left_eye_distance == 0) and (self.count == self.valueToAverage):
                        	self.initial_left_eye_distance = self.totalLeftEye / self.valueToAverage                        
                        	#print("leftEyeDistance: ", int(leftEyeVerticalDistance), " - initial: ", int(self.initial_left_eye_distance))
						# calculate distance for mouth_points
                    	mouthUpPoint = face[point_mouth_1]
                    	MouthDownPoint = face[point_mouth_2]
                    	mouthVerticalDistance, info = self.findDistance(mouthUpPoint, MouthDownPoint)
                    	self.totalMouth += mouthVerticalDistance
                    	if (self.initial_mouth_distance == 0) and (self.count == self.valueToAverage):
                        	self.initial_mouth_distance = self.totalMouth / self.valueToAverage    
                        	print("Aguardando gestos corporais para atuvar/desativar dispositivos . . .")
                        	#print("MouthDistance: ", int(mouthVerticalDistance), " - initial: ", int(self.initial_mouth_distance))
                    	if ((mouthVerticalDistance - self.initial_mouth_distance) > 15) and (self.initial_mouth_distance > 0):
                            self.countMouthOpened = self.countMouthOpened + 1
                            if (self.countMouthOpened == self.totalCountClosed):
                            	if (self.relay1AlreadyActived == 0):
                                	 SerialArduino.write('1\n'.encode())
                                	 self.relay1AlreadyActived = 1
                            	else:
                                	 SerialArduino.write('0\n'.encode()) 
                                	 self.relay1AlreadyActived = 0     
                            	print("A boca está aberta . . .")
                            	print("MouthDistance: ", int(mouthVerticalDistance), " - initial: ", int(self.initial_mouth_distance))
                            	#cv2.waitKey(1000)
                    	else:
                        	self.countMouthOpened = 0
                    	if ((int(self.initial_left_eye_distance) - int(leftEyeVerticalDistance)) >= 4) and (self.initial_left_eye_distance > 0):
                            self.countLeftEyeClosed = self.countLeftEyeClosed + 1
                            if (self.countLeftEyeClosed == self.totalCountClosed):
                            	if (self.relay2AlreadyActived == 0):
                                	 SerialArduino.write('3\n'.encode())
                                	 self.relay2AlreadyActived = 1
                            	else:
                                	 SerialArduino.write('2\n'.encode()) 
                                	 self.relay2AlreadyActived = 0     
                            	print("A olho está fechado . . .")
                            	print("leftEyeDistance: ", int(leftEyeVerticalDistance), " - initial: ", int(self.initial_left_eye_distance))
                            	#cv2.waitKey(1000)
                    	else:
                        	self.countLeftEyeClosed = 0
                    	#if (self.initial_left_eye_distance == 0) and (self.count == self.valueToAverage):
                        #	print("leftEyeDistance: ", int(leftEyeVerticalDistance), " - initial: ", int(self.initial_left_eye_distance))
                    	self.count = self.count + 1
                        # processing head balance 
                    	if (self.headBalancedPointOld == None):
                        	self.headBalancedPointOld = leftEyeUpPoint
                    	headBalancedDistance, info = self.findDistance(self.headBalancedPointOld,  leftEyeUpPoint)
                    	if (headBalancedDistance > self.maxHeadDistance):
                            self.maxHeadDistance = headBalancedDistance
                    	if (self.maxHeadDistance >= self.horizBalanceTrigger):
                            self.maxHeadDistance = (self.horizBalanceTrigger / 2)
                            self.countHeadBalanced = self.countHeadBalanced + 1
                            if (self.countHeadBalanced == self.totalCountBalanced):
                            	#print("Balançou a cabeça: ", headBalancedDistance)
                            	self.countHeadBalanced = 0                                 
                            	if (self.relay3AlreadyActived == 0):
                                	SerialArduino.write('1\n'.encode())
                                	self.relay3AlreadyActived = 1
                            	else:
                                	SerialArduino.write('0\n'.encode()) 
                                	self.relay3AlreadyActived = 0
                            	cv2.waitKey(500)
                    	#else:
                        #    print("Não balançou a cabeça: ", headBalancedDistance)
						#print("face[leftEyeUp]: ", headBalancedDistance)
                faces.append(face)

        return img, faces

    def findDistance(self,p1, p2, img=None):
        """
        Find the distance between two landmarks based on their
        index numbers.
        :param p1: Point1
        :param p2: Point2
        :param img: Image to draw on.
        :param draw: Flag to draw the output on the image.
        :return: Distance between the points
                 Image with output drawn
                 Line information
        """

        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        #if img is not None:
        #    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        #    cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        #    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        #    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        #    return length,info, img
        #else:
        #    return length, info
        return length, info
    
def processHands(img, detectorHands=None, SerialArduino = None, alreadyActivated1 = 0, alreadyActivated2 = 0):
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

        finges1 = detectorHands.fingersUp(hands[0])
        if finges1[0] == 0 and finges1[1] == 1 and finges1[2] == 1 and finges1[3] == 1 and finges1[4] == 1:
            if (alreadyActivated1 == 0):
                SerialArduino.write('1\n'.encode())    
                alreadyActivated1 = 1  
                print("ativou rele 1 . . .")
        if finges1[0] == 0 and finges1[1] == 0 and finges1[2] == 0 and finges1[3] == 0 and finges1[4] == 0:
            if (alreadyActivated1 == 1):
                SerialArduino.write('0\n'.encode())
                print("Desativou rele 1 . . .")
                alreadyActivated1 = 0
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

            finges2 = detectorHands.fingersUp(hands[1])
            if finges2[0] == 0 and finges2[1] == 1 and finges2[2] == 1 and finges2[3] == 0 and finges2[4] == 0:
                if (alreadyActivated2 == 0):
                    SerialArduino.write('3\n'.encode()) 
                    alreadyActivated2 = 1
                    print("Ativou rele 2 . . .")     
            if finges2[0] == 0 and finges2[1] == 0 and finges2[2] == 0 and finges2[3] == 0 and finges2[4] == 0:
                if (alreadyActivated2 == 1):
                    SerialArduino.write('2\n'.encode())
                    alreadyActivated2 = 0
                    print("Desativou rele 2 . . .")

        #print(" ")  # New line for better readability of the printed output

    return img, alreadyActivated1, alreadyActivated2

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


    detectorFace = FaceMeshDetector(staticMode=False, maxFaces=1, minDetectionCon=0.5, minTrackCon=0.5, initial_mouth_distance=0, initial_left_eye_distance=0)
# Initialize the HandDetector class with the given parameters
    detectorHands = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

    alreadyActivated1 = 0
    alreadyActivated2 = 0
    
    while True:
        success, img = cap.read()

        img, faces = detectorFace.findFaceMesh(img, False, SerialArduino)
        #if len(faces)!= 0:
        #   print(len(faces[0]))

        img, alreadyActivated1, alreadyActivated2 = processHands(img, detectorHands, SerialArduino, alreadyActivated1, alreadyActivated2)

		# show camera image with defined points
        cv2.imshow("Image", img)

        # Wait for 1 millisecond to check for any user input, keeping the window open
        cv2.waitKey(1)


if __name__ == "__main__":
    main()