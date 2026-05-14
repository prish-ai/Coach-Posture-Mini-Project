import cv2
import mediapipe as mp

# Setup MediaPipe Pose
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # mirror it

    # Convert to RGB (MediaPipe needs RGB, OpenCV gives BGR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run pose detection
    results = pose.process(rgb_frame)

    # Draw skeleton if a person is detected
    if results.pose_landmarks:
        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        # Get the 4 landmarks we care about
        landmarks = results.pose_landmarks.landmark

        left_shoulder  = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_ear       = landmarks[mp_pose.PoseLandmark.LEFT_EAR]
        left_hip       = landmarks[mp_pose.PoseLandmark.LEFT_HIP]

        # Get frame size to convert landmark % positions to pixels
        h, w, _ = frame.shape

        # Draw circles on our 4 key points
        cv2.circle(frame, (int(left_shoulder.x * w), int(left_shoulder.y * h)),
                   8, (255, 0, 0), -1)   # blue = left shoulder
        cv2.circle(frame, (int(right_shoulder.x * w), int(right_shoulder.y * h)),
                   8, (255, 0, 0), -1)   # blue = right shoulder
        cv2.circle(frame, (int(left_ear.x * w), int(left_ear.y * h)),
                   8, (0, 255, 255), -1) # yellow = ear
        cv2.circle(frame, (int(left_hip.x * w), int(left_hip.y * h)),
                   8, (0, 255, 0), -1)   # green = hip

        # Print coordinates to terminal
        print(f"Shoulder: ({left_shoulder.x:.2f}, {left_shoulder.y:.2f})")
        print(f"Ear:      ({left_ear.x:.2f}, {left_ear.y:.2f})")

    else:
        cv2.putText(frame, "No person detected", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Pose Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()