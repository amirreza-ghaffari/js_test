# ======= MatterMost =========

MATTERMOST_SERVER_URL = "https://im.dkservices.ir"
MM_USERNAME = 'digikalacrisis.softw'
MM_PASSWORD = '4AXc@xEbskZRrrF'
MM_TOKEN = "wcwz775tpbye7rg9m4cwqtr6ao"


# ======= Caller and SMS Panel =========
CALLER_SERVER_AUTH_KEY = "api-key"
CALLER_SERVER_AUTH_VALUE = ",/nh<*tqbJs0-)="
SMS_PANEL_PASSWORD = 'Basic ZGlnaV9IUi9kaWdpa2FsYTpIR1BEU0lOTmxwQXRjeVlL'

# ======= Postgres =========
DB_USER = "bcm_user"
DB_PASS = "bcm_user"
DB_NAME = "bcm"
DB_PORT = "5432"
DB_HOST = "localhost"

# ======= Celery =========

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

# ======= Email =========

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.digikala.com'
EMAIL_HOST_USER = 'Crisis.software@digikala.com'
EMAIL_HOST_PASSWORD = 'qazQAZ123!@#'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
