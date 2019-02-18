#7.1.2.1.4
#new pinout
#bbgreen
#light sensor as service

import sys, os
import Adafruit_BBIO.GPIO as GPIO
import thread
import time
import mysql.connector 
from array import *
import datetime
import urllib2
import urllib
import socket
import shutil

settingsarray = [0]*200

menulevel = 1

#global variables
#global variables
timeout = 1
socket.setdefaulttimeout(timeout)
run = 0
IPMing = 0
accumlight = 0
dailyaccumlight = 0
heating1 = 0
heating2 = 0
cooling1 = 0
cooling2 = 0
cooling3 = 0
cooling4 = 0
rhing = 0
temperature = 0
humidity = 0
light = 0
lightcalc = 0
moles = 0
irrigating = 0
alerting = 0

envname = ''
thezone = '0'
alt = 0

ConnectionError =''



config = {
	'user': 'bone',
	'password': 'bone',
	'host': 'localhost',
	'database': 'agrowsoftdb',
	'raise_on_warnings': False,
}

#pins
heat1pin = 'P8_29'
heat2pin = 'P8_30'
cool1pin = 'P8_31'
cool2pin = 'P8_8'
cool3pin = 'P8_33'
cool4pin = 'P8_34'
rhpin = 'P8_35'
ipmpin = 'P8_36'
w1pin = 'P8_37'
w2pin = 'P8_38'
w3pin = 'P8_39'
w4pin = 'P8_40'
w5pin = 'P8_41'
w6pin = 'P8_42'
#co2pin = 'P8_43'
alertpin = 'P8_44'


time_tuple = ( 2012, # Year
                  9, # Month
                  6, # Day
                  0, # Hour
                 38, # Minute
                  0, # Second
                  0, # Millisecond
              )

def settime(time_tuple):
    import ctypes
    import ctypes.util
    import time

    # /usr/include/linux/time.h:
    #
    # define CLOCK_REALTIME                     0
    CLOCK_REALTIME = 0

    # /usr/include/time.h
    #
    # struct timespec
    #  {
    #    __time_t tv_sec;            /* Seconds.  */
    #    long int tv_nsec;           /* Nanoseconds.  */
    #  };
    class timespec(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long),
                    ("tv_nsec", ctypes.c_long)]

    librt = ctypes.CDLL(ctypes.util.find_library("rt"))

    ts = timespec()
    ts.tv_sec = int( time.mktime( datetime.datetime( *time_tuple[:6]).timetuple() ) )
    ts.tv_nsec = time_tuple[6] * 1000000 # Millisecond to nanosecond

    # http://linux.die.net/man/3/clock_settime
    librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))



def startup():
	global moles
	
	#load variables
	try:
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		query = ("REPAIR TABLE conditions")
		cursor.execute(query)
		cursor.close()
		cursor = cnx.cursor()
		query = ("REPAIR TABLE conditionstemp")
		cursor.execute(query)
		cursor.close()
		cursor = cnx.cursor()
		query = ("REPAIR TABLE controllers")
		cursor.execute(query)
		cursor.close()
		cursor = cnx.cursor()
		query = ("REPAIR TABLE controls")
		cursor.execute(query)
		cursor.close()
		cursor = cnx.cursor()
		query = ("REPAIR TABLE controlstemp")
        	cursor.execute(query)
		cursor.close()
		cursor = cnx.cursor()
		query = ("REPAIR TABLE customer")
		cursor.execute(query)
		cursor.close()
		cursor = cnx.cursor()
		query = ("REPAIR TABLE settings")
		cursor.execute(query)
		cursor.close()
		cnx.close()
		

	except:
		print("Database does not exists")
		


	try:
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		query = ("UPDATE controlstemp set State=0")
		cursor.execute(query)
		cursor.close()
		
		#version
		cursor = cnx.cursor()
		query = ("UPDATE settings set var='4' where ID='47'")
		cursor.execute(query)
		cursor.close()

		#irrigating set to off
		cursor = cnx.cursor()
		query = ("UPDATE settings set var='0' where ID='80'")
		cursor.execute(query)
		cursor.close()

		#dailyaccumlight
		cursor = cnx.cursor()
		query = ("UPDATE settings set var='0' where ID='50'")
		cursor.execute(query)
		cursor.close()

		cursor = cnx.cursor()
		query = ("UPDATE settings set var='0' where ID='80'")
		cursor.execute(query)
		cursor.close()
		cursor = cnx.cursor()
		query = ("select Moles from conditionstemp")
		cursor.execute(query)
		data = cursor.fetchall()
		for row in data:
			moles = row[0]
		cursor.close()
		cnx.close()

	except:			
		print("Database does not exists")
		

	try:
		shutil.copy2('resolv.conf', '/etc/resolv.conf')
	except:
		print("could not copy conf")
	



def setup():

	#load variables
	try:
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()
		query = ("SELECT * from settings order by ID")
		cursor.execute(query)
		data = cursor.fetchall()
		for row in data:
			global envname
			#print row[2]
			if row[0] == 1:
				envname = row[2]

			if row[0] > 1:
				x = row[0]
				y = row[2]
				settingsarray[x] = y
				#print settingsarray[x]
		cursor.close()
		cnx.close()
		
		

	except:
		print("Database does not exists")
		
	else:
		cnx.close()
	

