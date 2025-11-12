Facial Recognition Attendance System

This project is a real-time, face-based attendance tracking system developed during an industrial internship. It combines computer vision, machine learning, and GUI development to automate the attendance process in a professional environment.

It captures faces through a webcam, identifies the person, and allows them to Clock-In / Clock-Out securely using a 5-second facial confirmation and a manual verification button to avoid accidental marking.

⸻

⭐ Key Highlights
	•	🎥 Live Face Detection & Recognition using OpenCV + Face Recognition
	•	🧠 5-second identity confirmation delay for reliability
	•	👆 Manual “Mark Attendance” button to prevent false triggers
	•	🗂️ Logs attendance in Attendance.csv
	•	🧾 Shows Clock-In / Clock-Out status and working time summary
	•	🧱 Modern GUI built with PyQt5
	•	🛡️ Handles unreadable images & Mac .DS_Store issues
	•	💻 Suitable for offices, labs, classrooms, co-working spaces

⸻

🧰 Tech Stack

Component	Technology
Programming Language	Python 3.x
Face Recognition	face_recognition (dlib)
Computer Vision	OpenCV
GUI Framework	PyQt5
Data Storage	CSV (Pluggable to SQLite / MySQL)


⸻

📂 Project Structure

Attendance System/
│── ImagesAttendance/        # Face images for recognition
│── Attendance.csv           # Auto-generated attendance log
│── mainwindow.py            # Entry GUI
│── out_window.py            # Camera + recognition + logic
│── mainwindow.ui            # PyQt UI file
│── outputwindow.ui          # PyQt UI file
│── README.md                # Documentation
│── requirements.txt         # Dependencies


⸻

🚀 How to Run

1️⃣ Install Libraries

pip install opencv-python face_recognition PyQt5 numpy

macOS users may need brew install cmake for face_recognition.

2️⃣ Add User Faces

Place clear face images inside:

ImagesAttendance/

The filename = person’s name.

ImagesAttendance/
 ├── rahman.jpg
 ├── john.png

3️⃣ Start the System

python mainwindow.py

Click Start System → camera opens → system ready.

⸻

✅ CSV Output Format

Name	Timestamp	Action
JOHN	25/10/24 09:14:22	Clock In
JOHN	25/10/24 17:59:11	Clock Out


⸻

🛠️ How It Works
	1.	Load saved faces & generate encodings
	2.	Open webcam & detect faces in real-time
	3.	Compare encoding → match identity
	4.	Wait 5 seconds to verify presence
	5.	User clicks Mark Attendance button
	6.	System logs entry & updates UI

This ensures accuracy and prevents accidental attendance marking.

⸻

🎯 Future Enhancements
	•	Web dashboard & admin login
	•	Mobile attendance app
	•	QR + Face dual authentication
	•	Cloud database (Firebase / MySQL)
	•	Employee analytics & reports
	•	Customized alert sounds & notifications

⸻

👨‍💻 About This Project

This application was built as part of a real industrial internship, with a focus on:
	•	Practical computer vision deployment
	•	GUI-based user systems
	•	Real-world reliability checks
	•	Time & attendance automation

It reflects hands-on engineering, not just theory.

⸻

🤝 Acknowledgements
	•	OpenCV contributors
	•	face_recognition library by Adam Geitgey
	•	PyQt5 framework
	•	Mentors & internship team for guidance

⸻

