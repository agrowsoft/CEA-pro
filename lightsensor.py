import time
import mysql.connector 
from tsl2561 import TSL2561

LightSensor = TSL2561()


config = {
	'user': 'bone',
	'password': 'bone',
	'host': 'localhost',
	'database': 'agrowsoftdb',
	'raise_on_warnings': False,
}


while True:
    time.sleep(5)
    try:
	light =  LightSensor.lux()
	print (light)
    except:
        pass

    try:
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("UPDATE settings SET var=%s where ID=%s")
	args = light, '150'
	cursor.execute(query,args)
 	
	cursor.execute(query)
	cursor.close()
	cnx.close()

    except:
        pass

	