def theloop():
	global run
	global light
	global moles
	global irrigating
	global dailyaccumlight
	while True:
		time.sleep(1)
		
		#print (run)
		if run == '1':
			print("running")

			#heater1
			#find set point
			spt = float(settingsarray[2])
			now = datetime.datetime.now()
			thehour=int(settingsarray[86])
			theminute=int(settingsarray[87])
			setpt1 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[88])
			theminute=int(settingsarray[89])
			setpt2 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[91])
			theminute=int(settingsarray[92])
			setpt3 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[94])
			theminute=int(settingsarray[95])
			setpt4 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			if now >= setpt4:
				spt = float(settingsarray[96])
				#print("4")	
			elif now >= setpt3:
				spt = float(settingsarray[93])
				#print("3")
			elif now >= setpt2:
				spt = float(settingsarray[90])
				#print("2")
			else:	
				spt = float(settingsarray[2])
				#print("1")			
			if temperature < (spt-float(settingsarray[3])):
				x = heater1(1)
			else:
				x = heater1(0)
			
			#heater2
			#find set point
			now = datetime.datetime.now()
			thehour=int(settingsarray[97])
			theminute=int(settingsarray[98])
			setpt1 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[99])
			theminute=int(settingsarray[100])
			setpt2 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[102])
			theminute=int(settingsarray[103])
			setpt3 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[105])
			theminute=int(settingsarray[106])
			setpt4 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			if now >= setpt4:
				spt = float(settingsarray[107])
				#print("4")	
			elif now >= setpt3:
				spt = float(settingsarray[104])
				#print("3")
			elif now >= setpt2:
				spt = float(settingsarray[101])
				#print("2")
			else:	
				spt = float(settingsarray[4])
				#print("1")			
			if temperature < (spt-float(settingsarray[3])):
				x = heater2(1)
                        else:
                                x = heater2(0)
			
			#cooling1
			#find set point
			now = datetime.datetime.now()
			thehour=int(settingsarray[37])
			theminute=int(settingsarray[38])
			setpt1 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[108])
			theminute=int(settingsarray[109])
			setpt2 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[111])
			theminute=int(settingsarray[112])
			setpt3 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[114])
			theminute=int(settingsarray[115])
			setpt4 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			if now >= setpt4:
				spt = float(settingsarray[116])
				#print("4")	
			elif now >= setpt3:
				spt = float(settingsarray[113])
				#print("3")
			elif now >= setpt2:
				spt = float(settingsarray[110])
				#print("2")
			else:	
				spt = float(settingsarray[6])
				#print("1")			
			
			if temperature > (spt+float(settingsarray[5])):
                                x = cool1(1)
                        else:
                                x = cool1(0)

			#cooling2
			#find set point
			now = datetime.datetime.now()
			thehour=int(settingsarray[117])
			theminute=int(settingsarray[118])
			setpt1 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[119])
			theminute=int(settingsarray[120])
			setpt2 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[122])
			theminute=int(settingsarray[123])
			setpt3 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[125])
			theminute=int(settingsarray[126])
			setpt4 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			if now >= setpt4:
				spt = float(settingsarray[127])
				#print("4")	
			elif now >= setpt3:
				spt = float(settingsarray[124])
				#print("3")
			elif now >= setpt2:
				spt = float(settingsarray[121])
				#print("2")
			else:	
				spt = float(settingsarray[7])
				#print("1")			
			
			if temperature > (spt+float(settingsarray[5])):
                                x = cool2(1)
                        else:
                                x = cool2(0)

			#cooling3
			#find set point
			now = datetime.datetime.now()
			thehour=int(settingsarray[128])
			theminute=int(settingsarray[129])
			setpt1 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[130])
			theminute=int(settingsarray[131])
			setpt2 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[133])
			theminute=int(settingsarray[134])
			setpt3 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[136])
			theminute=int(settingsarray[137])
			setpt4 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			if now >= setpt4:
				spt = float(settingsarray[138])
				#print("4")	
			elif now >= setpt3:
				spt = float(settingsarray[135])
				#print("3")
			elif now >= setpt2:
				spt = float(settingsarray[132])
				#print("2")
			else:	
				spt = float(settingsarray[8])
				#print("1")			
			if temperature > (spt+float(settingsarray[5])):
                                x = cool3(1)
                        else:
                                x = cool3(0)
			
			#cooling4
			#find set point
			now = datetime.datetime.now()
			thehour=int(settingsarray[139])
			theminute=int(settingsarray[140])
			setpt1 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[141])
			theminute=int(settingsarray[142])
			setpt2 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[144])
			theminute=int(settingsarray[145])
			setpt3 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			thehour=int(settingsarray[147])
			theminute=int(settingsarray[148])
			setpt4 = now.replace(hour=thehour, minute=theminute, second=0, microsecond=0)
			if now >= setpt4:
				spt = float(settingsarray[149])
				#print("4")	
			elif now >= setpt3:
				spt = float(settingsarray[146])
				#print("3")
			elif now >= setpt2:
				spt = float(settingsarray[143])
				#print("2")
			else:	
				spt = float(settingsarray[9])
				#print("1")			
			if temperature > (spt+float(settingsarray[5])):
                                x = cool4(1)
                        else:
                                x = cool4(0)
			
			#RH
			if humidity > (float(settingsarray[10])):
                                x = rh(1)
                        else:
                                x = rh(0)

			#check irrigation
			if temperature <= 70:
  				vpdtemp = 1.0
  			elif temperature <=74:
  				vpdtemp = 1.05
			elif temperature <=78:
  				vpdtemp = 1.10
			elif temperature <=82:
  				vpdtemp = 1.15
			elif temperature <=86:
  				vpdtemp = 1.15
			elif temperature >86:
  				vpdtemp = 1.20
			
			if humidity >= 78:
   				vpdhumidity = 1.0
			elif humidity >= 68:
				vpdhumidity = 1.05
			elif humidity >= 58:
				vpdhumidity = 1.1
			elif humidity >= 38:
				vpdhumidity = 1.15
			elif humidity < 38:
				vpdhumidity = 1.20
  
			lightcalc = light*.0185/86400*.1*vpdtemp*vpdhumidity;
  			#lightcalc = light*.0185/86400*.1*1*1
  			
			
			if irrigating == 0:
				moles = moles + lightcalc
			if light > 10:
				dailyaccumlight = dailyaccumlight + lightcalc
			else:
				midnighttestor = datetime.datetime.now()
				midnightflag = now.replace(hour=23, minute=59, second=0, microsecond=0)
				if (midnighttestor > midnightflag):
			 		dailyaccumlight = 0
				
			
			if settingsarray[76] == '1':
				#print (moles)
				#print (float(settingsarray[23]))
				if moles >= float(settingsarray[23]):
					irrigating = 1
			if settingsarray[76] == '0':
				hour = int(time.strftime("%H"))
				min = int(time.strftime("%M"))
				sec = int(time.strftime("%S"))
				#print (min)
				for i in xrange(57,71,2):
					#print (i)
					if int(settingsarray[i]) == hour:
						#print (hour)
						#print (settingsarray[i])
						if int(settingsarray[i+1]) == min:
							#print (min)
							#print (settingsarray[i+1])
							if (3 - sec) > 0:
								#print (sec)
								irrigating = 1	
			if settingsarray[76] == '2':
				if moles >= float(settingsarray[23]):
					irrigating = 1
				hour = int(time.strftime("%H"))
				min = int(time.strftime("%M"))
				sec = int(time.strftime("%S"))
				for i in xrange(57,71,2):
					if int(settingsarray[i]) == hour:
						if int(settingsarray[i+1]) == min:
							if (3 - sec) > 0:
								irrigating = 1

			#ipm
			hour = int(time.strftime("%H"))
			min = int(time.strftime("%M"))
			sec = int(time.strftime("%S"))
			if int(settingsarray[73]) == hour:
      				if int(settingsarray[74]) == min:
					global IPMing
					if IPMing == 0:
						if (3 - sec) > 0:
							IPMing = 1
			global alerting
			
			#alerts
			if temperature < float(settingsarray[26]) or temperature > float(settingsarray[27]):
          			#if alerttemp == 0 and :
				#	x = alert(1)
				alerttemp = 1
			else:
				#if alerting == 1:
				#	x = alert(0)
				alerttemp = 0
			#dry contact
			GPIO.setup("P9_41", GPIO.IN)
			#contact = GPIO.input("P9_41")
			#print(contact)
			if GPIO.input("P9_41"):
    				#print("HIGH")
				#if alerting == 0:
				#	x = alert(1)
				alertdry = 1
			else:
    				#print("LOW")
				#if alerting == 1:
				#	x = alert(0)
				#	alerting = 0
				alertdry = 0
          	          
          		if alerttemp == 1 or alertdry == 1:
				if alerting == 0:
					x = alert(1)
					alerting = 1
			if alerttemp == 0 and alertdry == 0:
				if alerting == 1:
					x = alert(0)
					alerting = 0
						
		else:
			print("stopped")
		
							
