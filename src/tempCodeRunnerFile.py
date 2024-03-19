'''
gest_name = handmajor.get_gesture()
Controller.handle_controls(gest_name, handmajor.hand_result)
                    
for hand_landmarks in results.multi_hand_landmarks:
    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
else:
    Controller.prev_hand = None
cv2.imshow('Gesture Controller', image)
'''

import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize MediaPipe Drawing
mp_drawing = mp.solutions.drawing_utils

# Initialize variables for mouse control
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
hand_center_x, hand_center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
mouse_enabled = False

# Create a function to move the mouse cursor
def move_mouse(x, y):
    pyautogui.moveTo(x, y)

# Create a function to perform a click
def perform_click():
    pyautogui.click()

# Create a function to toggle mouse control
def toggle_mouse_control():
    global mouse_enabled
    mouse_enabled = not mouse_enabled

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Calculate the center of the hand
            hand_center_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * SCREEN_WIDTH)
            hand_center_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * SCREEN_HEIGHT)

            # Draw landmarks and connections on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # If mouse control is enabled, move the mouse
            if mouse_enabled:
                move_mouse(hand_center_x, hand_center_y)
    else:
        # If no hands are detected, disable mouse control
        mouse_enabled = False

    # Show the frame with the mouse cursor
    cv2.imshow('Gesture Controlled Mouse', frame)

    # Handle key events
    key = cv2.waitKey(1)
    if key == 27:  # ESC key to exit
        break
    elif key == ord('c'):  # 'c' key to perform a click
        perform_click()
    elif key == ord('m'):  # 'm' key to toggle mouse control
        toggle_mouse_control()

# Release the webcam and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Release MediaPipe Hands
hands.close()
