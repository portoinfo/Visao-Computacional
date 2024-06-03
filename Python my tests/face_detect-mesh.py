import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
while True:
	success, img = cap.read()
	img = cv2.flip(img, 1)
	img, faces = detector.findFaceMesh(img)
	if faces:
		print(faces[0][0])
	cv2.imshow("Image", img)
	cv2.waitKey(1)