#include <Arduino.h>
#include <ArduinoJson.h>
#include <WiFiMulti.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiUdp.h>
#include <string.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>


//#define DHTPIN 2     // Digital pin connected to the DHT sensor 
// Feather HUZZAH ESP8266 note: use pins 3, 4, 5, 12, 13 or 14 --
// Pin 15 can work but DHT must be disconnected during program upload.

//#define sensorPin A0
//#define LEDRed  3

// Uncomment the type of sensor in use:
#define DHTTYPE    DHT11     // DHT 11


// See guide for details on sensor wiring and usage:
//   https://learn.adafruit.com/dht/overview



//╔═════════════════╗
// 網 路 相 關 參 數
//╚═════════════════╝
const char globleWiFiSSID[] = "e521"; //威秀wifi
const char globleWiFiPassword[] = "e521E521e521"; //12346789
String globleServerPath = "http://e3b1-163-13-133-72.ngrok.io/"; //偉中後端伺服器URL
float globleTemperature = 0;
float globleHumidity = 0;              
int globleMHsensor = 0;              
int globleLDR = 0; 
bool globleWaterMotor = false;
long long lastWaterMotortime = 0;       
//╔═══════════╗
// 腳 位 宣 告
//╚═══════════╝

const int8_t  Waterpin = 26;          
const int8_t  sensorPin = 34;  
const int8_t  DHTPIN = 14;        
const int8_t  lightPin = 35;    

//╔════════════════════╗
// 工 作 執 行 緒 宣 告
//╚════════════════════╝
TaskHandle_t taskAskRequest, taskStatusLED, taskRealCoinAndTicketing, taskRealTime, taskTestThread;

//╔══════════════════════════════════════════════╗
// 旗 標 宣 告 
// 寫: simulationCoinPulse, simulationTicketPulse
// 讀: realCoin, 
//╚══════════════════════════════════════════════╝
enum statusFlag { //狀態燈
      execution = 1, connectedInternet, connectedServer
}statusFlag;
enum busyFlag { //
      rushHour = 1800, unRushHour = 5000
}busyFlag;

//╔═════════════════╗
// 工 作 列 隊 宣 告
//╚═════════════════╝

DHT_Unified dht(DHTPIN, DHTTYPE);
uint32_t delayMS;

//[函  式] 負責校準時間
unsigned long long timeCalibration( void ){
  struct tm timeinfo;
  const long gmtOffsetSec = 8* 3600;
  const long dayLightOffsetSec = 0;
  const char* ntpServer = "pool.ntp.org";

  while (WiFi.status() == WL_CONNECTED) {
    Serial.println("[timeCalibration] 開始時間校準");
    configTime(gmtOffsetSec, dayLightOffsetSec, ntpServer);
    if( !getLocalTime(&timeinfo) ){
      Serial.println("[timeCalibration] 校準失敗3秒後重新開始");
      delay(3000);
    }else{
      Serial.println("[timeCalibration] 校準成功");
      return 0;
    }
  }
  Serial.println("[timeCalibration] 無網路無法校準");
  return 0;
}

//[函  式] 取得現在時間
int64_t getTimestamp() {
	struct timeval tv;
	gettimeofday(&tv, NULL);
	return (tv.tv_sec * 1000LL + (tv.tv_usec / 1000LL));
}

//[函  式] 負責連上網路
void wifiConnect( void ){

  //WiFi.mode(WIFI_STA);
  Serial.print("[wifiConnect] 嘗試連線 SSID:");
  Serial.print(globleWiFiSSID);
  Serial.print(" Password:");
  Serial.println(globleWiFiPassword);
  //WiFiMulti wifiMulti;
  //wifiMulti.h方法
  //wifiMulti.addAP("威秀wifi", "12346789");
  //wifiMulti.addAP("zhenyu的iphone", "12346789"); 
  //while (wifiMulti.run() != WL_CONNECTED) {
    //statusFlag = execution;
  //}

  //WiFi.h方法
  WiFi.begin(globleWiFiSSID, globleWiFiPassword);
  
  Serial.print("[wifiConnect] 等待");
  while (WiFi.status() != WL_CONNECTED) {
    statusFlag = execution;
    Serial.print(".");
    vTaskDelay(500 / portTICK_RATE_MS );
  }
  
  // WiFi.h方法
  statusFlag = connectedInternet;
  Serial.println("\n[wifiConnect] Wi-Fi連線成功");
  Serial.print("[wifiConnect] SSID：");
  Serial.println(WiFi.SSID());
  Serial.print("[wifiConnect] IP位址：");
  Serial.println(WiFi.localIP());
  Serial.print("[wifiConnect] WiFi RSSI: ");
  Serial.println(WiFi.RSSI());
}

