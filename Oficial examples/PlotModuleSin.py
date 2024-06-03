from cvzone.PlotModule import LivePlot
import cv2
import math


sinPlot = LivePlot(w=1200, yLimit=[-100, 100], interval=0.01)
xSin=0

while True:

    xSin += 1
    if xSin == 360: xSin = 0
    imgPlotSin = sinPlot.update(int(math.sin(math.radians(xSin)) * 100))

    cv2.imshow("Image Sin Plot", imgPlotSin)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break