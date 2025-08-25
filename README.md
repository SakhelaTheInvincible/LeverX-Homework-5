## Learning Platform API (Django + DRF)

Production-grade REST API for courses, lectures, homework and grading. Auth via JWT. Roles: Teacher/Student. Clean architecture, strong permissions, pagination, filtering, throttling, OpenAPI docs.

### Stack
- Django 5, Django REST Framework
- MySQL (production), SQLite in tests
- JWT auth via SimpleJWT
- drf-spectacular (OpenAPI 3 schema + Swagger UI)
- UV for dependency and environment management
- pytest (+ xdist, cov) for tests

### Project Layout
```
api/            # Django project
users/          # Custom user model, auth endpoints
courses/        # Courses and lectures
homework/       # Assignments, submissions, grades, comments
tests/          # Shared factories, fixtures, smoke tests
```

### Quickstart (Windows PowerShell)
1) Install dependencies
```
uv sync --dev
```
2) Configure MySQL and create database (example: `leverx_db`).
3) Create `.env` file in project root (see below).
4) Migrate DB
```
uv run python manage.py migrate --run-syncdb
```
5) Run server
```
uv run python manage.py runserver
```
6) (Optional) Create admin user
```
uv run python manage.py createsuperuser
```

### Environment (.env)
```
DEBUG=true
DJANGO_SECRET_KEY=change-me
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=leverx_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306

THROTTLE_RATE_ANON=60/min
THROTTLE_RATE_USER=120/min
```

### API Documentation
- Schema: `/api/schema/`
- Swagger UI: `/api/docs/`

### Authentication
- Register: `POST /api/v1/auth/register/` with JSON `{username, password, role}` where `role` in `teacher|student`.
- Login: `POST /api/v1/auth/login/` -> returns `{access, refresh}`.
- Refresh: `POST /api/v1/auth/refresh/`.
- Current user: `GET /api/v1/auth/me/` (JWT required).

### Key Endpoints (v1)
- Courses: `GET/POST /api/v1/courses/`, `GET/PATCH/DELETE /api/v1/courses/{id}/`
  - Manage members: `POST /api/v1/courses/{id}/add-student/{user_id}/`, `POST /api/v1/courses/{id}/remove-student/{user_id}/`, `POST /api/v1/courses/{id}/add-teacher/{user_id}/`
- Lectures (nested): `GET/POST /api/v1/courses/{course_id}/lectures/`
- Homework assignments: `GET/POST /api/v1/courses/{course_id}/lectures/{lecture_id}/homework/`
- Submissions: `GET/POST /api/v1/courses/{course_id}/lectures/{lecture_id}/homework/{assignment_id}/submissions/`
- Grades: `GET/POST /api/v1/courses/{course_id}/lectures/{lecture_id}/homework/{assignment_id}/grades/`
- Grade comments: `GET/POST /api/v1/courses/{course_id}/lectures/{lecture_id}/homework/{assignment_id}/grades/{grade_id}/comments/`

### Permissions Model
- All endpoints require authentication by default.
- Teachers (course owner or teacher):
  - CRUD their courses
  - Add/remove students; add teachers
  - CRUD lectures in their courses
  - Create homework assignments, grade submissions, and comment on grades
- Students:
  - View available/enrolled courses and lectures
  - View homework
  - Submit homework for enrolled courses
  - View their submissions and grades; comment on grades

### Pagination, Filtering, Search, Ordering
- Pagination: PageNumberPagination; `?page=` params, page size 10 default
- Filtering: `?name=...` on courses; lecture/homework endpoint filters included
- Search: Courses by `name,description`; Lectures by `topic`
- Ordering: Courses by `created_at,updated_at,name`; Lectures by `created_at,updated_at,topic`

### Throttling
- Anonymous: `THROTTLE_RATE_ANON` (default `60/min`)
- Authenticated: `THROTTLE_RATE_USER` (default `120/min`)

### Testing (pytest)
- Install dev deps: `uv sync --dev`
- Run tests: `uv run pytest -q`
- Coverage + parallel: `uv run pytest -q -n auto --cov`
- Test DB: SQLite in-memory for speed

### Local Tips
- Windows firewall/port prompts may appear on first run
- If MySQL client errors occur, ensure server is running and `.env` credentials are correct
- File uploads (lecture presentation) saved to `media/presentations/`

### Design Notes
- `users.User` is custom with `role` and helpers `is_teacher()` / `is_student()`
- Clean separation: viewsets delegate membership logic to `courses/services.py`
- Strong queryset scoping and create-time permission checks
- URL path versioning: all endpoints under `/api/v1/`

