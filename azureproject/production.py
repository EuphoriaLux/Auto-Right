import os

# Add your custom host(s) here
additional_allowed_hosts = ['power-up.lu']
additional_csrf_trusted_origins = ['https://power-up.lu']

# Configure the domain name using the environment variable
# that Azure automatically creates for us.
azure_host = os.environ.get('WEBSITE_HOSTNAME')
if azure_host:
    ALLOWED_HOSTS = [azure_host] + additional_allowed_hosts
    CSRF_TRUSTED_ORIGINS = ['https://' + azure_host] + additional_csrf_trusted_origins
else:
    ALLOWED_HOSTS = additional_allowed_hosts
    CSRF_TRUSTED_ORIGINS = additional_csrf_trusted_origins

DEBUG = True

# WhiteNoise configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Add whitenoise middleware after the security middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # add locale
    'django.middleware.locale.LocaleMiddleware',
    # add locale
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR / 'locale/'),  # Assuming your locale files will be in the "locale" directory of your project
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Configure Postgres database based on connection string of the libpq Keyword/Value form
# https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conn_str_params['dbname'],
        'HOST': conn_str_params['host'],
        'USER': conn_str_params['user'],
        'PASSWORD': conn_str_params['password'],
    }
}
