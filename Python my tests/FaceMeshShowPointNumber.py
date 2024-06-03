import cv2
import mediapipe as mp
import time


class FaceMeshDetector:

    def __init__(self, staticMode=False, maxFaces=2, minDetectionCon=0.5, minTrackCon=0.5):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticMode,self.maxFaces,
                                                 self.minDetectionCon,self.minTrackCon)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2)

    def findFaceMesh(self, img, draw=True):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        faces = []
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                	self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACE_CONNECTIONS,
                                               self.drawSpec, self.drawSpec)
                #face = []
                #for id, lm in enumerate(faceLms.landmark):
                #    ih, iw, ic = img.shape
                #    x, y = int(lm.x * iw), int(lm.y * ih)
                #    face.append([x, y])
                #faces.append(face)
        return img


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceMeshDetector()

    #detector = FaceMeshDetector(staticMode=False, maxFaces=2, minDetectionCon=0.5, minTrackCon=0.5)

    while True:
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img, draw=True)
        cTime = time.time()
        fps = 1/ (cTime - pTime)
        pTime = cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                                 3, (0, 255, 0), 3)

        # Display the image in a window named 'Image'
        cv2.imshow("Image", img)

        # Wait for 1 millisecond to check for any user input, keeping the window open
        cv2.waitKey(1)


if __name__ == "__main__":
    main()