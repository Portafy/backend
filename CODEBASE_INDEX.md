# Codebase Index — PDF-to-Website (Portafy Backend)

Repository root: c:/Users/ms/Desktop/Internships/Collaborations/Amira/Pdf-to-Website

- Stack: Django 5.2, Django REST Framework, SimpleJWT, PostgreSQL, Celery (used in code), CORS.
- Project root for backend: Backend/Portafy
- Apps: accounts, pdfs, websites, payments, core

## High-level Architecture

- Monolithic Django project `config` with DRF APIs.
- JWT authentication via SimpleJWT (Authorization header type is `JWT`, not `Bearer`).
- CORS enabled for all origins in dev.
- PostgreSQL DB configured by default.
- Static served from `Backend/Portafy/static/` and media from `Backend/Portafy/media/` in dev.
- Celery app configured; background tasks defined in `core.tasks` and `pdfs.tasks`.

## Settings Overview

File: Backend/Portafy/config/settings/base.py
- DEBUG: True (development)
- ALLOWED_HOSTS: []
- INSTALLED_APPS:
  - Django core: admin, auth, contenttypes, sessions, messages, staticfiles
  - Third-party: corsheaders, drf_yasg, rest_framework, django_filters, debug_toolbar, rest_framework_simplejwt, rest_framework_simplejwt.token_blacklist
  - Local apps: accounts, pdfs, core, websites, payments
- MIDDLEWARE: includes `corsheaders` and `debug_toolbar`
- ROOT_URLCONF: config.urls
- Templates: DIRS = [BASE_DIR/templates/]
- REST_FRAMEWORK:
  - Auth: JWT
  - Permission: AllowAny (override in views/permissions)
  - Filter backends: DjangoFilterBackend
- SIMPLE_JWT:
  - ACCESS_TOKEN_LIFETIME: 1 day
  - REFRESH_TOKEN_LIFETIME: 7 days
  - AUTH_HEADER_TYPES: ("JWT",)
- Database (default):
  - ENGINE: django.db.backends.postgresql
  - NAME: portafy_db, USER: root, PASSWORD: pass123, HOST: localhost, PORT: 5432
- Auth:
  - AUTH_USER_MODEL: accounts.User (email as username)
- Static/Media:
  - MEDIA_URL = /media/, MEDIA_ROOT = BASE_DIR/media
  - STATIC_URL = /static/, STATICFILES_DIRS = [BASE_DIR/static]

Environment-specific settings:
- config/settings/dev.py, config/settings/prod.py (not detailed here)

## Dependencies (Backend/requirements/base.txt)

Runtime highlights:
- Django, djangorestframework, djangorestframework_simplejwt, django-filter
- django-cors-headers, django-debug-toolbar, drf-yasg
- pillow, psycopg2-binary, whitenoise
- python-decouple, python-magic

Dev/Tooling:
- black, isort, pre_commit, coverage, pytest-django

Note:
- Celery and google-generativeai are referenced in code but not listed in base.txt; ensure they are added to requirements where appropriate.

## URL Map (Top-level)

File: Backend/Portafy/config/urls.py
- /admin/ — Django admin
- /accounts/ — include(accounts.urls)
- /pdfs/ — include(pdfs.urls)
- /websites/ — include(websites.urls)
- /payments/ — include(payments.urls)
- /__debug__/ — Django Debug Toolbar
- Dev static/media serving via `static()` helpers

## APIs by App

### accounts

Models: Backend/Portafy/accounts/models.py
- User(AbstractUser)
  - email unique, phone unique
  - USERNAME_FIELD = "email", REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone"]
- Customer(models.Model)
  - OneToOne(User), subscription (F/B/P/PR), profile_picture

Serializers: Backend/Portafy/accounts/serializers.py
- UserSerializer (creates users via `create_user`)
- UserProfileSerializer (adds website_count via `obj.websites.count()`)

Views: Backend/Portafy/accounts/views/auth_views.py and user_views.py
- LoginView (TokenObtainPairView) — returns tokens + user
- RegisterView (CreateAPIView) — creates user + returns tokens + user
- LogoutView (TokenRefreshView) — blacklists refresh token
- UserProfileView — profile info (in user_views.py)

URLs: Backend/Portafy/accounts/urls.py
- POST /accounts/token/refresh/ — refresh JWT
- POST /accounts/auth/login/ — obtain tokens
- POST /accounts/auth/register/ — create user + tokens
- POST /accounts/auth/logout/ — blacklist refresh token
- GET /accounts/user/profile/ — user profile
Auth notes:
- Header: Authorization: `JWT <access_token>`

### pdfs

Model: Backend/Portafy/pdfs/models.py
- UploadedFile
  - user (FK User), file (PDF-only via FileExtensionValidator + size validator)
  - content (JSON), filename (auto from file slug), uploaded_at (indexed)
  - save() sets `filename` if missing

Views: Backend/Portafy/pdfs/views.py
- FileViewSet (ModelViewSet) — parser MultiPart/Form, permission IsOwner
- FileExtractView (RetrieveAPIView) — returns extracted/processed content
Permissions:
- `core.permissions.IsOwner` (object must belong to user)

URLs: Backend/Portafy/pdfs/urls.py
- Router on "" -> FileViewSet
  - GET /pdfs/ — list own files
  - POST /pdfs/ — upload new PDF (multipart)
  - GET /pdfs/{id}/, PUT/PATCH /pdfs/{id}/, DELETE /pdfs/{id}/
