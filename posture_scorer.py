from session_tracker import SessionTracker
tracker = SessionTracker()
import cv2
import json
import mediapipe as mp
import math
import subprocess
import time
import ctypes


# ── MediaPipe setup ──────────────────────────────────────────
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ── Cooldown setup ───────────────────────────────────────────
last_alert_time = 0
COOLDOWN_SECONDS = 15
goodSecs = 0
badSecs  = 0
streak   = 0

# ── Angle calculator ─────────────────────────────────────────
def calculate_angle(a, b, c):
    angle_radians = math.atan2(c[1] - b[1], c[0] - b[0]) - \
                    math.atan2(a[1] - b[1], a[0] - b[0])
    angle_degrees = abs(math.degrees(angle_radians))
    if angle_degrees > 180:
        angle_degrees = 360 - angle_degrees
    return angle_degrees

# ── Posture checker ──────────────────────────────────────────
def check_posture(angle):
    if angle > 140:
        return "Good Posture", (0, 255, 0)
    else:
        return "Bad Posture! Sit Up!", (0, 0, 255)

# ── Main loop ────────────────────────────────────────────────
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        h, w, _ = frame.shape

        ear = landmarks[mp_pose.PoseLandmark.LEFT_EAR]
        shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]

        ear_pt = (int(ear.x * w), int(ear.y * h))
        shoulder_pt = (int(shoulder.x * w), int(shoulder.y * h))
        hip_pt = (int(hip.x * w), int(hip.y * h))

        angle = calculate_angle(ear_pt, shoulder_pt, hip_pt)
        status, color = check_posture(angle)

        if status == "Good Posture":
            goodSecs += 1
            streak   += 1
        else:
            badSecs += 1
            streak   = 0

        # ── Write live data for Flask ─────────────────────────
        posture_data = {
            'angle':    int(angle),
            'status':   status,
            'good_pct': round((goodSecs / max(goodSecs+badSecs,1))*100, 1),
            'bad_pct':  round((badSecs  / max(goodSecs+badSecs,1))*100, 1),
            'streak':   streak
        }
        with open('posture_data.json', 'w') as f:
            json.dump(posture_data, f)

        # ── Update session tracker ────────────────────────────
        tracker.update(status)
        stats = tracker.get_stats()

        # ── Alert logic ──────────────────────────────────────
        current_time = time.time()

        if status == "Bad Posture! Sit Up!":
            # Write bad flag
            with open("posture_flag.txt", "w") as f:
                f.write("bad")

            # Trigger alert if cooldown passed
            if current_time - last_alert_time > COOLDOWN_SECONDS:
                print("Triggering alert now!")

                # Run C alert program
                subprocess.run([
                    r"C:\Users\PRISHA\OneDrive\Desktop\coach_posture\c_ext\alert.exe"
                ])

                # Show popup
                ctypes.windll.user32.MessageBoxW(
                    0,
                    "Sit up straight!\nYour posture is bad!",
                    "Posture Coach Alert",
                    0x30
                )

                last_alert_time = current_time

        else:
            # Write good flag
            with open("posture_flag.txt", "w") as f:
                f.write("good")

        # ── Draw skeleton ────────────────────────────────────
        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        # ── Draw key points ──────────────────────────────────
        cv2.circle(frame, ear_pt, 8, (0, 255, 255), -1)
        cv2.circle(frame, shoulder_pt, 8, (255, 0, 0), -1)
        cv2.circle(frame, hip_pt, 8, (0, 255, 0), -1)

        # ── Draw posture line ────────────────────────────────
        cv2.line(frame, ear_pt, shoulder_pt, color, 2)
        cv2.line(frame, shoulder_pt, hip_pt, color, 2)

        # ── Show on screen ───────────────────────────────────
        cv2.putText(frame, f"Angle: {int(angle)}",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.putText(frame, status,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        print(f"Angle: {int(angle)} → {status}")

    else:
        cv2.putText(frame, "Stand in frame!", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 165, 255), 2)

    # ── Show session stats on screen ──────────────────────
    try:
        cv2.putText(frame, f"Session: {stats['duration']}",
                    (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, f"Good: {stats['good_pct']}%",
                    (10, 115),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv2.putText(frame, f"Bad:  {stats['bad_pct']}%",
                    (10, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    except:
        pass

    cv2.imshow("Posture Coach", frame)
                    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# ── Save log when session ends ────────────────────────
tracker.save_log()
stats = tracker.get_stats()
print("\n" + "="*40)
print("  SESSION SUMMARY")
print("="*40)
print(f"Duration    : {stats['duration']}")
print(f"Good posture: {stats['good_pct']}%")
print(f"Bad posture : {stats['bad_pct']}%")
print("="*40)