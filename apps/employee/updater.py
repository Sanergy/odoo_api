import xmlrpc.client
import logging
from odooapi import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apps.employee import syncData


logger = logging.getLogger(__name__)

def start():
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(sync, 'interval', seconds=10)
    scheduler.start()