def heater1(hstate):
	global envname
	global heating1 	
	if hstate == 1:
		if heating1 == 0:
			GPIO.setup(heat1pin, GPIO.OUT)
			GPIO.output(heat1pin, GPIO.HIGH)
			time.sleep(.25)
			GPIO.setup(heat1pin, GPIO.OUT)
			GPIO.output(heat1pin, GPIO.HIGH)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Heater1'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, controlname, '1', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				#print  "senddata"
				x = postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '1', currdate,currtime,currall, controlname
			cursor.execute(query,args)
			cursor.close()
			cnx.close()
			heating1 = 1
	else:
		
		if heating1 == 1:
			GPIO.setup(heat1pin, GPIO.IN)
			time.sleep(.25)
			GPIO.setup(heat1pin, GPIO.IN)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Heater1'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, 'Heater1', '0', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '0', currdate,currtime,currall, controlname
			cursor.execute(query,args)			

			cursor.close()
			cnx.close()
			heating1 = 0

	return 1;


		
							
def heater2(hstate):
	global envname
	global heating2 	
	if hstate == 1:
		if heating2 == 0:
			GPIO.setup(heat2pin, GPIO.OUT)
			GPIO.output(heat2pin, GPIO.HIGH)
			time.sleep(.25)
			GPIO.setup(heat2pin, GPIO.OUT)
			GPIO.output(heat2pin, GPIO.HIGH)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Heater2'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, controlname, '1', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '1', currdate,currtime,currall, controlname
			cursor.execute(query,args)
			cursor.close()
			cnx.close()
			heating2 = 1	
		
	else:
		if heating2 == 1:
			GPIO.setup(heat2pin, GPIO.IN)
			time.sleep(.25)
			GPIO.setup(heat2pin, GPIO.IN)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Heater2'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, controlname, '0', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '0', currdate,currtime,currall, controlname
			cursor.execute(query,args)
			cursor.close()
			cnx.close()
			heating2 = 0
	return 1;