- GET /pdfs/extract/{pk}/ — extract/process selected file

Background tasks: Backend/Portafy/pdfs/tasks.py
- process_pdf(pdf_path) [shared_task]
  - extract_text_blocks -> Gemini via `core.utils.gemini_api(PROMPT...)`
  - Returns string or ValidationError message

### websites

Models: Backend/Portafy/websites/models.py
- WebsiteContent: user FK, content JSON, created_at
- ThemeConfig: optional user FK (custom themes), name unique, theme [dark|light], template_type [minimal|creative], config JSON; cannot delete if in use
- Website:
  - user FK, file (OneToOne UploadedFile), theme FK, content (OneToOne WebsiteContent)
  - unique_id (UUID, indexed), slug unique, title, created_at
  - save() auto-slug: `{username}-{slugify(title)}-{uuid[:8]}`
  - get_absolute_url -> `websites:live_site` by slug

Views: Backend/Portafy/websites/views.py
- WebsiteViewSet (ModelViewSet), permission IsOwnerOrAdminOrReadOnly
- LiveSiteView (RetrieveAPIView, AllowAny) — public website by slug

URLs: Backend/Portafy/websites/urls.py
- Router on "" -> WebsiteViewSet
  - /websites/ and /websites/{id}/ (CRUD)
- GET /websites/live/{slug}/ — public read

### payments

Models: Backend/Portafy/payments/models.py
- Payment(models.Model) — user FK, website FK, email, amount, is_successful, payment_gateway, reference_id (unique), timestamps

Services: Backend/Portafy/payments/chapa.py
- initialize(tx_ref, amount, currency, email, ...) — returns checkout_url
- verify(tx_ref) — returns success flag and raw response

Serializers: Backend/Portafy/payments/serializers.py
- InitiatePaymentSerializer, VerifyPaymentSerializer

Views: Backend/Portafy/payments/views.py
- POST /payments/initiate/ (auth) — starts Chapa payment, returns { checkout_url, tx_ref }
- POST /payments/verify/ (auth) — verifies tx_ref for current user, marks Payment successful
- POST /payments/webhook/chapa/ (public) — Chapa server callback; verifies and marks Payment successful

URLs: Backend/Portafy/payments/urls.py
- app_name = "payments"; routes registered as above

Environment:
- CHAPA_SECRET_KEY — required
- CHAPA_BASE_URL — optional, defaults to https://api.chapa.co

Dependencies:
- requests added in Backend/requirements/base.txt

Example (initiate):
- Header: Authorization: JWT <access_token>
- Body:
  {"website_id": 1, "email": "user@example.com", "amount": "500.00", "currency": "ETB", "return_url": "http://localhost:3000/after-pay"}

Example curl:
```bash
curl -X POST http://localhost:8000/payments/initiate/ \
  -H "Authorization: JWT <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{ "website_id": 1, "email": "user@example.com", "amount": "500.00", "currency": "ETB" }'
```

Webhook:
- Configure Chapa dashboard webhook to POST to http://<host>/payments/webhook/chapa/
- Endpoint is unauthenticated and verifies via Chapa verify API

### core

Permissions: Backend/Portafy/core/permissions.py
- IsOwner, IsOwnerOrReadOnly, IsOwnerOrAdmin, IsOwnerOrAdminOrReadOnly

Tasks: Backend/Portafy/core/tasks.py
- gemini_api(message: str) [shared_task]
  - Uses google.generativeai GenerativeModel("gemini-pro")
  - API key via `decouple.config("GEMINI_API_KEY")`

Utilities: Backend/Portafy/core/utils.py (not detailed here)

## Celery

- App config: Backend/Portafy/config/celery.py
  - DJANGO_SETTINGS_MODULE default: `config.settings.dev`
  - app = Celery('config'); `config_from_object('django.conf:settings', namespace='CELERY')`
  - `app.autodiscover_tasks()`, `debug_task` helper
- Tasks defined in:
  - core.tasks.gemini_api
  - pdfs.tasks.process_pdf

Broker/backend settings are not shown in settings files; ensure to configure `CELERY_*` variables per environment.

## Tests

- Backend/Portafy/accounts/tests/test_auth_views.py — tests for auth flows
- Placeholder test modules exist in other apps: `payments/tests.py`, `pdfs/tests.py`, `websites/tests.py`, `core/tests.py`

## Notable Implementation Details and Constraints

- Uploaded files limited to PDFs; size validator in `pdfs/validators.py`.
- Public site endpoint is read-only and anonymous: `/websites/live/{slug}/`.
- Media/static served via Django during development in `config/urls.py`.
- Debug toolbar mounted at `/__debug__/`.

## Gaps / TODOs Observed

- Requirements likely missing: `celery`, `google-generativeai`. Consider adding to appropriate requirements file(s).
- `payments` URLs not wired; verify `payments/views.py` and add endpoints as needed.
- SECURITY: DEBUG=True, CORS_ALLOW_ALL_ORIGINS=True, and sensitive DB defaults are for dev only; lock down in prod.
- SIMPLE_JWT uses `JWT` header type; ensure frontend aligns.

## Quick Start (Dev)

- Install Python dependencies from `Backend/requirements/dev.txt` (or `base.txt`).
- Ensure PostgreSQL running with a DB matching settings or override via environment.
- Run migrations and dev server from `Backend/Portafy`:
  - python manage.py migrate
  - python manage.py runserver
- Celery (example):
  - celery -A config worker -l info
  - Ensure `GEMINI_API_KEY` set if using Gemini tasks.
