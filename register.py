import cv2
import os

def register_user(name):
    path = f"static/dataset/{name}"
    os.makedirs(path, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    while True:
        success, img = cap.read()
        cv2.imshow("Register Face", img)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(f"{path}/{count}.jpg", img)
            count += 1
            print(f"Captured {count}")

        if count >= 5:
            break

    cap.release()
    cv2.destroyAllWindows()