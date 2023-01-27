# Postilaatikko projekti

Tämän projektin ideana oli tehdä Smart postilaatikko, joka lähettää python skriptin avulla tiedon aina kun posti saapuu. 
Postilaatikossa on magneetti sensorit, joiden avulla laati-kon sisällä oleva raspberrypi lähettää tiedon aina kun luukku aukaistaan. 
Tieto postin saapumisesta lähetetään Google cloudin google sheets ohjelmaan ja kännykkään IFTTT sovellusalustan avulla. 
Lisäksi RaspberryPi:n kamera ottaa kuvan joka kerta kun laatikko avataan. Kuva lähetetään dropbox pilvitallennus palveluun. 
Projektissa käytettiin myös ESP32:sta ja GrovePi:n LCD -näyttöä ja LED:iä. LCD -näyttö ja LED syttyvät ja ilmoittavat käyttäjälle aina kun posti saapuu.

# Tässä on lista käytetyistä laitteista ja teknologioista projektissa:
• Raspberry Pi 3
o Kamera
o 2 magneetti sensoria
• ESP32
o Grove RGB LCD -näyttö
o Grove LED kit
• Google Cloud
o Google Sheets
• MQTT (Mosquitto & Paho)
• Python
• DropBox
• MySQL
• IFTTT