def cool1(hstate):
	global cooling1 
	global envname	
	if hstate == 1:
		if cooling1 == 0:
			GPIO.setup(cool1pin, GPIO.OUT)
			GPIO.output(cool1pin, GPIO.HIGH)
			time.sleep(.25)
			GPIO.setup(cool1pin, GPIO.OUT)
			GPIO.output(cool1pin, GPIO.HIGH)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Cooling1'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, controlname, '1', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '1', currdate,currtime,currall, controlname
			cursor.execute(query,args)
			cursor.close()
			cnx.close()
			cooling1 = 1		
	else:
		if cooling1 == 1:
			GPIO.setup(cool1pin, GPIO.IN)
			time.sleep(.25)
			GPIO.setup(cool1pin, GPIO.IN)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Cooling1'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, controlname, '0', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '0', currdate,currtime,currall, controlname
			cursor.execute(query,args)
			cursor.close()
			cnx.close()
			cooling1 = 0
	return 1;

def cool2(hstate):
	global cooling2 
	global envname	
	if hstate == 1:
		if cooling2 == 0:
			GPIO.setup(cool2pin, GPIO.OUT)
			GPIO.output(cool2pin, GPIO.HIGH)
			time.sleep(.25)
			GPIO.setup(cool2pin, GPIO.OUT)
			GPIO.output(cool2pin, GPIO.HIGH)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Cooling2'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, controlname, '1', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '1', currdate,currtime,currall, controlname
			cursor.execute(query,args)
			cursor.close()
			cnx.close()
			cooling2 = 1
		
	else:
		if cooling2 == 1:
			GPIO.setup(cool2pin, GPIO.IN)
			time.sleep(.25)
			GPIO.setup(cool2pin, GPIO.IN)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Cooling2'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, controlname, '0', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '0', currdate,currtime,currall, controlname
			cursor.execute(query,args)
			cursor.close()
			cnx.close()
			cooling2 = 0
	return 1;

def cool3(hstate):
	global envname
	global cooling3 	
	if hstate == 1:
		if cooling3 == 0:
			GPIO.setup(cool3pin, GPIO.OUT)
			GPIO.output(cool3pin, GPIO.HIGH)
			time.sleep(.25)
			GPIO.setup(cool3pin, GPIO.OUT)
			GPIO.output(cool3pin, GPIO.HIGH)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Cooling3'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, controlname, '1', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '1', currdate,currtime,currall, controlname
			cursor.execute(query,args)
			cursor.close()
			cnx.close()
			cooling3 = 1
	else:
		if cooling3 == 1:		
			GPIO.setup(cool3pin, GPIO.IN)
			time.sleep(.25)
			GPIO.setup(cool3pin, GPIO.IN)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Cooling3'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, controlname, '0', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '0', currdate,currtime,currall, controlname
			cursor.execute(query,args)
			cursor.close()
			cnx.close()
			cooling3 = 0
	return 1;

def cool4(hstate):
	global envname
	global cooling4 	
	if hstate == 1:
		if cooling4 == 0:
			GPIO.setup(cool4pin, GPIO.OUT)
			GPIO.output(cool4pin, GPIO.HIGH)
			time.sleep(.25)
			GPIO.setup(cool4pin, GPIO.OUT)
			GPIO.output(cool4pin, GPIO.HIGH)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Cooling4'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, controlname, '1', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '1', currdate,currtime,currall, controlname
			cursor.execute(query,args)
			cursor.close()
			cnx.close()
			cooling4 = 1
	else:
		if cooling4 == 1:
			GPIO.setup(cool4pin, GPIO.IN)
			time.sleep(.25)
			GPIO.setup(cool4pin, GPIO.IN)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Cooling4'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, controlname, '0', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '0', currdate,currtime,currall, controlname
			cursor.execute(query,args)
			cursor.close()
			cnx.close()
			cooling4 = 0
	return 1;

def rh(hstate):
	global rhing 
	global envname	
	if hstate == 1:
		if rhing == 0:
			GPIO.setup(rhpin, GPIO.OUT)
			GPIO.output(rhpin, GPIO.HIGH)
			time.sleep(.25)
			GPIO.setup(rhpin, GPIO.OUT)
			GPIO.output(rhpin, GPIO.HIGH)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Dehumidify'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, controlname, '1', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '1', currdate,currtime,currall, controlname
			cursor.execute(query,args)
			cursor.close()
			cnx.close()
			rhing = 1
		
	else:
		if rhing == 1:
			GPIO.setup(rhpin, GPIO.IN)
			time.sleep(.25)
			GPIO.setup(rhpin, GPIO.IN)
			currdate = time.strftime("%Y/%m/%d")
			currtime = time.strftime("%H:%M:%S")
			currall =  time.strftime("%Y/%m/%d %H:%M:%S")
			serialnum = settingsarray[11]
			controlname = 'Dehumidify'
			cnx = mysql.connector.connect(**config)
                	cursor = cnx.cursor()
                	query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                	args = envname, serialnum, controlname, '0', currdate,currtime,currall
			cursor.execute(query,args)
			cursor.close()
			cursor = cnx.cursor()
			if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
			query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       		args = envname, serialnum, '0', currdate,currtime,currall, controlname
			cursor.execute(query,args)
			cursor.close()
			cnx.close()
			rhing = 0
		
	return 1;

