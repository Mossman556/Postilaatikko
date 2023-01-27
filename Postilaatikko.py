#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import datetime
import pygsheets
from picamera import PiCamera
from time import sleep
from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import random
import sys
import pymysql
import dropbox

# Yhteyden luominen msql tietokantaan
connection = pymysql.connect(host="localhost", user="jussi", passwd="kettujus1", database="postilaatikko1")
cursor = connection.cursor()

#lisää päivän ja kellon ajan kun laatikko avataan ja suljetaan.
avattu = "INSERT INTO AJAT(PÄIVÄYS, AVATTU) VALUES(curdate(), curtime());"
suljettu = "INSERT INTO AJAT(PÄIVÄYS, SULJETTU) VALUES(curdate(), curtime());"



#MQTT yhteys tiedot
broker ='localhost' # MQTT osoite
port = 1883 # MQTT portti
topic = "testi/mqtt" # MQTT viestin aihe
topic2 = "testi2/mqtt2" # Toinen MQTT viestin aihe
client_id = f'python-mqtt-{random.randint(0, 1000)}' # luo client_id:n random numeron välillä 0 - 1000
username = 'jussi' # MQTT käyttäjä nimi
password = 'kettujus1' # MQTT salasana

dbx = dropbox.Dropbox('sl.BRwH3JwecQpJiU4ehVpUd3od-76WPdro3CNR7FyPyeXVRs-JopO2EYAIDKjUbgwJMyLCPswyZJKPqYGpvUUesQAqwoUnnBHsp1_PCpGFfhrKT3Z6q5REUEJ-nwBzQJKsNbcoWRY') # dropbox token key
dbx.users_get_current_account() # hakee nykyisen dropbox tilin tiedot

#Funktio jolla luodaan MQTT yhteys sekä ilmoitetaan siitä.
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client






# Viestin publish toiminto
def publish(client):
    msg_count = 0 
    if True:
        time.sleep(1)
        result = client.publish(topic) # MQTT viesti topic
        # jos status 0 printtaa postiluukku auki muutoin failed.
        status = result[0]
        if status == 0:
            print(f"Postiluuku auki")
            
            
           
            
            
            
        else:
            client.disconnect(client)
            print(f"Failed to send message to topic {topic}")
            client.loop_stop()

# toisen viestin publish toiminto
def publish2(client):
    msg_count = 0 
    if True:
        time.sleep(1)
        result = client.publish(topic2) # MQTT viesti topic 2
        # jos status = 0 niin printaa postiluukku auki muuten failed
        status = result[0]
        if status == 0:
            print(f"Postiluuku kiinni")
            
            
           
            
            
            
        else:
            client.disconnect(client)
            print(f"Failed to send message to topic {topic}")
            client.loop_stop()
            

            
        

# Asettaa Broadcom moden jotta GPIO pinnit voidaan asettaa numeroiksi.
GPIO.setmode(GPIO.BCM)

# Asettaa vars funktiot eli onko auki ja oliko aikasemmin auki
isOpen = None
previouslyOpen = None

# Asettaa ovi sensori pinnin.
DOOR_SENSOR_PIN = 18
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# googlesheets asetukset jotta ohjelma pystyy tallentamaan tiedot google cloudin pygsheetsiin.
gs = pygsheets.authorize(service_file='/home/jussi/Desktop/service_file.json')
sh = gs.open('Letterbox Activations')
wks = sh.sheet1

firstRun = 1

#Asetukset postilaatikon sensorin avaukselle ja sulkemiselle sekä pygsheet rivien lisäykset, dropbox kuvan siirto ja mysql tietokannan tiedon lisäys.
while True:
    previouslyOpen = isOpen
    isOpen = GPIO.input(DOOR_SENSOR_PIN) #GPIO pin tieto
    if (isOpen and (isOpen != previouslyOpen)): # jos on auki niin lähettää tiedon pygsheettiin ja tekee rivi lisäykset.
        now = datetime.datetime.now() 
        thedate = time.strftime("%d.%m.%Y") # päivämäärä asetus pygsheettiin.
        thetime = now.strftime("%H:%M:%S")  # aika asetus pygshettiin.
        print ("Postilaatikko on avattu! %s at %s" % (thedate, thetime))
        wks.insert_rows(1) # asettaa aina uuden rivin kun luukku avataan
        
        

        dateField = 'A%d' % wks.cols # päivämäärä asetus pygsheet riviin
        timeField = 'B%d' % wks.cols # aika asetus pygsheet riviin

        wks.cell(dateField).value = thedate # päivämäärän laittaminen pygsheet päivä lokeroon
        wks.cell(timeField).value = thetime # ajan laittaminen pygsheet avattu / suljettu lokeroon
        
        # Tekee MYSQL avattu funktion.
        cursor.execute(avattu)
        connection.commit()
        
        
        #Kamera ottaa kuvan kun postilaatikko avataan.
        camera = PiCamera()
        camera.brightness = 55
        camera.resolution = (1024, 768)
        camera.start_preview()
        camera.capture('/home/jussi/Desktop/posti.jpg')
        camera.close()
        
        #Lähettää kameran ottaman kuvan dropbox palveluun
        f = open('posti.jpg', 'rb')
        dbx.files_upload(bytes(f.read()), "/Apps/Postilaatikko/Posti.jpg %s at %s" % (thedate, thetime))
        
        
        
        
        
        # Run funkito mqtt viestiä publish varten joka suoritetaan.
        def run():
            
            client = connect_mqtt()
            client.loop_start()
            publish(client)
            client.loop_stop()
            
            
            
            
            


        if __name__ == '__main__':
                run()
        
    # Postilaatikon sulkemisen toiminnot    
    elif (isOpen != previouslyOpen):
        now = datetime.datetime.now()
        thedate = now.strftime("%d/%m/%Y") # Asettaa päivämäärän pygsheetsia varten.
        thetime = now.strftime("%H:%M:%S") # Asettaa ajan pygsheetsia varten.
        
        
        
        
        
        print ("Postilaatikko on suljettu. (%s at %s)" % (thedate, thetime))
        
        #MYSQL funktio
        cursor.execute(suljettu)
        connection.commit()
        
        # Run funktio publish2 MQTT viestille
        def run2():
            
            client = connect_mqtt()
            client.loop_start()
            publish2(client)
            client.loop_stop()
            
            
            
            


        if __name__ == '__main__':
                run2()
        
        
        
        
       
        
        
        
        
        
            


        
    # jos firstRun on 0 tämä ilmoittaa pygsheetille ajan jolloin se on suljettu.
    if(firstRun == 1):
            timeClosedField = 'C%d' % wks.cols
            wks.cell(timeClosedField).value = thetime
            
            
            
            
    else:
        firstRun = 0

        

    time.sleep(0.1)
