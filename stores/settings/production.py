from .base import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = Config('EMAIL_HOST')
EMAIL_PORT = Config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = Config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = Config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False