def ipm(hstate):
	global envname	
	if hstate == 1:
		GPIO.setup(ipmpin, GPIO.OUT)
		GPIO.output(ipmpin, GPIO.HIGH)
		time.sleep(.25)
		GPIO.setup(ipmpin, GPIO.OUT)
		GPIO.output(ipmpin, GPIO.HIGH)
		currdate = time.strftime("%Y/%m/%d")
		currtime = time.strftime("%H:%M:%S")
		currall =  time.strftime("%Y/%m/%d %H:%M:%S")
		serialnum = settingsarray[11]
		controlname = 'IPM'
		cnx = mysql.connector.connect(**config)
                cursor = cnx.cursor()
                query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                args = envname, serialnum, controlname, '1', currdate,currtime,currall
		cursor.execute(query,args)
		cursor.close()
		cursor = cnx.cursor()
		if settingsarray[24] == '1':
			x= postcontrol(controlname,hstate)
		query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
     		args = envname, serialnum, '1', currdate,currtime,currall, controlname
		cursor.execute(query,args)
		cursor.close()
		cnx.close()
			
		
	else:
		GPIO.setup(ipmpin, GPIO.IN)
		time.sleep(.25)
		GPIO.setup(ipmpin, GPIO.IN)
		currdate = time.strftime("%Y/%m/%d")
		currtime = time.strftime("%H:%M:%S")
		currall =  time.strftime("%Y/%m/%d %H:%M:%S")
		serialnum = settingsarray[11]
		controlname = 'IPM'
		cnx = mysql.connector.connect(**config)
                cursor = cnx.cursor()
                query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                args = envname, serialnum, controlname, '0', currdate,currtime,currall
		cursor.execute(query,args)
		cursor.close()
		cursor = cnx.cursor()
		if settingsarray[24] == '1':
			x= postcontrol(controlname,hstate)
		query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       	args = envname, serialnum, '0', currdate,currtime,currall, controlname
		cursor.execute(query,args)
		cursor.close()
		cnx.close()
		
		
	return 1;

def alert(hstate):
	global envname	
	if hstate == 1:
		GPIO.setup(alertpin, GPIO.OUT)
		GPIO.output(alertpin, GPIO.HIGH)
		time.sleep(.25)
		GPIO.setup(alertpin, GPIO.OUT)
		GPIO.output(alertpin, GPIO.HIGH)
		currdate = time.strftime("%Y/%m/%d")
		currtime = time.strftime("%H:%M:%S")
		currall =  time.strftime("%Y/%m/%d %H:%M:%S")
		serialnum = settingsarray[11]
		controlname = 'Alarm'
		cnx = mysql.connector.connect(**config)
                cursor = cnx.cursor()
                query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                args = envname, serialnum, controlname, '1', currdate,currtime,currall
		cursor.execute(query,args)
		cursor.close()
		cursor = cnx.cursor()
		if settingsarray[24] == '1':
			x= postcontrol(controlname,hstate)
		query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
     		args = envname, serialnum, '1', currdate,currtime,currall, controlname
		cursor.execute(query,args)
		cursor.close()
		cnx.close()
			
		
	else:
		GPIO.setup(alertpin, GPIO.IN)
		time.sleep(.25)
		GPIO.setup(alertpin, GPIO.IN)
		currdate = time.strftime("%Y/%m/%d")
		currtime = time.strftime("%H:%M:%S")
		currall =  time.strftime("%Y/%m/%d %H:%M:%S")
		serialnum = settingsarray[11]
		controlname = 'Alarm'
		cnx = mysql.connector.connect(**config)
                cursor = cnx.cursor()
                query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                args = envname, serialnum, controlname, '0', currdate,currtime,currall
		cursor.execute(query,args)
		cursor.close()
		cursor = cnx.cursor()
		if settingsarray[24] == '1':
			x= postcontrol(controlname,hstate)
		query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       	args = envname, serialnum, '0', currdate,currtime,currall, controlname
		cursor.execute(query,args)
		cursor.close()
		cnx.close()
		
		
	return 1;




