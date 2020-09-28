import logging
import time
import datetime
import sqlite3
from datetime import timedelta
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

#########################################################	

logging.basicConfig(handlers = [logging.FileHandler('log/age-db.log'), logging.StreamHandler()],level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#logging.basicConfig(handlers = [logging.FileHandler('log/age-db.log'), logging.StreamHandler()], level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

age_IOCs_inactive_for_days = cfg['age_IOCs_inactive_for_days']

now = datetime.datetime.utcnow()
deleteOlderThan= (now - timedelta(days=age_IOCs_inactive_for_days)).isoformat(timespec='seconds')

#########################################################

def initSQLlite():
	conn = sqlite3.connect('IOCs.db')
	logging.info('Opened database successfully')

	return conn

#########################################################

def ageDB(conn,deleteOlderThan):
	cur = conn.cursor()
	cur.execute('select * from iocs where last_seen <"'+deleteOlderThan+'"')
	rows = cur.fetchall()
	for row in rows:
		logging.debug(row)
		
	cur.execute('select * from iocs where last_seen <"'+deleteOlderThan+'"')
	conn.commit()
	logging.info('Aging database successfully - removed {}'.format(len(rows)))

#########################################################

conn = initSQLlite()
ageDB(conn,deleteOlderThan)
