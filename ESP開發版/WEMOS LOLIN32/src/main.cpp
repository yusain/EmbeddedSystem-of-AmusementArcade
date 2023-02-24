#include <Arduino.h>
#include <ArduinoJson.h>

#include <esp_task_wdt.h>

#include <WiFiMulti.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiUdp.h>

#include <string.h>

#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#include <U8g2lib.h>
#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif


/*
  U8g2lib Example Overview:
    Frame Buffer Examples: clearBuffer/sendBuffer. Fast, but may not work with all Arduino boards because of RAM consumption
    Page Buffer Examples: firstPage/nextPage. Less RAM usage, should work with all Arduino boards.
    U8x8 Text Only Example: No RAM usage, direct communication with display controller. No graphics, 8x8 Text only.    
  This is a page buffer example.    
*/

// Please UNCOMMENT one of the contructor lines below
// U8g2 Contructor List (Picture Loop Page Buffer)
// The complete list is available here: https://github.com/olikraus/u8g2/wiki/u8g2setupcpp
// Please update the pin numbers according to your setup. Use U8X8_PIN_NONE if the reset pin is not connected

U8G2_SSD1306_128X64_NONAME_1_SW_I2C u8g2(U8G2_R0,
                                /*SCL clock=*/ 4, 
                                /*SDL data= */ 5, 
                                /* reset=*/ U8X8_PIN_NONE);   
                                // All Boards without Reset of the Display



// See guide for details on sensor wiring and usage:
// https://learn.adafruit.com/dht/overview
// Uncomment the type of sensor in use:
#define DHTTYPE    DHT11     // DHT 11


// ╔═════════════════╗
//  網 路 相 關 參 數
// ╚═════════════════╝
const char globleWiFiSSID[] = "iPhone"; //WiFiSSID
const char globleWiFiPassword[] = "511511511"; //WiFiPassword
String globleServerPath = "http://eea6-163-13-133-72.ngrok.io"; //偉中後端伺服器URL

// ╔═════════════════╗
//  GPIO 相 關 參 數
// ╚═════════════════╝
float globleTemperature = 0;
float globleHumidity = 0;              
int globleMHsensor = 0;              
int globleLDR = 0; 
bool globleWaterMotor = false;
long long lastWaterMotortime = 0;
long long WaterMotortime = 12*60*60*1000;

int loopdelay = 1 * 60 * 1000;

// ╔═════════════════╗
//  GPIO 腳 位 宣 告
// ╚═════════════════╝

#define  LightDRPin 39      // Analog pin for LightDR
#define  DHTPIN   16        // Digital pin connected to the DHT sensor          
#define  MHsensorPin  36    // Analog pin for MHsensor
#define  WaterMotorpin 25   // Digital pin for WaterMotor

// ╔════════════════════╗
//  工 作 執 行 緒 宣 告
// ╚════════════════════╝
TaskHandle_t tasku8g2_Dispaly, taskuGPIOSensor, taskWatchDog;

// ╔════════════════════╗
//  旗 標 與 結 構 宣 告 
// ╚════════════════════╝
enum statusFlag { //系統狀態旗標
      execution = 1, connectedInternet, TimeCalibration, 
      Webhook , Webhookfalse, WebhookSuccess,
      ReTry
}statusFlag;

struct IconStatus { //Icon狀態存取
  int WifiIcon, DustIcon, LDRIcon;
}IconStatus;


// ╔═════════════════╗
//  工 作 列 隊 宣 告
// ╚═════════════════╝
DHT_Unified dht(DHTPIN, DHTTYPE);
uint32_t delaySensorMS;

// [函  式] 取得現在時間
int64_t getTimestamp() {
	struct timeval tv;
	gettimeofday(&tv, NULL);
	return (tv.tv_sec * 1000LL + (tv.tv_usec / 1000LL));
}

// [函  式] 負責校準時間
unsigned long long timeCalibration( void ){
  struct tm timeinfo;
  const long gmtOffsetSec = 8* 3600;
  const long dayLightOffsetSec = 0;
  const char* ntpServer = "pool.ntp.org";

  while (WiFi.status() == WL_CONNECTED) {
    statusFlag = TimeCalibration;
    Serial.println("[timeCalibration] 開始時間校準");
    configTime(gmtOffsetSec, dayLightOffsetSec, ntpServer);
    if( !getLocalTime(&timeinfo) ){
      Serial.println("[timeCalibration] 校準失敗3秒後重新開始");
      delay(3000);
    }else{
      lastWaterMotortime = getTimestamp();
      Serial.println("[timeCalibration] 校準成功");
      return 0;
    }
  }
  Serial.println("[timeCalibration] 無網路無法校準");
  return 0;
}

