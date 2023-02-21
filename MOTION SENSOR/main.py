import cv2
import pygame
import requests

cam = cv2.VideoCapture(0)

# While camera is open do all this

while cam.isOpened():
    # Read what is in the camera -frames
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()

    # Get the difference in the frames
    diff = cv2.absdiff(frame1, frame2)

    # Convert color to gray for easy computation

    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)

    # Convert to blur-Gaussian Blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold to remove noise

    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Dilation and contours

    dilated = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours

    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    for c in contours:
        if cv2.contourArea(c) < 80000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        pygame.init()
        pygame.mixer.init()
        sounda = pygame.mixer.Sound("alert.wav")
        sounda.play()
        url = 'https://us-central1-darboda-flutter.cloudfunctions.net/sendAlarm'
        data = {
            "id": "bbDaWFsg33ZIgB4u7SpyrtJXony2"
        }

        res = requests.post(url, json=data)
        print(res.text)

    # Wait for 10 sec to see if the user has pressed q to quit
    if cv2.waitKey(10) == ord('q'):
        break

    cv2.imshow('Group 1 Project', frame1)
