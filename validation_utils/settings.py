import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

EMAIL_VALIDATION_ENDPOINT = os.environ.get(
    "EMAIL_VALIDATION_FQDN", default=""
)

DATABASES = {
    'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
    'NAME': os.environ.get('DATABASE_NAME', 'postgres'),
    'USER': os.environ.get('DATABASE_USER', 'postgres'),
    'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'postgres'),
    'PORT': os.environ.get('DATABASE_PORT', '5432')
}