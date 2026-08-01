import cv2
import mediapipe as mp
import time
import pydirectinput as pyautogui

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

landmarker = HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
start_time = time.time()
last_move = None
last_direction = None

WINDOW_NAME = "HandRacer - Test"
window_positioned = False


def is_fist(hand):
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    curled = 0
    for tip, pip in zip(tips, pips):
        if hand[tip].y > hand[pip].y:
            curled += 1
    return curled >= 3


def count_extended_fingers(hand):
    # Sirf index(8/6), middle(12/10), ring(16/14), pinky(20/18) count karte hain
    # (thumb exclude, kyunke thumb ka up/down detect karna tricky hota hai)
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    extended = 0
    for tip, pip in zip(tips, pips):
        if hand[tip].y < hand[pip].y:  # tip pip se upar hai matlab ungli seedhi hai
            extended += 1
    return extended


while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    timestamp_ms = int((time.time() - start_time) * 1000)
    result = landmarker.detect_for_video(mp_image, timestamp_ms)

    h, w, _ = frame.shape
    move = "down"  # default: haath na ho to reverse/brake
    direction = "none"
    is_target_hand = False
    finger_count = 0

    if result.hand_landmarks and result.handedness:
        hand = result.hand_landmarks[0]
        hand_label = result.handedness[0][0].category_name

        # Flip ki wajah se "Left" label = tumhara actual RIGHT hand
        if hand_label == "Left":
            is_target_hand = True

        for lm in hand:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # Accelerate/Brake - jaisa pehle tha, kuch change nahi
        if is_fist(hand):
            move = "down"
        else:
            move = "up"

        # Turn - SIRF right hand se, finger count se
        if is_target_hand:
            finger_count = count_extended_fingers(hand)
            if finger_count == 1:
                direction = "right"
            elif finger_count == 2:
                direction = "left"
            else:
                direction = "none"

    # Accelerate/Brake hold (unchanged)
    if move != last_move:
        if last_move == "up":
            pyautogui.keyUp("up")
        elif last_move == "down":
            pyautogui.keyUp("down")

        if move == "up":
            pyautogui.keyDown("up")
        elif move == "down":
            pyautogui.keyDown("down")

        last_move = move

    # Left/Right hold (naya)
    if direction != last_direction:
        if last_direction == "left":
            pyautogui.keyUp("left")
        elif last_direction == "right":
            pyautogui.keyUp("right")

        if direction == "left":
            pyautogui.keyDown("left")
        elif direction == "right":
            pyautogui.keyDown("right")

        last_direction = direction

    status = "RIGHT HAND" if is_target_hand else "no/wrong hand"
    cv2.putText(frame, f"{status} | Fingers: {finger_count} | Dir: {direction} | Move: {move}",
                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    cv2.imshow(WINDOW_NAME, frame)

    if not window_positioned:
        cv2.moveWindow(WINDOW_NAME, 0, 0)
        cv2.resizeWindow(WINDOW_NAME, 320, 240)
        window_positioned = True

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Cleanup
if last_move == "up":
    pyautogui.keyUp("up")
elif last_move == "down":
    pyautogui.keyUp("down")
if last_direction == "left":
    pyautogui.keyUp("left")
elif last_direction == "right":
    pyautogui.keyUp("right")

landmarker.close()