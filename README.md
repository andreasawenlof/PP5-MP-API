# 🎵 Music Productivity API

## 📌 Table of Contents

-   [🎵 Music Productivity API](#-music-productivity-api)
    -   [📌 Table of Contents](#-table-of-contents)
    -   [🚀 Introduction](#-introduction)
    -   [🔗 API Endpoints](#-api-endpoints)
        -   [🔑 Authentication](#-authentication)
        -   [🎵 Tracks](#-tracks)
        -   [🎶 Albums](#-albums)
        -   [🎸 Instruments](#-instruments)
        -   [💬 Comments](#-comments)
        -   [📋 Review System (Supervisor Feedback)](#-review-system-supervisor-feedback)
    -   [📦 Database Models](#-database-models)
        -   [🏆 Core Models](#-core-models)
        -   [🔗 Model Relationships](#-model-relationships)
    -   [🛠 CRUD Functionality](#-crud-functionality)
    -   [⚙️ Setup \& Deployment](#️-setup--deployment)
        -   [💻 Local Setup](#-local-setup)
        -   [Deployment to Heroku](#deployment-to-heroku)
    -   [📚 Agile Workflow](#-agile-workflow)
    -   [Technologies Used](#technologies-used)

---

## 🚀 Introduction

The **Music Productivity API** is built using **Django Rest Framework (DRF)** to streamline music composition and collaboration. This API allows **composers** to manage their projects efficiently, while **reviewers** can provide structured feedback without altering tracks. The API enforces strict role-based access control, ensuring transparency and security within the workflow.

---

## 🔗 API Endpoints

### 🔑 Authentication

| HTTP Method | Endpoint                      | Description                              | Access        |
| ----------- | ----------------------------- | ---------------------------------------- | ------------- |
| `POST`      | `/dj-rest-auth/login/`        | Log in a user and receive an auth token. | Public        |
| `POST`      | `/dj-rest-auth/logout/`       | Log out the user.                        | Authenticated |
| `POST`      | `/dj-rest-auth/registration/` | Admin-only: Create new user accounts.    | Admin Only    |

### 🎵 Tracks

| HTTP Method | Endpoint        | Description                | Access                            |
| ----------- | --------------- | -------------------------- | --------------------------------- |
| `GET`       | `/tracks/`      | Retrieve all tracks.       | **Composers Only**                |
| `POST`      | `/tracks/`      | Create a new track.        | **Composers Only**                |
| `GET`       | `/tracks/<id>/` | Retrieve a specific track. | **Composers & Assigned Reviewer** |
| `PUT`       | `/tracks/<id>/` | Update a track.            | **Composers Only**                |
| `DELETE`    | `/tracks/<id>/` | Delete a track.            | **Composers Only**                |

### 🎶 Albums

| HTTP Method | Endpoint        | Description                | Access         |
| ----------- | --------------- | -------------------------- | -------------- |
| `GET`       | `/albums/`      | Retrieve all albums.       | Composers Only |
| `POST`      | `/albums/`      | Create a new album.        | Composers Only |
| `GET`       | `/albums/<id>/` | Retrieve a specific album. | Composers Only |
| `PUT`       | `/albums/<id>/` | Update an album.           | Composers Only |
| `DELETE`    | `/albums/<id>/` | Delete an album.           | Composers Only |

### 🎸 Instruments

| HTTP Method | Endpoint             | Description                     | Access         |
| ----------- | -------------------- | ------------------------------- | -------------- |
| `GET`       | `/instruments/`      | Retrieve all instruments.       | Composers Only |
| `POST`      | `/instruments/`      | Add a new instrument.           | Composers Only |
| `GET`       | `/instruments/<id>/` | Retrieve a specific instrument. | Composers Only |
| `DELETE`    | `/instruments/<id>/` | Delete an instrument.           | Composers Only |

### 💬 Comments

| HTTP Method | Endpoint          | Description                     | Access         |
| ----------- | ----------------- | ------------------------------- | -------------- |
| `GET`       | `/comments/`      | Retrieve all comments.          | Composers Only |
| `POST`      | `/comments/`      | Add a comment to a track/album. | Composers Only |
| `DELETE`    | `/comments/<id>/` | Delete a comment.               | Composers Only |

### 📋 Review System (Supervisor Feedback)

| HTTP Method | Endpoint         | Description                      | Access                |
| ----------- | ---------------- | -------------------------------- | --------------------- |
| `GET`       | `/reviews/`      | Retrieve all supervisor reviews. | Composers Only        |
| `POST`      | `/reviews/`      | Add a review to a track/album.   | **Reviewers Only**    |
| `GET`       | `/reviews/<id>/` | Retrieve a review.               | Composers & Reviewers |

---

## 📦 Database Models

### 🏆 Core Models

-   **User**: Handles authentication & user roles.
-   **Track**: Represents an individual composition.
-   **Album**: A collection of tracks.
-   **Instrument**: Many-to-Many model for track instrumentation.
-   **Comment**: Internal communication system.
-   **Review**: Supervisor feedback system for structured feedback.

### 🔗 Model Relationships

-   **One-to-Many**: A track belongs to an album, but an album can have many tracks.
-   **Many-to-Many**: Tracks can have multiple instruments, and instruments can be used in multiple tracks.

---

## 🛠 CRUD Functionality

👉 **Create**: Tracks, albums, instruments, comments, and reviews.  
👉 **Read**: Retrieve details for tracks, albums, comments, and reviews.  
👉 **Update**: Modify track details, albums, and reviews (reviewers only).  
👉 **Delete**: Remove tracks, albums, instruments, and comments.

---

## ⚙️ Setup & Deployment

### 💻 Local Setup

```bash
git clone <your-repo-url>
cd music-productivity-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Deployment to Heroku

```bash
heroku login
heroku create <your-app-name>
git push heroku main
heroku run python manage.py migrate
```

---

## 📚 Agile Workflow

Project development follows **Agile methodology** with iterative improvements.

---

## Technologies Used

-   **Backend**: Django, Django REST Framework (DRF)
-   **Database**: PostgreSQL (Heroku hosted)
-   **Authentication**: dj-rest-auth (JWT-based authentication)
-   **Deployment**: Heroku, Cloudinary
-   **Other Libraries**: Django CORS Headers, Gunicorn
