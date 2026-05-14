# 🧠 AI Posture Coach

An AI-powered real-time posture detection and monitoring system built using Python, OpenCV, MediaPipe, and Computer Vision techniques.

The project uses pose estimation and skeletal landmark tracking to analyze user posture through a webcam feed and intelligently classify posture as good or bad in real time. It also provides smart alerts, session analytics, and live posture statistics to encourage healthier sitting habits during work or study sessions.

---

# 🚀 Features

- ✅ Real-time posture detection using AI pose estimation
- ✅ Computer vision–based skeletal tracking
- ✅ Intelligent posture classification system
- ✅ Detects slouching using body-angle calculations
- ✅ Popup alerts for bad posture
- ✅ Live posture analytics and session tracking
- ✅ Good vs bad posture percentage monitoring
- ✅ Flask API integration for live posture data
- ✅ CSV logging for long-term analytics and visualization
- ✅ Lightweight and works using a normal webcam

---

# 🧠 AI & Computer Vision Concepts Used

- Pose Estimation
- Human Landmark Detection
- Real-Time Video Processing
- Skeletal Tracking
- Angle-Based Posture Classification
- Computer Vision Analytics
- Behavioral Monitoring

The project leverages MediaPipe Pose Estimation to detect key body landmarks such as:
- Ear
- Shoulder
- Hip

Using these landmarks, the system calculates posture angles dynamically and classifies posture quality in real time.

---

# 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- Flask
- JSON
- Computer Vision
- Real-Time Webcam Processing

---

# 📂 Project Structure

```bash
Coach-Posture-Mini-Project/
│
├── posture_scorer.py
├── posedetector.py
├── session_tracker.py
├── server.py
├── posture_data.json
├── posture_flag.txt
├── requirements.txt
│
├── logs/
│   └── posture_sessions.csv
│
├── screenshots/
│   └── demo.png
