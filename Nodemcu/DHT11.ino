#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
#include <DHT.h> // dht11 temperature and humidity sensor library

// Set these to run example.
#define FIREBASE_HOST "smart-iot-android.firebaseio.com"
#define FIREBASE_AUTH "DOcCeOVR43KF8PscdC9RC30GuodKenRCwJZBX49g"
//Change line with your WiFi router name and password
// DEFINE HERE THE KNOWN NETWORKS
const char *KNOWN_SSID[] = {"KTA1-Leerlingen", "telenet-CF8FF7A-2.5ghz"};
const char *KNOWN_PASSWORD[] = {"LeerlingVanKTA1!", "pljka280"};

const int KNOWN_SSID_COUNT = sizeof(KNOWN_SSID) / sizeof(KNOWN_SSID[0]); // number of known networks

#define DHTPIN D4

// what digital pin we're connected to
#define DHTTYPE DHT11 // select dht type as DHT 11 or DHT22
DHT dht(DHTPIN, DHTTYPE);
void setup()
{
    Serial.begin(9600);

    boolean wifiFound = false;
    int i, n;

    // ----------------------------------------------------------------
    // Set WiFi to station mode and disconnect from an AP if it was previously connected
    // ----------------------------------------------------------------
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    delay(100);
    Serial.println("Setup done");

    // ----------------------------------------------------------------
    // WiFi.scanNetworks will return the number of networks found
    // ----------------------------------------------------------------
    Serial.println(F("scan start"));
    int nbVisibleNetworks = WiFi.scanNetworks();
    Serial.println(F("scan done"));
    if (nbVisibleNetworks == 0)
    {
        Serial.println(F("no networks found. Reset to try again"));
        while (true)
            ; // no need to go further, hang in there, will auto launch the Soft WDT reset
    }

    // ----------------------------------------------------------------
    // if you arrive here at least some networks are visible
    // ----------------------------------------------------------------
    Serial.print(nbVisibleNetworks);
    Serial.println(" network(s) found");

    // ----------------------------------------------------------------
    // check if we recognize one by comparing the visible networks
    // one by one with our list of known networks
    // ----------------------------------------------------------------
    for (i = 0; i < nbVisibleNetworks; ++i)
    {
        Serial.println(WiFi.SSID(i)); // Print current SSID
        for (n = 0; n < KNOWN_SSID_COUNT; n++)
        { // walk through the list of known SSID and check for a match
            if (strcmp(KNOWN_SSID[n], WiFi.SSID(i).c_str()))
            {
                Serial.print(F("\tNot matching "));
                Serial.println(KNOWN_SSID[n]);
            }
            else
            { // we got a match
                wifiFound = true;
                break; // n is the network index we found
            }
        } // end for each known wifi SSID
        if (wifiFound)
            break; // break from the "for each visible network" loop
    }              // end for each visible network

    if (!wifiFound)
    {
        Serial.println(F("no Known network identified. Reset to try again"));
        while (true)
            ; // no need to go further, hang in there, will auto launch the Soft WDT reset
    }

    // ----------------------------------------------------------------
    // if you arrive here you found 1 known SSID
    // ----------------------------------------------------------------
    Serial.print(F("\nConnecting to "));
    Serial.println(KNOWN_SSID[n]);

    // ----------------------------------------------------------------
    // We try to connect to the WiFi network we found
    // ----------------------------------------------------------------
    WiFi.begin(KNOWN_SSID[n], KNOWN_PASSWORD[n]);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");

    // ----------------------------------------------------------------
    // SUCCESS, you are connected to the known WiFi network
    // ----------------------------------------------------------------
    Serial.println(F("WiFi connected, your IP address is "));
    Serial.println(WiFi.localIP());
    //print local IP address
    Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH); // connect to firebase
    dht.begin();

    Firebase.setInt("Distance", 0);

    //Start reading dht sensor
}
int n = 0;

void loop()
{
    /*
 * For TEMp sensor 
 */

    float h = dht.readHumidity();    // Reading temperature or humidity takes about 250 milliseconds!
    float t = dht.readTemperature(); // Read temperature as Celsius (the default)

    if (isnan(h) || isnan(t))
    { // Check if any reads failed and exit early (to try again).
        Serial.println(F("Failed to read from DHT sensor!"));
        return;
    }

    Serial.print("Humidity: ");
    Serial.print(h);
    String fireHumid = String(h) + String("%"); //convert integer humidity to string humidity
    Serial.print("%  Temperature: ");
    Serial.print(t);
    Serial.println("Â°C ");
    String fireTemp = String(t) + String(" °C"); //convert integer temperature to string temperature
    delay(20);

    Firebase.setString("Humidity", fireHumid);   //setup path and send readings
    Firebase.setString("Temperature", fireTemp); //setup path and send readings
}