def zone(zname,zpin,hstate):
	#print ("zone")
	#print (zname)
	#print (zpin)
	#print (hstate) 
	global envname	
	if hstate == 1:
		GPIO.setup(zpin, GPIO.OUT)
		GPIO.output(zpin, GPIO.HIGH)
		time.sleep(.25)
		GPIO.setup(zpin, GPIO.OUT)
		GPIO.output(zpin, GPIO.HIGH)

		currdate = time.strftime("%Y/%m/%d")
		currtime = time.strftime("%H:%M:%S")
		currall =  time.strftime("%Y/%m/%d %H:%M:%S")
		serialnum = settingsarray[11]
		controlname = zname
		cnx = mysql.connector.connect(**config)
                cursor = cnx.cursor()
                query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                args = envname, serialnum, controlname, '1', currdate,currtime,currall
		cursor.execute(query,args)
		cursor.close()
		cursor = cnx.cursor()
		if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
		query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       	args = envname, serialnum, '1', currdate,currtime,currall, controlname
		cursor.execute(query,args)
		cursor.close()
		cnx.close()
			
		
	else:
		GPIO.setup(zpin, GPIO.IN)
		time.sleep(.25)
		GPIO.setup(zpin, GPIO.IN)
		currdate = time.strftime("%Y/%m/%d")
		currtime = time.strftime("%H:%M:%S")
		currall =  time.strftime("%Y/%m/%d %H:%M:%S")
		serialnum = settingsarray[11]
		controlname = zname
		cnx = mysql.connector.connect(**config)
                cursor = cnx.cursor()
                query = ("INSERT INTO controls (Greenhouse, Serialnum, Control, State, Date,Time,dateandtime) values (%s,%s,%s,%s,%s,%s,%s)")
                args = envname, serialnum, controlname, '0', currdate,currtime,currall
		cursor.execute(query,args)
		cursor.close()
		cursor = cnx.cursor()
		if settingsarray[24] == '1':
				x= postcontrol(controlname,hstate)
		query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s where Control=%s")
	       	args = envname, serialnum, '0', currdate,currtime,currall, controlname
		cursor.execute(query,args)
		cursor.close()
		cnx.close()
			
		
	return 1;




def readsensors():
 	
	while True:
		time.sleep(2)
		#get sensor data
	    	global temperature
		global humidity
		global light

		#w1="/sys/bus/w1/devices/28-0000053c9108/w1_slave"
		#raw = open(w1, "r").read()
		#t1 = ((float(raw.split("t=")[-1])/1000)*1.8)+32 
		#t2 = temperature - t1
		#if (abs(t2 - t1)>0.35):
		#	temperature = t1
  		
		#print temperature 
		#"+str(float(raw.split("t=")[-1])/1000)+"degrees"
		#temperature = 62.15 
		#humidity = 82.00
		#light =  tsltest3.LightSensor.calculateLux()
		#light =  LightSensor.calculateLux()

		#light = 40000
		
		#print (temperature)

def postdata():
	global temperature
	global humidity
	global envname
	global light
 	
	while True:
		time.sleep(900)
		cnx = mysql.connector.connect(**config)
               	cursor = cnx.cursor()
               	currdate = time.strftime("%Y/%m/%d")
		currtime = time.strftime("%H:%M:%S")
		serialnum = settingsarray[11]
		query = ("INSERT into conditions(Date,Time,Greenhouse,Temperature, Humidity, Light, Moles, Serialnum) values (%s,%s,%s,%s,%s,%s,%s,%s)")
                args = currdate, currtime, envname, temperature, humidity, light, moles, serialnum
		cursor.execute(query,args)
		cursor.close()
		cnx.close()