// [函  式] 負責連上網路
void wifiConnect( void ){

  //WiFi.mode(WIFI_STA);
  Serial.print("[wifiConnect] 嘗試連線 SSID:");
  Serial.print(globleWiFiSSID);
  Serial.print(" Password:");
  Serial.println(globleWiFiPassword);
  /*
  //WiFiMulti wifiMulti;
  //wifiMulti.h方法
  //wifiMulti.addAP("yusain的iphone", "511511511"); 
  //while (wifiMulti.run() != WL_CONNECTED) {
    //statusFlag = execution;
  //}
  */
  //WiFi.h方法
  WiFi.begin(globleWiFiSSID, globleWiFiPassword);
  
  Serial.print("[wifiConnect] 等待");
  while (WiFi.status() != WL_CONNECTED) {
    statusFlag = connectedInternet;
    Serial.print(".");
    vTaskDelay(500 / portTICK_RATE_MS );
  }
  
  // WiFi.h方法
  Serial.println("\n[wifiConnect] Wi-Fi連線成功");
  Serial.print("[wifiConnect] SSID：");
  Serial.println(WiFi.SSID());
  Serial.print("[wifiConnect] IP位址：");
  Serial.println(WiFi.localIP());
  Serial.print("[wifiConnect] WiFi RSSI: ");
  Serial.println(WiFi.RSSI());
}

// ╔═════════════════╗
//  U8g2 函 示 宣 告
// ╚═════════════════╝

#define TopH    10
#define MainH   34
#define BottomH 20
#define MainW   85
#define BottomW 58
#define spaceH  3

// 
#define IconSum       0x45
#define IconSumCloudy 0x41
#define IconCloudy    0x40

#define IconSmiley    0x24
#define Iconcalm      0x31
#define Iconunhappy   0x61

#define IconNoWiFi    0xe217
#define IconWiFi      0xe21a

// [函  式] 劃出 Oled 主要線架構
void u8g2_LineFrame(void){
  u8g2.drawHLine(0      ,(TopH+1)    ,u8g2.getDisplayWidth());          
  u8g2.drawHLine(0      ,(TopH+MainH),u8g2.getDisplayWidth());
  u8g2.drawVLine(MainW  ,(TopH+1)    ,MainH-1);
  u8g2.drawVLine(BottomW,(TopH+MainH),BottomH);
  u8g2.drawLine( BottomW/2-1, u8g2.getDisplayHeight()-BottomH
                ,BottomW/2+1, u8g2.getDisplayHeight());
}

// [函  式] 依據 WiFi 與Time 更新顯示
void u8g2_WiFiTime(int Period){  

  if (WiFi.status() != WL_CONNECTED) {    
    
    // WiFiIcon
    IconStatus.WifiIcon = IconNoWiFi;
    u8g2.setFont(u8g2_font_siji_t_6x10);
    u8g2.drawGlyph(u8g2.getDisplayWidth()-15, (TopH-spaceH), IconStatus.WifiIcon);


    String wifistate = "WiFiConnect";
    for(int i=0; i < (Period % 4); i++) wifistate+=".";

    // wifiConnectshow    
    u8g2.setFont(u8g2_font_5x8_tf);
    u8g2.setFontPosCenter();
    u8g2.drawStr(5,u8g2.getDisplayHeight()-(BottomH+MainH/2)+spaceH, wifistate.c_str());

  }else{
    
    // WiFiIcon
    IconStatus.WifiIcon = IconWiFi;
    u8g2.setFont(u8g2_font_siji_t_6x10);
    u8g2.drawGlyph(u8g2.getDisplayWidth()-15, (TopH-spaceH), IconStatus.WifiIcon);
    
    // get now time to Time
    char Time[100];
    time_t now = time (0);
    strftime (Time, 100, "%H:%M", localtime (&now));

    //TimeButtonShow
    u8g2.setFont(u8g2_font_courB18_tn);
    u8g2.setFontPosCenter();
    u8g2.drawStr(5,u8g2.getDisplayHeight()-(BottomH+MainH/2)+spaceH,Time);

  }
}

