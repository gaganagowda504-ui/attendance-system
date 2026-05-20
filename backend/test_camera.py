import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)

    # Press 's' to SAVE image
    if key & 0xFF == ord('s'):
        cv2.imwrite("my_photo.jpg", frame)
        print("Photo saved!")

    # Press 'q' to quit
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()