import datetime
import json

from celery_app import app
from database import session
from functionality.send_email import send_email
from logger.logger import logger
import celery
from flask_models.celery import CeleryTask
from flask_models.users import User


class EmailTask(celery.Task):
    def __call__(self, *args, **kwargs):
        logger.info('Task Starting : {0.name} [{0.request.id}]'.format(self))
        super(EmailTask, self).__call__(*args, **kwargs)

    def on_success(self, retval, task_id, args, kwargs):
        super(EmailTask, self).on_success(retval, task_id, args, kwargs)
        logger.info('Task Completed Successfully : Task Name - {0}, args - {1}, id - {2}'.format(
            self.request.task, args, self.request.id
        ))
        email = (json.loads(args[0])).get('email')

        user_id = session.query(User.id).filter(User.email == email).first()
        if not user_id:
            raise ValueError("Enter-Valid-Email")
        try:
            celery_task_obj = CeleryTask(
                user_id=int(user_id[0]),
                task_module=self.request.task,
                payload_data=email,
                task_status='COMPLETED',
                started_on=datetime.datetime.now(),
                task_id=self.request.id,
            )
            session.add(celery_task_obj)
            session.commit()
        except Exception as e:
            logger.info("Insertion Failed with - {}".format(str(e)))
            session.rollback()
            session.remove()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        super(EmailTask, self).on_failure(exc, task_id, args, kwargs, einfo)
        logger.info('Task Failed : Task Name - {0}, args - {1}, id - {2}, stack_trace - {3}'.format(
            self.request.task, args, self.request.id, einfo
        ))
        email = (json.loads(args[0])).get('email')

        user_id = session.query(User.id).filter(User.email == email).first()
        if not user_id:
            raise ValueError("Enter-Valid-Email")
        try:
            celery_task_obj = CeleryTask(
                user_id=int(user_id[0]),
                task_module=self.request.task,
                payload_data=email,
                task_status='EXCEPTION',
                started_on=datetime.datetime.now(),
                task_id=self.request.id,
            )
            session.add(celery_task_obj)
            session.commit()
        except Exception as e:
            logger.info("Insertion Failed with - {}".format(str(e)))
            session.rollback()
            session.remove()


@app.task(base=EmailTask)
def send_async_email(json_data):
    logger.info('json_data is - {}'.format(json_data))
    json_data = json.loads(json_data)
    send_email(**json_data)
