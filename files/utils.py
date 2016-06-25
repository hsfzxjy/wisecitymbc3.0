from django.conf import settings
from qiniu import Auth, BucketManager, put_file


def _extract(name):
    return getattr(settings, name, '')

access_key = _extract('QINIU_ACCESS_KEY')
secret_key = _extract('QINIU_SECRET_KEY')
bucket_name = _extract('QINIU_BUCKET_NAME')
domain_name = _extract('QINIU_DOMAIN_NAME')


def get_auth():
    return Auth(access_key, secret_key)


def get_bucket():
    return BucketManager(get_auth())


def get_upload_token():
    return get_auth().upload_token(bucket_name)


def delete_file(key):
    bucket = get_bucket()
    bucket.delete(bucket_name, key)


def get_mime_type(key):
    bucket = get_bucket()
    return bucket.stat(bucket_name, key)[0]['mimeType']


def upload_file(file):
    """Only for testing."""

    from os.path import basename
    from datetime import datetime

    key = '%s/%s' % (datetime.now().timestamp(), basename(file))
    token = get_auth().upload_token(bucket_name, key, 3600)

    ret, info = put_file(token, key, file)

    return ret['key']
