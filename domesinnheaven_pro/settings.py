"""
Django settings for domesinnheaven_pro project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
# WARNING: Keep secret key, passwords, and API keys secret in production!
SECRET_KEY = 'your-secret-key-here-change-in-production'
DEBUG = True  # Changed to False for production safety
ALLOWED_HOSTS = ['*']

# APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'domesinnheaven_app',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

WHITENOISE_MANIFEST_STRICT = False

ROOT_URLCONF = 'domesinnheaven_pro.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'domesinnheaven_app.context_processors.google_reviews',
                'domesinnheaven_app.context_processors.footer_packages',
                'domesinnheaven_app.context_processors.admin_unread_contacts',
                'domesinnheaven_app.context_processors.recaptcha_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'domesinnheaven_pro.wsgi.application'

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONAL
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# EMAIL - REPLACE WITH YOUR CREDENTIALS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-host.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@your-domain.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# GOOGLE REVIEWS
GOOGLE_REVIEW_RATING = 4.7
GOOGLE_REVIEW_COUNT = 900
GOOGLE_REVIEW_URL = "https://www.google.com/travel/search?q=domesinnheaven_pro%20camping%20reviews"

# RECAPTCHA - REPLACE WITH YOUR KEYS
RECAPTCHA_SITE_KEY = "6LdDzNksAAAAACA5R9MhWkyiuXRP1JnAQKwm00Ou"
RECAPTCHA_SECRET_KEY = "6LdDzNksAAAAAOnJqfhpuEXemB91WRqFy16yO8TA"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cloudinary (hardcoded for clips delivery)
# Upload your clips into: domes/clips/<sequence-number>/ezgif-frame-XXX.<ext>
CLOUDINARY_CLOUD_NAME = "dwyxmxume"
CLOUDINARY_BASE_DELIVERY_URL = f"https://res.cloudinary.com/{CLOUDINARY_CLOUD_NAME}/image/upload"
CLOUDINARY_CLIPS_BASE_URL = f"{CLOUDINARY_BASE_DELIVERY_URL}/f_auto,q_auto/domes/clips"