// [函  式] 依據 GPIO 輸出數值
void u8g2_GPIO(int count) {
      
  // HTsensor
  String strHumidity = "H:"; strHumidity += String(int(globleHumidity)); strHumidity += "%"; // H: value%
  u8g2.setFont(u8g2_font_6x10_tf);
  u8g2.setCursor(MainW+5,(TopH+MainH/2)-spaceH*2);
  u8g2.print(strHumidity.c_str());

  String strTemperature = "T:"; strTemperature += String(int(globleTemperature)); strTemperature += "\260C"; // T: value°C
  u8g2.setCursor(MainW+5,(TopH+MainH)-spaceH*2);
  u8g2.print(strTemperature.c_str());


  // Dust icon
  u8g2.setFont(u8g2_font_unifont_t_emoticons);

  switch (int(globleMHsensor)/(4096/3)) // max4096
  { case 0: IconStatus.DustIcon = IconSmiley; break;
    case 1: IconStatus.DustIcon = Iconcalm; break;
    case 2: IconStatus.DustIcon = Iconunhappy; break;  
    default:IconStatus.DustIcon = Iconunhappy; break; }

  u8g2.drawGlyph(10, u8g2.getDisplayHeight()-spaceH, IconStatus.DustIcon);


  
  // LDR  
  u8g2.setFont(u8g2_font_open_iconic_weather_2x_t);
  switch (int(globleLDR)/(400/3)) //LDR range:0 ~ 100up
  { case 0: IconStatus.LDRIcon = IconCloudy; break;
    case 1: IconStatus.LDRIcon = IconSumCloudy; break;
    case 2: IconStatus.LDRIcon = IconSum; break;  
    default:IconStatus.LDRIcon = IconSum; break; }
  u8g2.drawGlyph(BottomW/2+5, u8g2.getDisplayHeight()-spaceH*3, IconStatus.LDRIcon);



  // WM icon
  u8g2.setFont(u8g2_font_unifont_t_75);
  u8g2.drawGlyph(u8g2.getDisplayWidth()-15, u8g2.getDisplayHeight()-BottomH+spaceH*2, 0x25f0 + count);

  // WM Status message
  u8g2.setFont(u8g2_font_5x7_tf);
  long long Watertime = (getTimestamp() -lastWaterMotortime);

  if(Watertime > WaterMotortime){

    u8g2.drawStr(BottomW+5, u8g2.getDisplayHeight()-BottomH+spaceH*2, "WM:Start");  
    String strWoring = "Working" ;
    for(int i=0; i < (count % 4); i++) strWoring+=".";
    u8g2.drawStr(BottomW+5, u8g2.getDisplayHeight()-BottomH/2+spaceH*2, strWoring.c_str());}
  
  else{
  
    u8g2.drawStr(BottomW+5, u8g2.getDisplayHeight()-BottomH+spaceH*2, "WM:Stop");  
    String strWatertime = String( int( (WaterMotortime - Watertime)/(60*60*1000) ) ) + "hr"
                        + String( int( (WaterMotortime - Watertime)%(60*60*1000)/(60*1000) ) ) + "m"
                        + String( int( (WaterMotortime - Watertime)%(60*1000)/(1000) ) ) + "s";
    u8g2.drawStr(BottomW+5, u8g2.getDisplayHeight()-BottomH/2+spaceH*2, strWatertime.c_str()); }

}

// [函  式] 依據 StatusFla 輸出執行狀況
void u8g2_StatusFlag(void){

  String SystemStatus = "";
  switch (statusFlag)
  { case execution:         SystemStatus = "SystemWorking"; break;
    case connectedInternet: SystemStatus = "WiFi: " + String(globleWiFiSSID); break;
    case TimeCalibration:   SystemStatus = "TimeCalibration"; break;
    case Webhook:           SystemStatus = "Webhook..."; break;
    case WebhookSuccess:    SystemStatus = "Webhook Success"; break;
    case Webhookfalse:      SystemStatus = "Webhook false"; break;
    case ReTry:             SystemStatus = "ReTry"; break;
    default:                SystemStatus = ""; break; }

  u8g2.setFont(u8g2_font_6x10_tf);
  u8g2.setCursor(5,(TopH-spaceH));
  u8g2.print(SystemStatus.c_str());
}

// [任 務/ 執 行 續] U8G2 各項顯示
void u8g2_Dispaly(void * parameter){

  int count;
  while(true){

    u8g2.firstPage();
    do {
      
      u8g2_LineFrame();

      u8g2_StatusFlag();
      
      // wifi and Time
      u8g2_WiFiTime(count);
      
      // u8g2 sensor show
      u8g2_GPIO(count);

    } while ( u8g2.nextPage() );
    
    // count
    count<3 ? count++ : count=0;
  }
}

// ╔═══════════════════════╗
//  GPIOSensor 函 示 宣 告
// ╚═══════════════════════╝

