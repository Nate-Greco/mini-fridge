import cv2
from keyboard import is_pressed

cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

exit = False

while True:
    ret, frames = cam.read()

    if not ret:
        print("no frames")

    cv2.imshow('feed', frames)
    
    
    cv2.waitKey(1)

    if is_pressed('x'):
        print("exit")
        break

cam.release()
cv2.destroyAllWindows()