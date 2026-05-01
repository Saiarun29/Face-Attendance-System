@"
# 🎯 ProAttend – Smart Face Recognition Attendance System

ProAttend is an AI-powered attendance system that uses **face recognition technology** to automatically mark attendance in real time. It reduces manual effort and improves accuracy using computer vision.

---

## 🚀 Features

- 🔐 Secure Teacher Login  
- 📸 Face Registration using Webcam  
- 🧠 Model Training (OpenCV - LBPH)  
- 🎥 Real-time Face Recognition  
- 🗃️ MySQL Database Integration  
- 📊 Smart Dashboard:
  - ✅ Present Students  
  - 🟡 Registered but Absent  
  - 🔴 Not Registered  
- 🚫 Prevents duplicate attendance per day  
- 🎨 Modern UI (Glassmorphism Design)  

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)  
- **Computer Vision:** OpenCV, NumPy  
- **Database:** MySQL  
- **Frontend:** HTML, CSS  
- **Version Control:** Git, GitHub  

---

## 🧩 System Workflow

1. Teacher logs in  
2. Register student faces  
3. Train the model  
4. Start attendance  
5. System detects faces and marks attendance  
6. View categorized dashboard  

---

## 📂 Project Structure

Face-Attendance-System/
│
├── app.py  
├── attendance.py  
├── train_model.py  
├── register.py  
├── db.py  
│  
├── templates/  
│   ├── index.html  
│   ├── home.html  
│   └── dashboard.html  
│  
├── static/  
│   ├── bg.png  
│   ├── logo.png  
│   ├── icon.png  
│   └── dataset/  

---

## ⚙️ Setup Instructions

### 1. Clone the repository

git clone https://github.com/Saiarun29/Face-Attendance-System.git  
cd Face-Attendance-System  

---

### 2. Install dependencies

pip install flask opencv-python numpy mysql-connector-python  

---

### 3. Setup MySQL Database

CREATE DATABASE attendance_system;  

USE attendance_system;  

CREATE TABLE users (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    name VARCHAR(100)  
);  

CREATE TABLE attendance (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    user_id INT,  
    time DATETIME  
);  

CREATE TABLE students (  
    id INT AUTO_INCREMENT PRIMARY KEY,  
    name VARCHAR(100),  
    roll_no VARCHAR(50),  
    registered BOOLEAN DEFAULT FALSE  
);  

---

### 4. Run the application

python app.py  

---

### 5. Open in browser

http://127.0.0.1:5000  

---

## 🎯 Key Highlights

- Real-time face detection  
- Efficient LBPH model  
- Clean UI design  
- Practical real-world use case  

---

## 🔮 Future Improvements

- 📊 Add analytics charts  
- 📤 Export attendance to Excel  
- 👥 Multi-user login system  
- ☁️ Deploy to cloud  

---

## 👨‍💻 Author

**Nandikonda Saiarun**

---

## ⭐ Support

If you found this project useful, please give it a ⭐ on GitHub!
"@ | Set-Content README.md
