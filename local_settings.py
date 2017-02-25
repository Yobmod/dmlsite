import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'yobmod@gmail.com'
EMAIL_HOST_PASSWORD = '3Monsters'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SECRET_KEY = 'u8&hn$a@%16^xvg+t5#abg(p6+&+y&qms6!@$cf*$-q3!^lge+'
DEBUG = True


# AWS_STORAGE_BUCKET_NAME = dmlsite
# AWSAccessKeyId=AKIAIXLQVFPOJK5NPYSQ
# AWSSecretKey=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

# Access Key ID:
# AKIAICIVHERX6ZDDFOBA
# Secret Access Key:
# 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

# if not DEBUG:
	# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
	# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
	# AWS_STORAGE_BUCKET_NAME = 'dmlsite'
	# AWS_ACCESS_KEY_ID = 'AKIAICIVHERX6ZDDFOBA'
	# AWS_SECRET_ACCESS_KEY = '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'
