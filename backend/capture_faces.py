import cv2
import os

name = "gagana"  # change your name
path = f"dataset/{name}"

os.makedirs(path, exist_ok=True)

cap = cv2.VideoCapture(0)

count = 0

while True:
    ret, frame = cap.read()

    cv2.imshow("Capturing Faces", frame)

    # save image every loop (or press key later)
    img_path = f"{path}/{count}.jpg"
    cv2.imwrite(img_path, frame)

    count += 1

    print("Captured:", count)

    if count >= 50:  # take 50 images
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()