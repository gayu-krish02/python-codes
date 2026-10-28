import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

known_face = None
threshold = 2000  # Lower is stricter; adjust as needed

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    face_count = len(faces)  # Count the number of faces

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (100, 100))

        if known_face is None:
            known_face = face_img
            label = "Known Face"
        else:
            diff = np.sum((known_face.astype("float") - face_img.astype("float")) ** 2)
            if diff < threshold:
                label = "Known Face"
            else:
                label = "Unknown"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Display the number of faces on the frame
    cv2.putText(frame, f'Faces: {face_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Real-Time Face Recognition', frame)
    
    # Exit if window is closed
    if cv2.getWindowProperty('Real-Time Face Recognition', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
exit()