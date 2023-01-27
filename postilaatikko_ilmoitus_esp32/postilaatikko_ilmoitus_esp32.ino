#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include "rgb_lcd.h"

#define LED   4 /* Pinnin määritys ledille */

/* LCD näytön taustaväri kun se saa viestin että posti on saapunut */
const int colorR = 255;
const int colorG = 0;
const int colorB = 0;

/* LCD näytön taustaväri kun postilaatikko suljetaan */
const int colorT = 255;
const int colorS = 255;
const int colorV = 255;

/*  wifi router ja MQTT asetukset */
const char* ssid = "Router SSID";
const char* password = "Router Password";
const char* mqttServer = "mqtt server ip-address";
const int mqttPort = your mqtt port;
const char* mqttUser = "your mqtt username";
const char* mqttPassword = "yout mqtt password";


WiFiClient espClient;
PubSubClient client(espClient);
rgb_lcd lcd;


 
void callback(char* topic, byte* payload, int length)
{
Serial.print("Message arrived in topic: ");
Serial.println(topic);
Serial.print("Message:");
for (int i = 0; i < length; i++)
{
Serial.print((char)payload[i]);
}
Serial.println();
Serial.println("-----------------------");

/* Jos MQTT lähettää viestiä testi/mqtt LCD näyttöön tulee teksti "Posti on tullut". Myös LED syttyy.  */
if (String(topic) == "testi/mqtt") {
    Serial.print("Changing output to ");
    // set up the LCD's number of columns and rows:
    lcd.begin(16, 2);
    
    lcd.setRGB(colorR, colorG, colorB);
    
    // Print a message to the LCD.
    lcd.print("Posti on tullut!");

    delay(1000);

    digitalWrite(LED, HIGH);
    
    
    
}

/* Jos MQTT lähettää viestin testi/mqtt2 LCD näyttö näyttää tyhjää ja tausta väri muuttuu  */
/* MQTT viesti voi olla mitä haluaa mutta itse käytin testi/mqtt ja testi2/mqtt2 */
if (String(topic) == "testi2/mqtt2") {
    
    Serial.print("Changing output to ");
    // set up the LCD's number of columns and rows:
    lcd.begin(16, 2);
    
    lcd.setRGB(colorT, colorS, colorV);
    
    // Print a message to the LCD.
    lcd.print("");

    delay(1000);
    
    digitalWrite(LED, LOW);
  }
}
 
void setup()
{
  /* Wifi yhdistys asetukset */
Serial.begin(115200);
WiFi.begin(ssid, password); 
 
while (WiFi.status() != WL_CONNECTED)
{
delay(500);
Serial.println("Connecting to WiFi..");
}
Serial.println("Connected to the WiFi network");
/* MQTT server yhdistys */ 
client.setServer(mqttServer, mqttPort);
client.setCallback(callback);
 
while (!client.connected()) {
Serial.println("Connecting to MQTT...");
 
if (client.connect("ESP32Client", mqttUser, mqttPassword ))
{
Serial.println("connected");
}
else
{
Serial.print("failed with state "); /* Virhe viesti */
Serial.print(client.state());
delay(500);
}
}
/* yhdistää testi/mqtt ja testi2/mqtt2 clientteihin voidakseen lukea että kumpaa viestiä mqtt serveri lähettää */
client.subscribe("testi/mqtt");
client.subscribe("testi2/mqtt2");
pinMode(LED, OUTPUT);

 
}


  



void loop()
{
    
  
  
  client.loop();
}
