# 🎓 SIH25094 – AI-Powered Student Learning Assistant & Personalized Career Education Advisor

![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-18-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![Vite](https://img.shields.io/badge/Vite-Latest-purple)
![License](https://img.shields.io/badge/License-MIT-orange)

## 📌 Project Overview

The AI-Powered Student Learning Assistant and Personalized Career Education Advisor is an intelligent web platform developed for Students.

The system helps students make better academic and career decisions using Artificial Intelligence by providing personalized learning recommendations, career guidance, skill analysis, resume evaluation, scholarship information, and AI-powered chatbot support.

---

# ✨ Features

- AI Chat Assistant
- Personalized Learning Roadmap
- Career Recommendation
- Resume Analyzer
- Student Dashboard
- Course Recommendation
- Scholarship Information
- Admin Dashboard
- Student Progress Tracking
- Secure Authentication
- REST API Backend

---

# 🛠 Technology Stack

## Frontend

- React.js
- Vite
- Tailwind CSS
- Axios
- React Router

## Backend

- Django
- Django REST Framework
- Python

## Database

- SQLite (Development)
- MySQL (Production Ready)

## AI & ML

- Scikit-learn
- NLP
- OpenAI Integration (Future)
- Career Recommendation Engine

---

# 📂 Project Structure

```text
backend/
    accounts/
    students/
    learning/
    career/
    chatbot/
    core/

frontend/
    src/
    components/
    pages/
    services/
    assets/
```

---

# 🏗 System Architecture

```
                Student
                    │
                    ▼
          React Frontend (Vite)
                    │
         REST API (Axios Calls)
                    │
          Django REST Backend
                    │
    ┌───────────────┼───────────────┐
    │               │               │
 Student DB     AI Recommendation  Chatbot
    │               │               │
    └───────────────┼───────────────┘
                    │
                  MySQL
```

---

# 🗄 Database Modules

- Student
- Learning
- Career
- Courses
- Resume
- Chatbot
- Authentication
- Admin

---

# 👤 User Roles

### Student

- Register/Login
- Take Skill Assessment
- View Dashboard
- Chat with AI
- Upload Resume
- Receive Recommendations

### Admin

- Manage Students
- Manage Courses
- View Analytics
- Monitor AI Responses
- Manage Career Data

---

# API Modules

- Authentication API
- Student API
- Career API
- Learning API
- Chatbot API
- Resume API

---

# Installation

## Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Future Improvements

- Voice Assistant
- Video Learning Recommendation
- Interview Preparation
- AI Mock Interview
- Emotion Detection
- Multilingual Support

---

# License

MIT License

---

# Authors

Haripriyan V

Department of Artificial Intelligence and Machine Learning

VSB Engineering College

Tamil Nadu, India
