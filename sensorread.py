import mysql.connector
from si7021 import SI7021
import time

sensor=SI7021()

config = {
	'user': 'bone',
	'password': 'bone',
	'host': 'localhost',
	'database': 'agrowsoftdb',
	'raise_on_warnings': False,
}

while True:
	time.sleep(5)
	rh, temp = sensor.get_readings()
	#temp = sensor.get_temp()
	#rh = sensor.get_rel_humidity()
	print(temp)
	print(rh)
	try:
		query = ("UPDATE settings set var = %s where ID = %s")
		args = temp, 77
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		cursor.execute(query,args)
		query = ("UPDATE settings SET var=%s where ID=%s")
		args = rh, 78
		cursor.execute(query,args)
		cursor.close()
		cnx.close()
	except:
		pass