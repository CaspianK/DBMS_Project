from flask import Flask
import os
import sys
import cx_Oracle

def init_session(connection, requestedTag_ignored):
    cursor = connection.cursor()
    cursor.execute("""
        ALTER SESSION SET
        TIME_ZONE = 'UTC'
        NLS_DATE_FORMAT = 'YYY-MM-DD HH24:MI'
    """)

def start_pool():
    os.environ['PYTHON_USERNAME'] = 'Project'
    os.environ['PYTHON_PASSWORD'] = '52341'
    os.environ['PYTHON_CONNECTSTRING'] = 'Laptop-Caspian'
    pool_min = 4
    pool_max = 4
    pool_inc = 0
    pool_gmd = cx_Oracle.SPOOL_ATTRVAL_WAIT

    print("Connecting to", os.environ.get("PYTHON_CONNECTSTRING"))

    pool = cx_Oracle.SessionPool(user=os.environ.get("PYTHON_USERNAME"),
                                  password=os.environ.get("PYTHON_PASSWORD"),
                                  dsn=os.environ.get("PYTHON_CONNECTSTRING"),
                                  min=pool_min,
                                  max=pool_max,
                                  increment=pool_inc,
                                  threaded=True,
                                  getmode=pool_gmd,
                                  sessionCallback=init_session)
    return pool

pool = start_pool()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'woefubinenqoqirbio'

    from .views import views
    app.register_blueprint(views, url_prefix='/')
    
    # pool = start_pool()

    return app