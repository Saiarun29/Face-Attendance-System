import cv2
import numpy as np
from db import get_connection
from datetime import datetime


def mark_attendance(name):
    conn = get_connection()
    cursor = conn.cursor()

    # Get or insert user
    cursor.execute("SELECT id FROM users WHERE name=%s", (name,))
    result = cursor.fetchone()

    if result:
        user_id = result[0]
    else:
        cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
        conn.commit()
        user_id = cursor.lastrowid

    today = datetime.now().date()

    # Check duplicate attendance
    cursor.execute("""
        SELECT * FROM attendance
        WHERE user_id=%s AND DATE(time)=%s
    """, (user_id, today))

    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO attendance (user_id, time) VALUES (%s, %s)",
            (user_id, datetime.now())
        )
        conn.commit()
        print(f"✅ Attendance marked for {name}")
    else:
        print(f"⚠️ Already marked today for {name}")

    conn.close()


def start_recognition():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    label_map = np.load("labels.npy", allow_pickle=True).item()
    reverse_map = {v: k for k, v in label_map.items()}

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(0)

    attendance_done = False  # Prevent multiple triggers

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]

            label, confidence = recognizer.predict(roi)

            if confidence < 80 and not attendance_done:
                attendance_done = True

                name = reverse_map[label]

                # Show name briefly
                cv2.putText(frame, name, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

                cv2.imshow("Face Recognition", frame)
                cv2.waitKey(700)  # short delay for visibility

                # Mark attendance
                mark_attendance(name)

                # Close camera immediately
                cap.release()
                cv2.destroyAllWindows()
                return

            else:
                cv2.putText(frame, "Unknown", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        cv2.imshow("Face Recognition", frame)

        # Manual exit (backup)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()