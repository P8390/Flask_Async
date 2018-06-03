from celery_worker import send_async_email
import json

payload = {
    'email': 'pankaj@screen-magic.com'
}

send_async_email.delay(json.dumps(payload))
