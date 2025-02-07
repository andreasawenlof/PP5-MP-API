# 🎵 Music Productivity API

## 📌 Table of Contents

-   [🎵 Music Productivity API](#-music-productivity-api)
    -   [📌 Table of Contents](#-table-of-contents)
    -   [🚀 Introduction](#-introduction)
    -   [🔗 API Endpoints](#-api-endpoints)
        -   [🔑 Authentication](#-authentication)
        -   [🎵 Tracks](#-tracks)
    -   [📚 Testing](#-testing)
    -   [📚 Security Considerations](#-security-considerations)
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

...

---

## 📚 Testing

The API has been tested using **Postman** to verify that all endpoints function correctly. Below are the key areas of testing:

1. **Authentication**
    - Login, Logout, Registration functionality.
    - JWT Token handling and security.
2. **Tracks & Albums**
    - Creating, updating, deleting, and retrieving.
    - Ensuring only authorized users can modify content.
3. **Comments & Reviews**
    - Posting, retrieving, and deleting comments.
    - Ensuring reviewers can provide structured feedback.
4. **Error Handling**
    - Invalid requests return appropriate error messages.
    - Proper HTTP status codes (400, 401, 403, 404, 500) are used.
5. **Security**
    - Permissions enforce proper access control.
    - Unauthorized users cannot modify others' content.

---

## 📚 Security Considerations

-   **Environment Variables:**

    -   All sensitive credentials (DB URL, secret keys, JWT secrets) are stored in **environment variables**.
    -   `.env` files are used locally but are **never committed** to GitHub.

-   **Permissions & Authentication:**

    -   Role-based access control prevents unauthorized actions.
    -   JWT authentication ensures secure API access.

-   **CORS Handling:**

    -   Django CORS Headers ensures controlled cross-origin access.
    -   Only whitelisted domains can interact with the API.

-   **Debug Mode:**
    -   `DEBUG = False` in production to prevent leaks of sensitive information.

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

---
