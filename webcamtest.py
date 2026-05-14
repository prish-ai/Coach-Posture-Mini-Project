import cv2

cap = cv2.VideoCapture(0)   

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  

    if not ret:
        break

    cv2.putText(frame, "Webcam working!", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()