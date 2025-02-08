# Track Management API - Backend README

## 🎵 Overview

This is a **Track Management API** designed for composers and reviewers to efficiently manage tracks, albums, instruments, and track statuses. The API enables:

-   **Track creation, editing, and deletion** (by composers only)
-   **Comment system** for feedback and collaboration
-   **Review system** (future implementation)
-   **Filtering and searching** by genre, mood, status, project type, and vocals needed
-   **Role-based access control** (Composers vs. Reviewers)

This API is built to scale with additional features like **album bulk updates, reviews, and audio file imports** in future releases.

---

## 🚀 Features

-   **Tracks:** CRUD operations with status management
-   **Comments:** Threaded discussions per track
-   **Review System:** (Planned) Feedback & revision tracking for composers
-   **Albums:** Group tracks, add cover art, and manage updates
-   **Filtering & Search:** Quickly locate tracks based on metadata
-   **Authentication:** Secure JWT-based authentication with role-based permissions

---

## 🛠 Tech Stack

-   **Backend:** Django 4.2, Django REST Framework
-   **Database:** PostgreSQL
-   **Authentication:** dj-rest-auth with JWT tokens
-   **Deployment:** (Specify if deployed)
-   **Other Tools:** Django Filters, Django CORS Headers, Celery (if applicable)

---

## 🏗 Setup & Installation

### 1️⃣ Clone the Repository

```sh
git clone <repo_url>
cd backend
```

### 2️⃣ Create and Activate Virtual Environment

```sh
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables

Create a `.env` file in the root directory and add:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-database-url
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### 5️⃣ Apply Migrations & Create Superuser

```sh
python manage.py migrate
python manage.py createsuperuser
```

### 6️⃣ Run the Development Server

```sh
python manage.py runserver
```

---

## 🔬 Testing

Unit tests were run to verify authentication and role-based access. Example test output:

```sh
(.venv) mztr@Mac PP5-MP-API % python manage.py test mp_api.tests.test_auth
Found 9 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....===== In CustomLogoutView! =====
===== request.data: {'refresh_token': '...'} =====

----------------------------------------------------------------
Ran 9 tests in 14.750s

OK
Destroying test database for alias 'default'...
```

### **Tested Scenarios:**

✅ Authentication (Login/Logout) works correctly
✅ CRUD operations for Tracks & Comments
✅ Role-based access (Composers vs. Reviewers)
✅ Non-authorized users **cannot** access or modify tracks
✅ Tracks list displays correctly with filters & search

---

## 🔥 Known Issues

1. **Refresh Tokens**:

    - Manually fetching refresh tokens works in tests, but automatic renewal causes session issues.
    - **Solution:** Access tokens are set to **30 days** instead.

2. **Instrument Editing Issue**:
    - Tracks can be **created** with instruments but **not edited** with them currently.
    - **Planned Fix:** Future patch.

---

## 🚀 Future Enhancements

-   **Review System**: Allow reviewers to provide structured feedback.
-   **Audio File Upload**: Composers can attach preview tracks.
-   **Better Search & Filters**: More granular search capabilities.
-   **Bulk Album Edits**: Manage track statuses quickly.

---

## 📌 API Endpoints

(TBD: Auto-generate API documentation from Django REST Framework or Swagger)

---

## 🎯 Conclusion

This API is built for **speed, efficiency, and scalability**, ensuring a smooth workflow for composers and reviewers in the music industry. The backend is structured with **future growth in mind**, making it easy to add new features as needed.

---

**✅ Backend DONE. Next Up: Frontend README.**

🔥 Let’s go.
