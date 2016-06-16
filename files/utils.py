from django.conf import settings
from qiniu import Auth

access_key = getattr(settings, 'QINIU_ACCESS_KEY', '')
secret_key = getattr(settings, 'QINIU_SECRET_KEY', '')
bucket_name = getattr(settings, 'QINIU_BUCKET_NAME', '')


def get_upload_token():
    return Auth(access_key, secret_key).upload_token(bucket_name)