//[函  式] webhook回報後台
int webhook(){
  String httpRequestData;

  if( WiFi.status() == WL_CONNECTED ){
    
    // WiFiClientSecure client;
    HTTPClient http;

    // 建構post內容
    httpRequestData = "{\n  \"Temperature\": ";
    httpRequestData += String(globleTemperature);
    httpRequestData += ",\n  \"Humidity\": ";
    httpRequestData += String(globleHumidity);
    httpRequestData += ",\n  \"Dust\": ";
    httpRequestData += String(globleMHsensor);
    httpRequestData += ",\n  \"LightDR\": ";
    httpRequestData += bool(globleLDR);
    httpRequestData += ",\n  \"WaterMotor\": ";
    httpRequestData += String(globleWaterMotor);
    httpRequestData += ",\n  \"timestamp\": ";
    httpRequestData += String(getTimestamp());
    httpRequestData += "\n}";
    Serial.println("[webhook] working...\n");
    Serial.println(httpRequestData);

    Serial.print("url: ");Serial.println(globleServerPath.c_str());
    http.begin(globleServerPath.c_str());   
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(httpRequestData);
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    String payload = http.getString();
    Serial.println(payload);
    http.end();

    return 0;
  }
  return 1;
}

void setup() {

  Serial.begin(115200);          
  pinMode(Waterpin, OUTPUT);    
  pinMode(sensorPin,INPUT);
  pinMode(lightPin,INPUT);
  //水馬達初始化
  digitalWrite(Waterpin, HIGH); 
  // Initialize device.
  dht.begin();
  Serial.println(F("DHTxx Unified Sensor Example"));
  // Print temperature sensor details.
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  Serial.println(F("------------------------------------"));
  Serial.println(F("Temperature Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("°C"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("°C"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("°C"));
  Serial.println(F("------------------------------------"));
  
  // Print humidity sensor details.
  dht.humidity().getSensor(&sensor);
  Serial.println(F("Humidity Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("%"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("%"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("%"));
  Serial.println(F("------------------------------------"));

  // Set delay between sensor readings based on sensor details.
  delayMS = sensor.min_delay / 1000 * 60 * 1;
 
  //呼叫連線
  wifiConnect( );

  //時間校準(調用pool.ntp.org)
  timeCalibration( );

  //開啟「test」執行續在核心1
  //xTaskCreate( testThread, "testThread", 8192, NULL, 0, &taskTestThread);
  //xTaskCreatePinnedToCore( realCoinAndTicketing, "realCoinAndTicketing", 8192, NULL, 2, &taskRealCoin, 1);

  //webhook("coinPulse" ,10);
}

void loop() { 
  // Get temperature event and print its value.
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  Serial.println(F("-------------------------"));
  if (isnan(event.temperature)) {
    globleTemperature = 0;
    Serial.println(F("Error reading temperature!"));
  }
  else {
    globleTemperature = event.temperature;
    Serial.print(F("Temperature: "));
    Serial.print(event.temperature);
    Serial.println(F("°C"));
  }

  // Get humidity event and print its value.
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    globleHumidity = 0;
    Serial.println(F("Error reading humidity!"));
  }
  else {
    globleHumidity = event.relative_humidity;
    Serial.print(F("Humidity: "));
    Serial.print(event.relative_humidity);
    Serial.println(F("%"));
  }
  Serial.println(F("-------------------------\n"));

  // MHsensor
  globleMHsensor = analogRead(sensorPin);
  Serial.printf("現在檢測土壤溼度為: %d\n",globleMHsensor);
  Serial.println(F("-------------------------\n"));

  // LDR (light-dependent resistor)
  globleLDR = analogRead(lightPin);
  Serial.printf("現在檢測光線強度為: %d\n",globleLDR);
  Serial.println(F("-------------------------\n"));
  digitalWrite(Waterpin, HIGH); 
 
  //WaterMotor(12hours open 5 seconds)
  globleWaterMotor = false; 
  long long Nowtime =  getTimestamp();
 
  if(Nowtime - lastWaterMotortime > 45000000){
      digitalWrite(Waterpin, LOW); 
      delay(5000);
      digitalWrite(Waterpin, HIGH);
      globleWaterMotor = true;  
      Serial.printf("現在檢測水馬達啟動: %d\n",globleWaterMotor);
      Serial.println(F("-------------------------\n"));
      lastWaterMotortime = Nowtime;   }
  else {
      //Serial.printf("距離上次水馬達啟動: %d\n",(Nowtime - lastWaterMotortime));
      digitalWrite(Waterpin, HIGH);  }
 
  // Webhook 
  webhook();

  // Delay between measurements.
  delay(delayMS);
}
