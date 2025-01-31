# 🎵 Music Productivity API

## 📌 Table of Contents

- [🎵 Music Productivity API](#-music-productivity-api)
  - [📌 Table of Contents](#-table-of-contents)
  - [🚀 Introduction](#-introduction)
  - [🔗 API Endpoints](#-api-endpoints)
    - [🔑 Authentication](#-authentication)
    - [🎵 Tracks](#-tracks)
    - [🎶 Albums](#-albums)
    - [🎸 Instruments](#-instruments)
    - [💬 Comments](#-comments)
    - [📋 Review System (Supervisor Feedback)](#-review-system-supervisor-feedback)
  - [📦 Database Models](#-database-models)
    - [🏆 Core Models](#-core-models)
    - [🔗 Model Relationships](#-model-relationships)
  - [🛠 CRUD Functionality](#-crud-functionality)
  - [🔒 Authentication \& User Management](#-authentication--user-management)
  - [⚙️ Setup \& Deployment](#️-setup--deployment)
    - [💻 Local Setup](#-local-setup)
    - [Deployment to Heroku](#deployment-to-heroku)
  - [Technologies Used](#technologies-used)

---

## 🚀 Introduction

The **Music Productivity API** is a Django Rest Framework (DRF) powered backend designed to help composers and producers efficiently **manage their music projects**. Users can create, track, and organize **songs (tracks), albums, comments, instruments, and supervisor reviews** within an **intuitive, structured system**.

---

## 🔗 API Endpoints

### 🔑 Authentication

| HTTP Method | Endpoint                      | Description                              | Authentication |
| ----------- | ----------------------------- | ---------------------------------------- | -------------- |
| `POST`      | `/dj-rest-auth/login/`        | Log in a user and receive an auth token. | ❌ No          |
| `POST`      | `/dj-rest-auth/logout/`       | Log out the user.                        | ✅ Yes         |
| `POST`      | `/dj-rest-auth/registration/` | Admin-only: Create new user accounts.    | ✅ Admin Only  |

---

### 🎵 Tracks

| HTTP Method | Endpoint        | Description                | Authentication      |
| ----------- | --------------- | -------------------------- | ------------------- |
| `GET`       | `/tracks/`      | Retrieve all tracks.       | ❌ No               |
| `POST`      | `/tracks/`      | Create a new track.        | ✅ Yes              |
| `GET`       | `/tracks/<id>/` | Retrieve a specific track. | ❌ No               |
| `PUT`       | `/tracks/<id>/` | Update a track.            | ✅ Yes (Owner Only) |
| `DELETE`    | `/tracks/<id>/` | Delete a track.            | ✅ Yes (Owner Only) |

---

### 🎶 Albums

| HTTP Method | Endpoint        | Description                | Authentication |
| ----------- | --------------- | -------------------------- | -------------- |
| `GET`       | `/albums/`      | Retrieve all albums.       | ❌ No          |
| `POST`      | `/albums/`      | Create a new album.        | ✅ Yes         |
| `GET`       | `/albums/<id>/` | Retrieve a specific album. | ❌ No          |
| `PUT`       | `/albums/<id>/` | Update an album.           | ✅ Yes         |
| `DELETE`    | `/albums/<id>/` | Delete an album.           | ✅ Yes         |

---

### 🎸 Instruments

| HTTP Method | Endpoint             | Description                     | Authentication |
| ----------- | -------------------- | ------------------------------- | -------------- |
| `GET`       | `/instruments/`      | Retrieve all instruments.       | ❌ No          |
| `POST`      | `/instruments/`      | Add a new instrument.           | ✅ Yes         |
| `GET`       | `/instruments/<id>/` | Retrieve a specific instrument. | ❌ No          |
| `DELETE`    | `/instruments/<id>/` | Delete an instrument.           | ✅ Yes         |

---

### 💬 Comments

| HTTP Method | Endpoint          | Description                     | Authentication |
| ----------- | ----------------- | ------------------------------- | -------------- |
| `GET`       | `/comments/`      | Retrieve all comments.          | ❌ No          |
| `POST`      | `/comments/`      | Add a comment to a track/album. | ✅ Yes         |
| `DELETE`    | `/comments/<id>/` | Delete a comment.               | ✅ Yes         |

---

### 📋 Review System (Supervisor Feedback)

| HTTP Method | Endpoint         | Description                      | Authentication    |
| ----------- | ---------------- | -------------------------------- | ----------------- |
| `GET`       | `/reviews/`      | Retrieve all supervisor reviews. | ✅ Yes            |
| `POST`      | `/reviews/`      | Add a review to a track/album.   | ✅ Yes (Reviewer) |
| `PUT`       | `/reviews/<id>/` | Update a supervisor review.      | ✅ Yes (Reviewer) |
| `DELETE`    | `/reviews/<id>/` | Delete a review.                 | ✅ Yes (Reviewer) |

---

## 📦 Database Models

### 🏆 Core Models

-   **User**: Handles authentication & user data.
-   **Track**: Represents an individual song, linked to an album & instruments.
-   **Album**: A collection of tracks with its own genre, mood, and status.
-   **Instrument**: A Many-to-Many model allowing tracks to list used instruments.
-   **Comment**: A comment system for tracks & albums, allowing internal discussion.
-   **Review**: Supervisor feedback system, assigned to tracks/albums for revisions.

### 🔗 Model Relationships

-   **One-to-Many**: A track belongs to an album, but an album can have many tracks.
-   **Many-to-Many**: Tracks can have multiple instruments, and instruments can be used in multiple tracks.

---

## 🛠 CRUD Functionality

✅ **Create**: Users can add tracks, albums, instruments, and comments.  
✅ **Read**: Retrieve and display all entries (tracks, albums, etc.).  
✅ **Update**: Modify track details, albums, and supervisor reviews.  
✅ **Delete**: Remove tracks, albums, instruments, and comments.

---

## 🔒 Authentication & User Management

-   **Only admins can create new users.** No public registration.
-   **Users log in with credentials.**
-   **Users can only edit/delete their own tracks, albums, and comments.**
-   **Supervisors can post/edit reviews but cannot change track/album content.**

---

## ⚙️ Setup & Deployment

### 💻 Local Setup

1. **Clone the repository**

    ```bash
    git clone <your-backend-repo-url>
    cd music-productivity-api

    ```

2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Mac/Linux
    venv\Scripts\activate  # Windows
    ```
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run database migrations**
    ```bash
    python manage.py migrate
    ```
5. **Create a superuser** (optional, for admin access)
    ```bash
    python manage.py createsuperuser
    ```
6. **Run the development server**
    ```bash
    python manage.py runserver
    ```

### Deployment to Heroku

1. **Install Heroku CLI** and log in:
    ```bash
    heroku login
    ```
2. **Create a Heroku App**
    ```bash
    heroku create <your-app-name>
    ```
3. **Set up environment variables** in Heroku:
    - `SECRET_KEY`
    - `DATABASE_URL`
    - `ALLOWED_HOST`
4. **Deploy to Heroku**
    ```bash
    git push heroku main
    heroku run python manage.py migrate
    ```
5. **Run the app**
    ```bash
    heroku open
    ```

---

## Technologies Used

-   **Backend**: Django, Django REST Framework (DRF)
-   **Database**: PostgreSQL (Heroku hosted)
-   **Authentication**: dj-rest-auth (JWT-based authentication)
-   **Deployment**: Heroku
-   **Other Libraries**: Django CORS Headers, Gunicorn

---

🔥 **This README will evolve as features get implemented.** 🚀

---
