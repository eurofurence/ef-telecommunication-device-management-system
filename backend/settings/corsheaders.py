import environ

env = environ.Env()

if env('EFTDMS_DJANGO_DEBUG', cast=bool, default=False):
    CORS_ALLOWED_ORIGINS = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://localhost:8080',
        'http://127.0.0.1:8080',
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        env('EFTDMS_DJANGO_BASE_URL'),
    ]

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)
