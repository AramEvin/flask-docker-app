# 🐳 Flask Docker Starter App

A simple, extensible web application using **Flask**, **PostgreSQL**, and **Docker Compose**. Built for learning DevOps concepts, containerization, and web app deployment workflows.

---

## 🚀 Features

- 🔧 Flask application with blueprints and Jinja2 templates
- 🐘 PostgreSQL database with automatic init
- 🐳 Dockerized environment using Docker Compose
- 🧩 Environment variables with `.env`
- 🎨 Basic CSS + HTML frontend
- ♻️ CRUD operations on users (Create, Read, Update, Delete)
- 📁 Clean project structure following Flask best practices

---

## 📁 Project Structure

│
├── app/
│ ├── init.py # Flask app factory
│ ├── db.py # DB connection logic
│ ├── routes/ # Blueprint routes
│ │ └── users.py
│ ├── templates/ # HTML templates
│ └── static/ # CSS and static files
│
├── main.py # Entrypoint for app
├── Dockerfile # App Docker image
├── docker-compose.yml # Service orchestration
├── requirements.txt # Python dependencies
├── .env # Environment variables
└── .gitignore
