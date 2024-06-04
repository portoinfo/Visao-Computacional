"""
Face Mesh Module
By: Computer Vision Zone
Website: https://www.computervision.zone/
"""

import cv2
import mediapipe as mp
import math


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

    def findFaceMesh(self, img, draw=True):
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
                    	leftEyeUpPoint = face[point_left_eye_1]
                    	leftEyeDownPoint = face[point_left_eye_2]
                    	leftEyeVerticalDistance, info = self.findDistance(leftEyeUpPoint, leftEyeDownPoint)
                    	if (self.initial_left_eye_distance == 0):
                        	self.initial_left_eye_distance = leftEyeVerticalDistance                        
                    	print("leftEyeDistance: ", int(leftEyeVerticalDistance), " - initial: ", int(self.initial_left_eye_distance))
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

def main():
    cap = cv2.VideoCapture(0)

    detector = FaceMeshDetector(staticMode=False, maxFaces=1, minDetectionCon=0.5, minTrackCon=0.5, initial_mouth_distance=0, initial_left_eye_distance=0)
    while True:
        success, img = cap.read()

        img, faces = detector.findFaceMesh(img, False)
        #if len(faces)!= 0:
        #   print(len(faces[0]))

		# show camera image with defined points
        cv2.imshow("Image", img)

        # Wait for 1 millisecond to check for any user input, keeping the window open
        cv2.waitKey(200)


if __name__ == "__main__":
    main()