from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from celery_app import app

Base = declarative_base()

engine = create_engine(app.conf.SQLALCHEMY_DATABASE_URI)

Session = orm.sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()
