<div align="center">
<h1 align="center">

    
![Cover](https://github.com/ilakshaygupt/Soundly-Backend/assets/99826011/4af19f66-a134-4dae-b7ac-b3cdf95a6d6c)

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
- [🚀 Getting Started](#-getting-started)
- [🖼 Images](#-images)

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

## 🖼 Images

<p align="center">
  <img width="200" alt="Screenshot 2024-07-12 at 6 30 20 AM" src="https://github.com/user-attachments/assets/7393c918-614a-4877-acfd-6aa2968eccb1">
  <img src="https://github.com/user-attachments/assets/7332fd13-e7c0-4d6f-9b1f-8bacd6b9d982" alt="Artist" width="200" >
  <img src="https://github.com/user-attachments/assets/27b15221-b818-44ca-a6a3-6060caf6d90c" alt="player" width="200" >
  <img src="https://github.com/user-attachments/assets/fef117b7-3fa4-4adc-968e-639784a9328b" alt="Mobile Sign Up" width="200" >
</p>

### Desktop Images

<p align="center">
  <img src="https://github.com/user-attachments/assets/bee9b6f6-9daa-47f2-a8c1-c8981d714b2a" alt="Sign Up">
  <img src="https://github.com/user-attachments/assets/f674a78f-306b-48ee-aeb3-8a4978400245" alt="Music Player" >
  <img src="https://github.com/user-attachments/assets/26e191dd-9dc7-4234-a844-0f55d26ff694" alt="Search" >
  <img src="https://github.com/user-attachments/assets/3be47a4c-72ed-469f-8ac0-65c3efa2515a" alt="Home Page" >
</p>
