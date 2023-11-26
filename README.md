<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>SOUNDLY-BACKEND</h1>
<h3>◦ Developed with the software and tools below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/precommit-FAB040.svg?style=flat-square&logo=pre-commit&logoColor=black" alt="precommit" />
<img src="https://img.shields.io/badge/Gunicorn-499848.svg?style=flat-square&logo=Gunicorn&logoColor=white" alt="Gunicorn" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Django-092E20.svg?style=flat-square&logo=Django&logoColor=white" alt="Django" />
</p>
</div>

---

## 📖 Table of Contents
- [📖 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [📦 Features](#-features)
- [📂 repository Structure](#-repository-structure)
- [🚀 Getting Started](#-getting-started)
- [🛣 Roadmap](#-roadmap)

---

## 📍 Overview

Soundly Backend is the server-side component of a music streaming and playlist management system. 
It enables users to listen to their favorite songs, create playlists, and explore music.

---

## 📦 Features



### Authentication

- Email authentication with OTP
- Phone number authentication with OTP

### Homepage

- Get started songs / Recently played
- Favorite artist songs
- Recommendations based on user preferences

### Profile Page

- Followed artists' songs
- Listening history
- Logout

### Search

- Song search
- Advanced search based on language, mood, and genre

### Your Library

- Liked songs
- Followed artists
- Playlist creation and management

### Artist’s Dashboard

- Upload Your own Songs
- Description and tags
- Thumbnail upload



### Additional Features

- Guess game (Check your Knowledge)
- Synchronized lyrics (Json Data processed and sent for lyrics Synchronization)


---


## 📂 Repository Structure

```sh
└── Soundly-Backend/
    ├── accounts/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── renderers.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── utils.py
    │   └── views.py
    ├── game/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations/
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── music/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations/
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── soundly/
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── staticfiles/
    ├── images/
    ├── manage.py
    ├── requirements.txt
    ├── db.sqlite3

```

## 🚀 Getting Started

### Prerequisites

Before you begin, make sure you have the following dependencies installed on your system:

- [Python](https://www.python.org/downloads/): Ensure that you have Python installed. You can download it from the official Python website.

### Installing Dependencies

1. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    ```

    Activate the virtual environment:

    - **On Windows:**

        ```bash
        .\venv\Scripts\activate
        ```

    - **On macOS and Linux:**

        ```bash
        source venv/bin/activate
        ```

2. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    This will install all the required packages specified in the `requirements.txt` file.

### Running the Django Project

1. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

2. Start the development server:

    ```bash
    python manage.py runserver
    ```

    The Django development server will run at `http://127.0.0.1:8000/` by default.

3. Open your web browser and navigate to the provided address to view the Django project.


---

## 🛣Roadmap Project 

- [ ] **Task 1: Implement Razorpay Integration**
  - Integrate Razorpay for artists to set up payment processing.
  - Allow users to become artists and monetize their creations.
  - Implement payment flows for users subscribing to artist features.

- [ ] **Task 2: Implement Google OAuth**
  - Integrate Google OAuth for a seamless and secure login experience.
  - Allow users to sign in with their Google accounts.
  - Enhance user authentication and access control.

- [ ] **Task 3: Group Listening Feature**
  - Enable users to listen to music together in real-time.
  - Implement a synchronized playback experience for users in a group.
  - Allow users to create and join listening sessions.

- [ ] **Task 4: Notifications**
  - Implement a notification system for user interactions and updates.
  - Notify users about new releases, artist updates, and playlist changes.
  - Allow users to customize their notification preferences.

- [ ] **Task 5: Artist Analytics**
  - Provide artists with analytics on their listenership and engagement.
  - Implement insights such as play counts, listener demographics, and popular tracks.
  - Enhance the dashboard for artists to track their performance.

- [ ] **Task 6: Bug Fixes and Optimization**
  - Address reported bugs and issues.
  - Optimize the performance of the application.
  - Conduct thorough testing to ensure a stable and reliable user experience.