def postcontrol(name,state):
 	global envname
	global ConnectionError
	#print "postcontrol"
	currdate = time.strftime("%Y/%m/%d")
	currtime = time.strftime("%H:%M:%S")
	serialnum = settingsarray[11]
	time.sleep(2)
	post_data = {'Greenhouse':envname,'Serialnum':serialnum,'Control':name,'State':state}
 	#post_response = requests.post(url='http://www.agrowsoft.com/conditions/ceaproinsertcontrols.php',data=post_data)
 	#print post_response
	# This urlencodes your data (that's why we need to import urllib at the top)
	#data = urllib.urlencode(query_args)
	data = urllib.urlencode(post_data)

	# Send HTTP POST request
	headers = {"Host":"agrowsoft.com","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36","Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	url='http://www.agrowsoft.com/conditions/ceaproinsertcontrols.php'
	try:
		request = urllib2.Request(url, data, headers)
	except:
		pass
	try:
		response = urllib2.urlopen(request,timeout=1)
		html = response.read()
	except:
		pass
 
	

	# Print the result
	#print html	

		


def checkstate():
	global temperature
	global humidity
	global envname
	global light
	global dailyaccumlight
	while True:
		time.sleep(5)
		cnx = mysql.connector.connect(**config)
        	cursor = cnx.cursor()
        	currdate = time.strftime("%Y/%m/%d")
		currtime = time.strftime("%H:%M:%S")
		serialnum = settingsarray[11]
		query = ("UPDATE conditionstemp SET Date=%s, Time=%s, Greenhouse=%s,Temperature=%s, Humidity=%s, Light=%s, Moles=%s, Serialnum=%s")
        	args = currdate, currtime, envname, temperature, humidity, light, moles, serialnum
		cursor.execute(query,args)
		cursor.close()

		#dailyaccumlight
		cursor = cnx.cursor()
		query = ("UPDATE settings SET var=%s where ID=%s")
        	args = dailyaccumlight, '50'
		cursor.execute(query,args)
		cursor.close()
		
		#running?
		query = ("SELECT var from settings where ID=12")
		cursor = cnx.cursor()
        	cursor.execute(query)
        	data = cursor.fetchall()
		global run
		for row in data:
			if run == '1':
				if row[0] == '0':
					x = stopall()
			if run == '0':
				if row[0] == '1':
					setup();
			run = row[0] 
			#print (row[0])
			#print (run)
		cursor.close()

		cursor = cnx.cursor()
		query = ("SELECT var from settings where ID=77")
        	cursor.execute(query)
        	data = cursor.fetchall()
			
		for row in data:
			temptemp = float(row[0])
			if abs(temptemp - temperature) > .5:
				temperature = temptemp
			#print(temperature)
		cursor.close()
		cursor = cnx.cursor()
		query = ("SELECT var from settings where ID=78")
        	cursor.execute(query)
        	data = cursor.fetchall()
		
			
		for row in data:
			temphumidity = float(row[0])
			if abs(temphumidity - humidity) > .75:
				humidity = temphumidity
			#print(humidity)
		cursor.close()
		
		cursor = cnx.cursor()
		query = ("SELECT var from settings where ID=150")
        	cursor.execute(query)
        	data = cursor.fetchall()
			
		for row in data:
			light = float(row[0])
			
			#print(light)
		cursor.close()


		#check for settings update
		cursor = cnx.cursor()
		query = ("SELECT var from settings where ID=85")
        	cursor.execute(query)
        	data = cursor.fetchall()
		for row in data:
			if row[0] == '1':
				#refresh settings
				setup();
				query = ("Update settings set var = 0 where ID=85")
        			cursor.execute(query)
		cursor.close()

		
		#check for irrigate now
		cursor = cnx.cursor()
		global irrigating
		query = ("SELECT var from settings where ID=79")
        	cursor.execute(query)
        	data = cursor.fetchall()
		for row in data:
			if row[0] == '1':
				if irrigating == 0:
					irrigating = 1
					query = ("Update settings set var = 0 where ID=79")
        				cursor.execute(query)
		cursor.close()

		#check for update systemtime
		cursor = cnx.cursor()
		
		query = ("SELECT var from settings where ID=53")
        	cursor.execute(query)
        	data = cursor.fetchall()
		for row in data:
			if row[0] == '1':
				query = ("SELECT var from settings where ID=54")
        			cursor.execute(query)
        			data = cursor.fetchall()
				for row in data:
					newdate = row[0]
				query = ("SELECT var from settings where ID=55")
        			cursor.execute(query)
        			data = cursor.fetchall()
				for row in data:
					newtime = row[0]

				
				try:
					newosdate = 'date +%Y%m%d -s "' + newdate + '"'
					#print(newosdate)
					os.system(newosdate)

				except:
					print("could not update date")

				try:
					newostime = 'date +%T -s "' + newtime +'"'
					#print(newostime)
					os.system(newostime)

				except:
					print("could not update time")
				
				query = ("Update settings set var = 0 where ID=53")
        			cursor.execute(query)
		cursor.close()
		
		

		#check for upgrade
		cursor = cnx.cursor()
		query = ("SELECT var from settings where ID=48")
        	cursor.execute(query)
        	data = cursor.fetchall()
		for row in data:
			if row[0] == '1':
				print("time for upgrade")
				try:
					shutil.copy2('/var/www/conditions/backup.sql', 'backup.sql')
					print("file copied")
				except:
					print("could not copy")

				try:
					shutil.copy2('/var/www/conditions/poststats.py', 'poststats.py')
					print("file copied")
				except:
					print("could not copy")

				#try:
					#shutil.copy2('/var/www/conditions/sensorread.py', 'sensorread.py')
					#print("file copied")
				#except:
					#print("could not copy")

				try:
					shutil.copy2('/var/www/conditions/app.py', 'app.py')
					print("file copied")
				except:
					print("could not copy")
				
				query = ("Update settings set var = 0 where ID=48")
        			cursor.execute(query)
		cursor.close()

		#check for power down
		cursor = cnx.cursor()
		query = ("SELECT var from settings where ID=56")
        	cursor.execute(query)
        	data = cursor.fetchall()
		for row in data:
			if row[0] == '1':
				print("time to power down")
			
				query = ("Update settings set var = 0 where ID=56")
        			cursor.execute(query)
				os.system('shutdown now')
			
		cursor.close()

		#check for database restore
		cursor = cnx.cursor()
		query = ("SELECT var from settings where ID=49")
        	cursor.execute(query)
        	data = cursor.fetchall()
		cursor.close()
		cnx.close()
		for row in data:
			if row[0] == '1':
				#source database
				print("db1")
				
				os.system('mysql -u root  agrowsoftdb -e \ "source backup.sql;"')
				time.sleep(2)
				cnx = mysql.connector.connect(**config)
				cursor = cnx.cursor()
        			print("db2")
				#update serialnumber
				query = ("UPDATE settings SET var=%s where ID=%s")
        			args = settingsarray[11], '11'
				cursor.execute(query,args)
				query = ("UPDATE controllers SET Serialnum=%s where customerID=%s")
        			args = settingsarray[11], '1'
				cursor.execute(query,args)
				query = ("UPDATE settings SET var='0' where ID='49'")
				cursor.execute(query)
				print("db3")
				cursor.close()
				cnx.close()
				
				
 
def stopall():
	global IPMing
	global heating1
	global heating2
	global cooling1
	global cooling2
	global cooling3
	global cooling4
	global rhing
	global irrigating
	global alerting

	GPIO.setup(heat1pin, GPIO.IN)
	GPIO.setup(heat2pin, GPIO.IN)
	GPIO.setup(cool1pin, GPIO.IN)
	GPIO.setup(cool2pin, GPIO.IN)
	GPIO.setup(cool3pin, GPIO.IN)
	GPIO.setup(cool4pin, GPIO.IN)
	GPIO.setup(rhpin, GPIO.IN)
	GPIO.setup(ipmpin, GPIO.IN)
	GPIO.setup(w1pin, GPIO.IN)
	GPIO.setup(w2pin, GPIO.IN)
	GPIO.setup(w3pin, GPIO.IN)
	GPIO.setup(w4pin, GPIO.IN)
	GPIO.setup(w5pin, GPIO.IN)
	GPIO.setup(w6pin, GPIO.IN)
	GPIO.setup(alertpin, GPIO.IN)
	currdate = time.strftime("%Y/%m/%d")
	currtime = time.strftime("%H:%M:%S")
	currall =  time.strftime("%Y/%m/%d %H:%M:%S")
	serialnum = settingsarray[11]
	cnx = mysql.connector.connect(**config)
       	cursor = cnx.cursor()
	query = ("UPDATE controlstemp SET Greenhouse=%s, Serialnum=%s, State=%s, Date=%s,Time=%s,dateandtime=%s")
	args = envname, serialnum, '0', currdate,currtime,currall
	cursor.execute(query,args)
	cursor.close()
	cursor = cnx.cursor()
	query = ("UPDATE settings set var='0' where ID='80'")
	cursor.execute(query)
	cursor.close()
	cnx.close()									
		
	IPMing = 0
	heating1 = 0
	heating2 = 0
	cooling1 = 0
	cooling2 = 0
	cooling3 = 0
	cooling4 = 0
	rhing = 0
	irrigating = 0
	alerting = 0								

def irrigate():
	global irrigating
	global moles
	global menulevel
	global thezone
	while True:
		time.sleep(1)
		#print (irrigating)
		if irrigating == 1:
			cnx = mysql.connector.connect(**config)
       			cursor = cnx.cursor()
			query = ("UPDATE settings SET var=1 where ID=80")
			cursor.execute(query)
			cursor.close()
			cnx.close()
			#watering
			
			print ("watering6")
			#16 on
			thezone = '6'
			x = zone('Zone6',w6pin,1)
			time.sleep(15)

			print ("watering6")
			thezone = '1'
			x = zone('Zone1',w1pin,1)
			ontime = float(settingsarray[13])
			time.sleep(ontime)
			x = zone('Zone1',w1pin,0)	
			time.sleep(5)
		
			print ("watering2")
			x = zone('Zone2',w2pin,1)
			thezone = '2'
			ontime = float(settingsarray[14])
			time.sleep(ontime)
			x = zone('Zone2',w2pin,0)	
			time.sleep(5)
		
			x = zone('Zone3',w3pin,1)
			thezone = '3'
			ontime = float(settingsarray[15])
			time.sleep(ontime)
			x = zone('Zone3',w3pin,0)	
			time.sleep(5)	
		
			x = zone('Zone4',w4pin,1)
			thezone = '4'
			ontime = float(settingsarray[16])
			time.sleep(ontime)
			x = zone('Zone4',w4pin,0)	
			time.sleep(5)	
		
			x = zone('Zone5',w5pin,1)
			thezone = '5'
			ontime = float(settingsarray[17])
			time.sleep(ontime)
			x = zone('Zone5',w5pin,0)
			time.sleep(5)

			x = zone('Zone6',w6pin,0)

			
			irrigating = 0
			cnx = mysql.connector.connect(**config)
       			cursor = cnx.cursor()
			query = ("UPDATE settings SET var=0 where ID=80")
			cursor.execute(query)
			cursor.close()
			cnx.close()
			thezone = 'Complete'
			moles = 0
			menulevel = 1	
			time.sleep(5)	



def ipmthread():
	global IPMing
	
	while True:
		time.sleep(1)
		if IPMing == 1:
			x = ipm(1)
			ontime = int(settingsarray[75])*60
			time.sleep(ontime)		
			x = ipm(0)
			IPMing = 0
		
def main():
	#print("Main")26
	#start database
	time.sleep(10)
	os.system('/etc/init.d/mysql start')
	#os.system('/usr/bin/mysqld_safe')
	#for lcd pad #for pins 17,18#busnum=2 
	#os.system('echo BB-I2C1 > /sys/devices/bone_capemgr.8/slots')
	#set time
	#os.system('ntpdate pool.ntp.org')
	#os.system('echo BB-W1:00A0 > /sys/devices/bone_capemgr.8/slots')	
	
	
	startup();
	setup();
	#stopall();
	
	# Create read sensor thread as follows
	#try:
   	#	thread.start_new_thread( readsensors, () )
	#except:
   	#	print "Error: unable to start sensor thread"

	# Create thread as follows
	try:
   		thread.start_new_thread( theloop, () )
	except:
   		print "Error: unable to start theloop thread"
	
	# Create thread as follows
	try:
   		thread.start_new_thread( checkstate, () )
	except:
   		print "Error: unable to start checkstate thread"
	# Create thread as follows
	try:
   		thread.start_new_thread( postdata, () )
	except:
   		print "Error: unable to start postdata thread"

	try:
   		thread.start_new_thread( irrigate, () )
	except:
   		print "Error: unable to start checkstate thread"
	
	try:
   		thread.start_new_thread( ipmthread, () )
	except:
   		print "Error: unable to start checkstate thread"
	
	while True:
		x = 0		

if __name__ == "__main__":
    main()
