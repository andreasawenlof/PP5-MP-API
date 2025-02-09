# ✅ Backend Testing Documentation

## 🛠 Automated Unit Tests

The backend was tested using Django’s built-in test framework.

```sh
(.venv) python manage.py test mp_api.tests.test_auth
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

```sh
(.venv) (.venv) mztr@Mac PP5-MP-API % python manage.py test mp_api.tests.test_auth
Found 9 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....===== In CustomLogoutView! =====
===== request.data: {'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTE1NDQ4MCwiaWF0IjoxNzM5MDY4MDgwLCJqdGkiOiIxZWIwYWU5YjBiY2I0MzVjYWU5YmI1OTUwNDYyNWFlYSIsInVzZXJfaWQiOjF9.tol4vugW0cmYGsjEDBGIu9HboMRf1RUWE2fIqfQoK4I'} =====
...===== In CustomLogoutView! =====
===== request.data: {'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczOTE1NDQ4NywiaWF0IjoxNzM5MDY4MDg3LCJqdGkiOiJiNGZlZWRjNzExMWM0ZjY1OThjZDQxNTQzNjA2ZTA4NiIsInVzZXJfaWQiOjF9.ReGuFYRSty6ZwaadROOjuhlX4jyKk0ObsAvAuI_9flc'} =====
..
----------------------------------------------------------------------
Ran 9 tests in 14.474s

OK
Destroying test database for alias 'default'...
(.venv) (.venv) mztr@Mac PP5-MP-API %
```

## 🛠 Endpoint Tests

---

![Login](documents/tests/login.png)
![Trackslist](documents/tests/trackslist.png)
![Tracks Create](documents/tests/trackscreate.png)
![Tracks Edit](documents/tests/tracksedit.png)
![Tracks Delete](documents/tests/tracksdelete.png)
![Commentslist](documents/tests/commentsget.png)
![Comments Update](documents/tests/commentsupdate.png)
![Comments Delete](documents/tests/commentsdelete.png)
![Profileslist](documents/tests/profilesget.png)
![Profile Edit](documents/tests/profileupdate.png)
![Moods List](documents/tests/genresget.png)
![Genres List](documents/tests/moodsget.png)
![Project Types List](documents/tests/projecttypesget.png)
![Instruments List](documents/tests/instrumentsget.png)

## 🔥 Known Issues

-   **Currently, there is no feedback when a user fails to log in due to invalid credentials.**  
    **Fix:** Add a feedback message in the app.

-   **When trying to access a specific profile while logged out, a 500 error occurs due to 'AnonymousUser' object has no attribute 'profile'.**  
    **Fix (Workaround):** Redirect the user to a 404 page instead. The actual fix would be resolving the crash, but the user should still be redirected to a 404 page as it currently is.

-   **Couldn’t fetch profile, received a 500 error.**  
    **Fix:** Profile detail needed `queryset = objects.all()`.

-   **Logged-in users can only comment on tracks they own, not all of them.**  
    **Fix:** There was an issue in the API view that needed adjustment. On the frontend, the conditional in `TrackDetails` had `CommentComponent` included only for owners.  
    **Fixed by moving it outside of that restriction.**

-   **Refresh Tokens**:

    -   Manually fetching refresh tokens works in tests, but automatic renewal causes session issues.
    -   **Solution/Workaround:** Access tokens are set to **30 days** instead.
