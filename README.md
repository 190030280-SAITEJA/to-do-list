Project Name: SmartTask - A Personal Task Manager

Description:SmartTask is a web-based to-do list application built with Flask that allows users to efficiently manage their daily tasks. It features user authentication (sign up, login, logout), task creation with categories and priorities, due date tracking, and task status toggling (Pending/Completed). Each user sees only their own tasks, ensuring a personalized experience.

Purpose : 

Stay organized by categorizing and prioritizing tasks.

Manage their time better through due date reminders and overdue indicators.

Keep track of progress with the ability to toggle task completion status.

It serves as both a productivity tool and a learning project for understanding full-stack web development.

Value: 

User-Focused Design: Each user has a secure, isolated space to manage their tasks.

Visual Productivity: Overdue tasks are visually highlighted, helping users prioritize.

Simplicity and Accessibility: Easy to use, minimal setup required, accessible from any browser.

Learning-Oriented: Demonstrates core web development concepts like database relationships, user sessions, form handling, and CRUD operations.



Technologies Used: This project was developed using Python 3 and the Flask web framework to handle routing, server-side logic, and session management. For data storage, it uses SQLite, a lightweight relational database, alongside SQLAlchemy, which serves as an Object Relational Mapper (ORM) to manage database operations with Python classes. User authentication is secured using Werkzeug's built-in password hashing utilities. On the frontend, the app utilizes HTML5, CSS3, and the Bootstrap framework to create a responsive and user-friendly interface. Jinja2 templating is used to dynamically render HTML content based on backend data.

Setup Instructions: 

1.Install Python

Make sure Python is installed on your computer.

You can download it from python.org/downloads.

During installation, check “Add Python to PATH”.

2.Download the Project

If you're using Git:

git clone https://github.com/190030280-SAITEJA/to-do-list.git

cd to-do-list/src

Or just download the ZIP file from GitHub and extract it.

 3.Install the Required Libraries
 
 pip install -r requirements.txt

 4.Run the App

 python to-do-list.py

Visit in your browser:
Open http://127.0.0.1:5000 in your browser to start using the app.