// [函  式] DHT11 Sensor
void DHT11sensor(void){
   // Get temperature event and print its value.
    sensors_event_t event;
    dht.temperature().getEvent(&event);
    Serial.println("-------------------------");
    if (isnan(event.temperature)) {
      globleTemperature = 0;
      Serial.println("Error reading temperature!");
    }
    else {
      globleTemperature = event.temperature;
      Serial.print("Temperature: ");
      Serial.print(event.temperature);
      Serial.println("°C");
    }

    // Get humidity event and print its value.
    dht.humidity().getEvent(&event);
    if (isnan(event.relative_humidity)) {
      globleHumidity = 0;
      Serial.println("Error reading humidity!");
    }
    else {
      globleHumidity = event.relative_humidity;
      Serial.print("Humidity: ");
      Serial.print(event.relative_humidity);
      Serial.println("%");
    }
    Serial.println("-------------------------\n");
}

// [函  式] Dust Sensor
void Dust(void){
  // Dust(MHsensor)
  globleMHsensor = analogRead(MHsensorPin);
  Serial.printf("現在檢測土壤溼度為: %d\n",globleMHsensor);
  Serial.println("-------------------------\n");
}

// [函  式] LDR Sensor
void LDR(void){
  // LDR (light-dependent resistor)
  globleLDR = analogRead(LightDRPin);
  Serial.printf("現在檢測光線強度為: %d\n",globleLDR);
  Serial.println("-------------------------\n");
}

// [函  式] WaterMotor Sensor
void WaterMotor(void){
  //WaterMotor(12hours open 5 seconds)
  digitalWrite(WaterMotorpin, HIGH);    
  globleWaterMotor = false;

  long long Nowtime =  getTimestamp();
  if(Nowtime - lastWaterMotortime > WaterMotortime){
      digitalWrite(WaterMotorpin, LOW); 
      delay(5000);
      digitalWrite(WaterMotorpin, HIGH);
      globleWaterMotor = true;  
      Serial.printf("現在檢測水馬達啟動: %d\n",globleWaterMotor);
      Serial.println("-------------------------\n");
      lastWaterMotortime = Nowtime;   }
  else {
      //Serial.printf("距離上次水馬達啟動: %d\n",(Nowtime - lastWaterMotortime));
      digitalWrite(WaterMotorpin, HIGH);  }
}

// [任 務/ 執 行 續] GPIOSensor偵測各個感測器
void GPIOSensor(void * parameter){
  while(true){
   
    //The GPIOSensor Function
    DHT11sensor();
    Dust();
    LDR();
    WaterMotor();

    //delay between measurements
    delay(delaySensorMS); //5*1000);

  } 
}

// [函  式] webhook回報後台
int webhook(){

  String httpRequestData;
  
  if( WiFi.status() == WL_CONNECTED ){

    statusFlag = Webhook;

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
    httpRequestData += String(globleLDR);
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

    httpResponseCode  == 200 ? statusFlag = WebhookSuccess : statusFlag = Webhookfalse; 
    delay(500 / portTICK_RATE_MS);
    statusFlag == WebhookSuccess ? statusFlag =  execution : statusFlag = ReTry;
    http.end();
    return 0;
  }
  return 1;
}


// [任 務/ 執 行 續] WatchDog偵測webhook狀態
//#define WDT_TIMEOUT 3
void WatchDog(void * parameter){  
  while(true){
    //esp_task_wdt_reset();
    if (statusFlag == ReTry){
        webhook();
    }    
    delay(1500 / portTICK_RATE_MS );
  }
}

// Main_Program_Setup
void setup() {

  Serial.begin(115200);

  // Initialize PINSet         
  pinMode(WaterMotorpin, OUTPUT);    
  pinMode(MHsensorPin,INPUT);
  pinMode(LightDRPin,INPUT);  
 
  digitalWrite(MHsensorPin, HIGH);  //水馬達初始化
  
  // Initialize device and Set delay between sensor readings
  u8g2.begin();

  dht.begin();
  sensor_t sensor;
  delaySensorMS = sensor.min_delay / 1000;
  
  // 開啟 task 執行續
  xTaskCreate( u8g2_Dispaly, "u8g2_Dispaly", 2048, NULL, 0, &tasku8g2_Dispaly);  
  xTaskCreate( GPIOSensor, "GPIOSensor", 8192, NULL, 1, &taskuGPIOSensor);
  xTaskCreate( WatchDog, "WatchDog", 2048, NULL, 2, &taskWatchDog);

  //esp_task_wdt_init(WDT_TIMEOUT, true); //enable panic so ESP32 restarts
  //esp_task_wdt_add(&taskWatchDog); //add current thread to WDT watch

  // 呼叫連線
  wifiConnect( );  

  // 時間校準(調用pool.ntp.org)
  timeCalibration( );
}

//Main_Program_loop 
void loop() {
 
  // Webhook 
  webhook();

  // Delay 1 minutes
  delay(loopdelay / portTICK_RATE_MS);
}