# PyLearnHub

**PyLearnHub** is a comprehensive Python learning platform designed for learners and enthusiasts to study Python, engage in interactive classes, collaborate in a supportive community, and track their course progress. Built with **Django**, **MySQL**, and **Docker**, **PyLearnHub has been tested on Linux (Ubuntu 24.04)** and demonstrates professional Python web development, Docker deployment, and environment management best practices.

---

##  Features

### Courses
- Comprehensive Python courses for all skill levels.
- Enroll in courses and track progress: **Enrolled → In-Progress → Completed**.
- Submit course tasks directly through the platform.
- **Tested on Linux** for all course and task features.

### Live Interactive Classes
- Join live sessions for real-time learning.
- Participate in coding exercises and live discussions.
- Fully compatible and **tested on Linux** environments.

### Community & Collaboration
- Post questions and share code for debugging.
- Comment on posts and provide feedback.
- Upload and download source code and images related to tasks or problems.
- Collaborative learning and peer support.
- **Tested on Linux** for all community features.

### Account Management
- Signup/Login required to participate.
- Profile management and course tracking.
- **Linux-tested account flows** for reliability.

---

##  Tech Stack

- **Backend:** Python 3.11, Django  
- **Database:** MySQL  
- **Environment Management:** `python-decouple`  
- **Containerization:** Docker  
- **Tested on Linux**

---

##  Installation & Setup (Linux / Ubuntu Recommended)

### 1. Clone Repository

```bash
git clone https://github.com/nexapytech/nexapy-learnhub.git
cd nexapy-learnhub





### Docker Setup (Recommended)
docker build -t pylearnhub .
docker run -p 8000:8000 pylearnhub
