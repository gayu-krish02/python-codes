import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Drawing colors and brush types
colors = [(0,0,255), (0,255,0), (255,0,0)]  # Red, Green, Blue
brush_types = [(12, 1.0), (4, 0.3), (8, 0.6)]  # (thickness, alpha): brush, pencil, sketch
color_names = ["Red", "Green", "Blue"]
brush_names = ["Brush", "Pencil", "Sketch"]

current_color = 0
current_brush = 0
erase_mode = False

# Button positions
button_y = 10
color_buttons = [(20 + i*70, button_y, 60, 40) for i in range(3)]
brush_buttons = [(250 + i*90, button_y, 80, 40) for i in range(3)]
erase_button = (530, button_y, 80, 40)
stop_button = (630, button_y, 40, 40)

cap = cv2.VideoCapture(0)
canvas = None
prev_point = None

def fingers_up(hand_landmarks):
    # Returns a list of which fingers are up (1) or down (0)
    tips = [4, 8, 12, 16, 20]
    up = []
    for tip in tips:
        up.append(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y)
    return up

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    if canvas is None:
        canvas = np.ones_like(frame) * 255  # White background

    # Draw UI buttons
    for i, (x, y, bw, bh) in enumerate(color_buttons):
        cv2.rectangle(frame, (x, y), (x+bw, y+bh), colors[i], -1 if current_color==i else 2)
        cv2.putText(frame, color_names[i], (x+5, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255) if current_color==i else colors[i], 2)
    for i, (x, y, bw, bh) in enumerate(brush_buttons):
        cv2.rectangle(frame, (x, y), (x+bw, y+bh), (50,50,50), -1 if current_brush==i else 2)
        cv2.putText(frame, brush_names[i], (x+5, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255) if current_brush==i else (50,50,50), 2)
    # Erase button
    ex, ey, ew, eh = erase_button
    cv2.rectangle(frame, (ex, ey), (ex+ew, ey+eh), (0,0,0), -1 if erase_mode else 2)
    cv2.putText(frame, "Erase", (ex+5, ey+30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255) if erase_mode else (0,0,0), 2)
    # Stop button
    sx, sy, sw, sh = stop_button
    cv2.rectangle(frame, (sx, sy), (sx+sw, sy+sh), (0,0,0), 2)
    cv2.putText(frame, "X", (sx+10, sy+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    index_finger_tip = None
    up = [0,0,0,0,0]

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            h, w, _ = frame.shape
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)
            index_finger_tip = (x, y)
            up = fingers_up(hand_landmarks)

    # Button click detection (only if index finger is up and others are down)
    if index_finger_tip and up[1] and not any(up[2:]):
        ix, iy = index_finger_tip
        # Color buttons
        for i, (x, y, bw, bh) in enumerate(color_buttons):
            if x < ix < x+bw and y < iy < y+bh:
                current_color = i
                erase_mode = False
                prev_point = None
        # Brush buttons
        for i, (x, y, bw, bh) in enumerate(brush_buttons):
            if x < ix < x+bw and y < iy < y+bh:
                current_brush = i
                erase_mode = False
                prev_point = None
        # Erase button
        ex, ey, ew, eh = erase_button
        if ex < ix < ex+ew and ey < iy < ey+eh:
            erase_mode = True
            prev_point = None
        # Stop button
        sx, sy, sw, sh = stop_button
        if sx < ix < sx+sw and sy < iy < sy+sh:
            break

    # Draw only if index finger is up and all other fingers are down
    if index_finger_tip and up[1] and not any(up[2:]):
        if prev_point:
            if erase_mode:
                cv2.line(canvas, prev_point, index_finger_tip, (255,255,255), 30)
            else:
                thickness, alpha = brush_types[current_brush]
                overlay = canvas.copy()
                cv2.line(overlay, prev_point, index_finger_tip, colors[current_color], thickness)
                cv2.addWeighted(overlay, alpha, canvas, 1 - alpha, 0, canvas)
        prev_point = index_finger_tip
    else:
        prev_point = None

    # Overlay the canvas on the frame
    display = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
    cv2.imshow("Air Drawing", display)

    if cv2.getWindowProperty("Air Drawing", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
