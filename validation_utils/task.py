import requests
import sentry_sdk
import settings
from celery import shared_task
from postgres_db import PostgresService
from datetime import datetime

table = PostgresService(
    user = settings.DATABASES['USER'],
    password = settings.DATABASES['PASSWORD'],
    host = settings.DATABASES['HOST'],
    port = settings.DATABASES['PORT'],
    dbname = settings.DATABASES['NAME'],
    table = 'strongbox.sb_email',
    primarykey = 'email'
)

table.connect()

# @shared_task(name='validate_email')
def validate_email(email, validation_source):
    try:
        url = "{0}/{1}".format(settings.EMAIL_VALIDATION_ENDPOINT, "v1/validate")
        print('-# ', url, email, validation_source, '\n')
        r = requests.post(
            url,
            json={
                "email": email,
                "source": validation_source
            }
        )
        r.raise_for_status()
        validation_data = r.json()['zeroBounceResponse']
        validation_status = validation_data['status']
        validation_sub_status = validation_data.get('sub_status')
        validation_processed_at = validation_data['processed_at']

        #db update
        table.update_multiple_columns(
            columns = ['validated_at', 'validation_status', 'validation_sub_status'],
            columns_value = [validation_processed_at, validation_status, validation_sub_status],
            # columns_value = [datetime.now(), "validated", "sub-validated"],
            primaryKey_value = email
        )
        table.commit()

        table.select_all()
        
    except Exception as e:
        if e.response.status_code != 404:
            sentry_sdk.capture_exception(e)

# @shared_task(name='validation_from_db')
def validation_from_db():
    try:
        subscribers = table.select_where(
            columns = ['email', 'source_table'],
            where_col = 'validation_status',
            where_val = 'un-validated'
        )

        for sub in subscribers:
            validate_email(sub[0], sub[1])
            
    except Exception as e:
        sentry_sdk.capture_exception(e)

validation_from_db()