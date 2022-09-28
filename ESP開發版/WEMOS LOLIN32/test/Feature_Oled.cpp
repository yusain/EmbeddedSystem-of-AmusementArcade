#include <Arduino.h>
#include <ArduinoJson.h>
#include <WiFiMulti.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiUdp.h>
#include <string.h>

//╔═════════════════╗
// 網 路 相 關 參 數
//╚═════════════════╝
const char globleWiFiSSID[] = "e521"; //威秀wifi
const char globleWiFiPassword[] = "e521E521e521"; //12346789
String globleServerPath = "http://163.13.133.185:3001"; //中間伺服器URL
String globleCompanyAbbreviation = "dj"; //公司簡寫
int globleId = 113001;              //本裝置編號
int8_t globleCoinId = 11;           //投幣模組
int8_t globleTicketingId = 21;      //出票模組
int8_t globleCrushTicketingId = 31; //裁票模組
int8_t globlePowerId = 41;          //電源模組

//╔═══════════╗
// 腳 位 宣 告
//╚═══════════╝
const int8_t  onboardLed1 = 2;          //控制板子上的狀態燈
const int8_t  coinModelCounter = 4;     //投幣機計數脈衝
const int8_t  ticketModelCounter = 17;  //出票機計數脈衝
const int8_t  ticketModelMotor = 16;    //出票機馬達
const int8_t  crushModel1 = 5;          //裁票機預留
const int8_t  crushModel2 = 18;         //裁票機預留
const int8_t  crushModel3 = 19;         //裁票機預留
const int8_t  powerControl = 21;        //電源控制
const int8_t  testInput1 = 13;           //測試輸入1(上拉)
const int8_t  testInput2 = 12;           //測試輸入2(上拉)

//╔════════════════════╗
// 工 作 執 行 緒 宣 告
//╚════════════════════╝
TaskHandle_t taskAskRequest, taskStatusLED, taskRealCoinAndTicketing, taskRealTime, taskTestThread;

//╔══════════════════════════════════════════════╗
// 旗 標 宣 告 
// 寫: simulationCoinPulse, simulationTicketPulse
// 讀: realCoin, 
//╚══════════════════════════════════════════════╝
bool globleSimulationTimeForCoin = false;   //為真時模擬模擬輸出
bool globleSimulationTimeForTicket = false; //為真時模擬模擬輸出
enum statusFlag { //狀態燈
      execution = 1, connectedInternet, connectedServer
}statusFlag;
enum busyFlag { //
      rushHour = 1800, unRushHour = 5000
}busyFlag;
enum oledFlag {
        wifi, dth11, hwSoil, waterpump, sunlightR
}oledFlag;

//╔═════════════════╗
// 工 作 列 隊 宣 告
//╚═════════════════╝
QueueHandle_t coinQueue, ticketQueue;
int8_t queueSize = 16;

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
  WiFiMulti wifiMulti;
  WiFi.mode(WIFI_STA);
  Serial.print("[wifiConnect] 嘗試連線 SSID:");
  Serial.print(globleWiFiSSID);
  Serial.print(" Password:");
  Serial.println(globleWiFiPassword);
  //wifiMulti.h方法
  //wifiMulti.addAP("威秀wifi", "12346789");
  //wifiMulti.addAP("zhenyu的iphone", "12346789"); 
  //while (wifiMulti.run() != WL_CONNECTED) {
    //statusFlag = execution;
  //}

  //WiFi.h方法
  WiFi.begin(globleWiFiSSID, globleWiFiPassword);
  
  //WiFi.begin("zhenyu的iphone", "12346789");
  Serial.print("[wifiConnect] 等待");
  while (WiFi.status() != WL_CONNECTED) {
    statusFlag = execution;
    Serial.print(".");
    vTaskDelay(500 / portTICK_RATE_MS );
  }
  
  //WiFi.h方法
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
int webhook( String event, int count){
  String httpRequestData;
  Serial.print("[webhook] event:");
  Serial.print(event);
  Serial.print(" count:");
  Serial.println(count);

  if( WiFi.status() == WL_CONNECTED ){
    WiFiClient client;
    HTTPClient http;
    int8_t modelId = 0;
    int8_t inputPortId = 0;

    //根據event分配modelId和inputPortId
    if(event == "coinPulse"){
      modelId = globleCoinId;  
      inputPortId = 3;
    }else if(event == "lotteryPulse"){
      modelId = globleTicketingId;
      inputPortId = 1;
    }else{
      modelId = 0;
    }

    //建構post內容
    httpRequestData = "{\"events\": [{\"type\":\"";
    httpRequestData += event;                       //事件
    httpRequestData += "\",\"timestamp\": ";
    httpRequestData += String(getTimestamp());      //時間
    httpRequestData += ",\"source\": {\"vendorHwid\": \"";
    httpRequestData += globleCompanyAbbreviation;   //身分(公司)
    httpRequestData += String(globleId);            //身分(裝置)
    httpRequestData += String(modelId);             //身分(模組)
    httpRequestData += "\", \"count\":";
    httpRequestData += String(count);               //執行次數
    httpRequestData += ", \"inputPortId\":";        
    httpRequestData += String(inputPortId);         //執行port(沒有為甚麼)
    httpRequestData += ",\"offline\": false}}]}";
    Serial.println("[webhook] Success");
    //Serial.println(httpRequestData);

    http.begin(client, globleServerPath + "/webhook");
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    int httpResponseCode = http.POST(httpRequestData);
    return 0;
  }
  return 1;
}

//[函  式] 模擬投幣訊號(給MB)
int simulationCoinPulse(int count) {
  Serial.print("[simulationCoinPulse] 模擬投幣訊號(給MB) count=");
  Serial.println(count);
  int8_t pulseTime = 50;

  //暫時重新設定腳位
  globleSimulationTimeForCoin = true;
  pinMode(coinModelCounter, OUTPUT);

  //loop
  for( int i = 0 ; i < count ; i++ ){
    digitalWrite(coinModelCounter, HIGH);
    delay(150);
    digitalWrite(coinModelCounter, LOW);
    delay(pulseTime);
  }

  //腳位復位
  globleSimulationTimeForCoin = false;
  pinMode(coinModelCounter, INPUT_PULLUP);
  return 0;
}

//[函  式] 模擬出票訊號(給model)
int simulationTicketPulse(int count) {
  Serial.print("[simulationTicketPulse] 模擬出票訊號(給model) count=");
  Serial.println(count);
  
  //設定
  bool inIsLow = false;     //false in腳(馬達)為高電平出發
  bool outIsClose = false;  //false out腳(記數)為高常開
  
  //宣告(出票觸發)
  bool lastStatusTicketingCount = false;    
  bool preStatusTicketingCount = false;     
  bool prepreStatusTicketingCount = false;  

  //暫時重新設定腳位
  globleSimulationTimeForTicket = true; //改變旗標
  pinMode(ticketModelMotor, OUTPUT);

  //起動出票機馬達
  int64_t startTime = getTimestamp();           //計時開始
  int64_t stopTime = startTime + (count * 100);  //計時結束
  digitalWrite(ticketModelMotor, HIGH);
  do{
    //出票觸發(更新狀態)(計數出票觸發)
    prepreStatusTicketingCount = preStatusTicketingCount;
    preStatusTicketingCount = lastStatusTicketingCount;
    lastStatusTicketingCount = digitalRead(ticketModelCounter);
    
    if( prepreStatusTicketingCount == true && preStatusTicketingCount == true && lastStatusTicketingCount == false){ //負緣觸發
      count--;
    }

    vTaskDelay(5 / portTICK_RATE_MS ); //delay 5ms

  } while (count > 0 && getTimestamp() < stopTime); //當count沒或是超時停止
  digitalWrite(ticketModelMotor, LOW);


  //腳位復位
  globleSimulationTimeForTicket = false; //改變旗標
  //pinMode(ticketModelCounter, INPUT_PULLUP);
  pinMode(ticketModelMotor, INPUT_PULLUP);
  return 0;
}

//[執行緒] 板子上的LED狀態改變
void statusLED( void * parameter ){
  //初始化腳位
  pinMode(onboardLed1, OUTPUT);
  
  short highTime = 1000;
  short lowTime = 0;
  while (true) {
    if(statusFlag == execution){
      highTime = 30;
      lowTime = 200;
    }else if(statusFlag == connectedInternet){
      highTime = 200;
      lowTime = 200;
    }else if(statusFlag == connectedServer){
      highTime = 1000;
      lowTime = 0;
    }else{
      highTime = 0;
      lowTime = 1000;
    }
    digitalWrite(onboardLed1, HIGH);
    vTaskDelay(highTime / portTICK_RATE_MS );
    digitalWrite(onboardLed1, LOW);
    vTaskDelay(lowTime / portTICK_RATE_MS );
  }
}

//[執行緒] 詢問有無投幣/出票請求(有的話PUSH)heartbeat
void askRequest( void * parameter ) {
    HTTPClient http;
    DynamicJsonDocument doc(1024);  //解析JSON序列化(忽略)

    //宣告
    String serverPath;
    String httpRequestData = "{}";
    String payload; //放get拿到的資訊
    int httpResponseCode = 0;
    coinQueue = xQueueCreate( 16, sizeof( int ) ); //設定投幣工作列隊
    if(coinQueue == NULL){
      Serial.println("[setup] Error creating the queue");
    }
    ticketQueue = xQueueCreate( 16, sizeof( int ) ); //設定出票工作列隊
    if(ticketQueue == NULL){
      Serial.println("[setup] Error creating the queue");
    }

    Serial.println("[askRequest] 開始反覆詢問有無投幣/出票請求");
    
    //建構get路徑
    serverPath = globleServerPath + "/askRequests";
    serverPath += "?_id=";
    serverPath += globleCompanyAbbreviation;   //身分(公司)
    serverPath += String(globleId);            //身分(裝置)
    
    while (true) {
      if(WiFi.status()== WL_CONNECTED){
        http.begin(serverPath.c_str());
        http.setTimeout(1500);
        int httpResponseCode = http.GET();
        if (httpResponseCode > 0) {
          payload = http.getString();
          payload = String(payload);
          //Serial.print("[askRequest] askRequest success!");
          //Serial.println(serverPath.c_str());
          statusFlag = connectedServer;

          //解析成JSON
          deserializeJson(doc, payload);
          if(doc["command"] != "doNothing"){
            Serial.print(payload);
          }
          String command = doc["command"]; //命令要幹嘛
          int count = doc["count"]; //做幾次
          
          //提取命令
          if(command == "coinPulse"){
            //將結果push
            if ( !xQueueIsQueueFullFromISR(coinQueue) ){ //Queue沒滿(可push)
              xQueueSend(coinQueue, &count, portMAX_DELAY);
              Serial.print(" coinQueue size=");
              Serial.println(uxQueueMessagesWaiting(coinQueue));
            }
          }else if(command == "lotteryPulse"){
            //將結果push
            if ( !xQueueIsQueueFullFromISR(ticketQueue) ){ //Queue沒滿(可push)
              xQueueSend(ticketQueue, &count, portMAX_DELAY);
              Serial.print(" ticketQueue size=");
              Serial.println(uxQueueMessagesWaiting(ticketQueue));
            }
          }

        } else {
          //Serial.print("[askRequest] askRequest Error code: ");
          //Serial.println(httpResponseCode);
          statusFlag = connectedInternet;
        }

        // Free resources
        http.end();
        busyFlag = rushHour;
        vTaskDelay(busyFlag / portTICK_RATE_MS ); //1.8秒確認一次
      
      }else {
        Serial.println("[askRequest] WiFi Disconnected");
      } 
    }
}

//[執行緒] 監聽有無真實投幣/出票/Queue(有的話直接回報後台)
void realCoinAndTicketing( void * parameter ){
  
  //宣告
  String event = "doNothing";   //做什麼事
  int16_t count = 0;            //計數
  int16_t element = 0;          //Queue使用
  bool replyServer = false;     //是否回覆伺服器

  //宣告(投幣觸發)
  bool lastStatusCoin = false;    //最新狀態
  bool preStatusCoin = false;     //第二新狀態
  bool prepreStatusCoin = false;  //第三狀態

  //宣告(出票馬達)
  bool lastStatusTicketingMotor = false;    //
  bool preStatusTicketingMotor = false;     //
  bool prepreStatusTicketingMotor = false;  //

  //宣告(出票觸發)
  bool lastStatusTicketingCount = false;    //
  bool preStatusTicketingCount = false;     //
  bool prepreStatusTicketingCount = false;  //

  //初始化腳位
  //pinMode(coinModelCounter, INPUT_PULLUP); //開了會影響到simulationCoinPulse
  Serial.println("[realCoin] 開始監聽有無真實投幣/出票/Queue");
  
  //監聽
  while (true){

    //投幣觸發(更新狀態)
    prepreStatusCoin = preStatusCoin;
    preStatusCoin = lastStatusCoin;
    lastStatusCoin = digitalRead(coinModelCounter);

    //出票馬達(更新狀態)
    prepreStatusTicketingMotor = preStatusTicketingMotor;
    preStatusTicketingMotor = lastStatusTicketingMotor;
    lastStatusTicketingMotor = digitalRead(ticketModelMotor);

    //出票觸發(更新狀態)
    prepreStatusTicketingCount = preStatusTicketingCount;
    preStatusTicketingCount = lastStatusTicketingCount;
    lastStatusTicketingCount = digitalRead(ticketModelCounter);


    //有投幣?
    if( prepreStatusCoin == true && preStatusCoin == false && lastStatusCoin == false){ //負緣觸發
      if(!globleSimulationTimeForCoin){ //非模擬時間(沒加的話會計到模擬訊號觸發)
        
        //catch coin signal
        Serial.println("[realCoin] 有真實投幣觸發!");
        event = "coinPulse";
        count = 1;
        replyServer = true;
      }
    }

    //有出票?
    while( lastStatusTicketingMotor == true){ //馬達啟動
      
      //出票馬達(更新狀態)
      prepreStatusTicketingMotor = preStatusTicketingMotor;
      preStatusTicketingMotor = lastStatusTicketingMotor;
      lastStatusTicketingMotor = digitalRead(ticketModelMotor);

      if( prepreStatusTicketingCount == true && preStatusTicketingCount == false && lastStatusTicketingCount == false){ //負緣觸發
        if(!globleSimulationTimeForTicket){ //非模擬時間(沒加的話會計到模擬訊號觸發)
          Serial.println("[realCoin] 有真實出票觸發!");
          event = "lotteryPulse";
          count++;
          replyServer = true;
        }
      }
    }

    //coinQueue是否為空?
    if(!xQueueIsQueueEmptyFromISR(coinQueue)){ //Queue不為空(可pop)
      xQueueReceive(coinQueue, &element, portMAX_DELAY);
      simulationCoinPulse(element);
      event = "coinPulse";
      count = element;
      replyServer = true;
    }

    //ticketQueue是否為空?
    if(!xQueueIsQueueEmptyFromISR(ticketQueue)){ //Queue不為空(可pop)
      xQueueReceive(ticketQueue, &element, portMAX_DELAY);
      simulationTicketPulse(element);
      event = "lotteryPulse";
      count = element;
      replyServer = true;
    }

    //是否回覆伺服器
    if(replyServer){
      webhook(event ,count);
      //重置
      String event = "doNothing";  
      int16_t count = 0;     
      int16_t element = 0;          
      replyServer = false;  
    }

    //延遲
    vTaskDelay(5 / portTICK_RATE_MS );
  }
}

//[執行緒] 測試
void testThread( void * parameter ){
  while(true) {
    if(digitalRead(testInput1) == false){
      simulationCoinPulse(5);
    }
    if(digitalRead(testInput2) == false){
      simulationTicketPulse(5);
    }
    vTaskDelay( 2000 / portTICK_RATE_MS ); 
  }
}

void setup() {
  //初始化
  Serial.begin(9600); //設定uart胞率
  Serial.println("[setup] 初始化系統");
  statusFlag = execution; //設定程式狀態
  
  //初始化queue
  coinQueue = xQueueCreate( queueSize, sizeof( int ) );
  if(coinQueue == NULL){
    Serial.println("Error creating the queue");
  }
  ticketQueue = xQueueCreate( queueSize, sizeof( int ) );
  if(ticketQueue == NULL){
    Serial.println("Error creating the queue");
  }

  //初始化腳位(執行緒可能會更改)
  Serial.println("[setup] 初始化腳位");
  pinMode(onboardLed1, OUTPUT); 
  pinMode(coinModelCounter, INPUT_PULLUP);    //投幣機觸發
  pinMode(ticketModelCounter, INPUT_PULLUP);  //裁票機馬達
  pinMode(ticketModelMotor, INPUT_PULLUP);    //裁票機計數器
  pinMode(crushModel1, OUTPUT);
  pinMode(crushModel2, OUTPUT);
  pinMode(crushModel3, OUTPUT);
  pinMode(powerControl, OUTPUT);
  pinMode(testInput1, INPUT_PULLUP);  //測試開關1
  pinMode(testInput2, INPUT_PULLUP);  //測試開關2

  //開啟「狀態燈」執行續在核心0
  xTaskCreate( statusLED, "statusLED", 1024, NULL, 2, &taskStatusLED);
  //xTaskCreatePinnedToCore( statusLED, "statusLED", 1024, NULL, 0, &taskStatusLED, 0);
  
  //呼叫連線
  wifiConnect( );

  //時間校準(調用pool.ntp.org)
  timeCalibration( );

  //開啟「askRequest」執行續在核心0
  xTaskCreate( askRequest, "askRequest", 8192, NULL, 3, &taskAskRequest);
  //xTaskCreatePinnedToCore( heartbeat, "heartbeat", 4096, NULL, 3, &taskHeartbeat, 0);

  //開啟「realCoin」執行續在核心1
  xTaskCreate( realCoinAndTicketing, "realCoinAndTicketing", 8192, NULL, 0, &taskRealCoinAndTicketing);
  //xTaskCreatePinnedToCore( realCoinAndTicketing, "realCoinAndTicketing", 8192, NULL, 2, &taskRealCoin, 1);

  //開啟「test」執行續在核心1
  //xTaskCreate( testThread, "testThread", 8192, NULL, 0, &taskTestThread);
  //xTaskCreatePinnedToCore( realCoinAndTicketing, "realCoinAndTicketing", 8192, NULL, 2, &taskRealCoin, 1);

  //webhook("coinPulse" ,10);
}

void loop() {
  if(digitalRead(testInput1) == false){
    simulationCoinPulse(5);
  }
  if(digitalRead(testInput2) == false){
    simulationTicketPulse(5);
  }
}
#include <Arduino.h>
#include <string.h>
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
    
*/

// Please UNCOMMENT one of the contructor lines below
// U8g2 Contructor List (Frame Buffer)
// The complete list is available here: https://github.com/olikraus/u8g2/wiki/u8g2setupcpp
// Please update the pin numbers according to your setup. Use U8X8_PIN_NONE if the reset pin is not connected
U8G2_SSD1306_128X64_NONAME_F_SW_I2C u8g2(U8G2_R0, /* clock=*/ 4, /* data=*/ 5, /* reset=*/ U8X8_PIN_NONE);   // All Boards without Reset of the Display

// End of constructor list


void u8g2_prepare(void) {
  u8g2.setFont(u8g2_font_6x10_tf);
  u8g2.setFontRefHeightExtendedText();
  u8g2.setDrawColor(1);
  u8g2.setFontPosTop();
  u8g2.setFontDirection(0);
}

void u8g2_box_frame(uint8_t a) {
  u8g2.setFont(u8g2_font_helvR08_tr);
  char s[] = "Cage";
  int w = u8g2.getStrWidth(s);      // returns w = 24
  int h = u8g2.getAscent(s)- u8g2.GetDescent(s);
  int x = 5;
  int y = 11;
  u8g2.setFontPosBaseline();
  u8g2.firstPage();
  do
  {
    u8g2.drawStr(x, y, s);
    u8g2.drawFrame(x-1,y-u8g2.getAscent()-1, w+2, h+2);
  } while( u8g2.nextPage() );
}

void u8g2_disc_circle(uint8_t a) {
  u8g2.drawStr( 0, 0, "drawDisc");
  u8g2.drawDisc(10,18,9);
  u8g2.drawDisc(24+a,16,7);
  u8g2.drawStr( 0, 30, "drawCircle");
  u8g2.drawCircle(10,18+30,9);
  u8g2.drawCircle(24+a,16+30,7);
}

void u8g2_r_frame(uint8_t a) {
  u8g2.drawStr( 0, 0, "drawRFrame/Box");
  u8g2.drawRFrame(5, 10,40,30, a+1);
  u8g2.drawRBox(50, 10,25,40, a+1);
}

void u8g2_line(uint8_t a) {
  u8g2.drawStr( 0, 0, "drawLine");
  u8g2.drawLine(7+a, 10, 40, 55);
  u8g2.drawLine(7+a*2, 10, 60, 55);
  u8g2.drawLine(7+a*3, 10, 80, 55);
  u8g2.drawLine(7+a*4, 10, 100, 55);
}

void u8g2_triangle(uint8_t a) {
  uint16_t offset = a;
  u8g2.drawStr( 0, 0, "drawTriangle");
  u8g2.drawTriangle(14,7, 45,30, 10,40);
  u8g2.drawTriangle(14+offset,7-offset, 45+offset,30-offset, 57+offset,10-offset);
  u8g2.drawTriangle(57+offset*2,10, 45+offset*2,30, 86+offset*2,53);
  u8g2.drawTriangle(10+offset,40+offset, 45+offset,30+offset, 86+offset,53+offset);
}
char wifi[] = "(wifi)";
void u8g2_extra_page(uint8_t a)
{
  u8g2.setFont(u8g2_font_open_iconic_all_1x_t);
  u8g2.setFontPosTop();
  u8g2.drawGlyph(0, 0, 0xf8);
  u8g2.setFont(u8g2_font_6x13_tr);
  u8g2.drawStr(5, u8g2.getDisplayWidth(), wifi);
}

uint8_t draw_state = 0;

void draw(void) {
  u8g2_prepare();
  u8g2_extra_page(draw_state&5);
  /*
  switch(draw_state) {
    case 0: u8g2_box_frame(draw_state&5); break;
    case 1: u8g2_disc_circle(draw_state&5); break;
    case 2: u8g2_r_frame(draw_state&5); break;
    case 3: u8g2_line(draw_state&5); break;
    case 4: u8g2_triangle(draw_state&5); break;
    case 5: u8g2_extra_page(draw_state&5); break;
  }*/
}


void setup(void) {
  u8g2.begin();
}

void loop(void) {
  // picture loop  
  u8g2.clearBuffer();
  draw();
  u8g2.sendBuffer();
  Serial.println(draw_state);
  // increase the state
  draw_state++;
  if ( draw_state >= 6 )
    draw_state = 0;

  // deley between each page
  delay(100);

}

void setup(void) {
  
  // DOGS102 Shield (http://shieldlist.org/controlconnection/dogs102)
  u8g2.begin(/* menu_select_pin= */ 5, /* menu_next_pin= */ 4, /* menu_prev_pin= */ 2, /* menu_home_pin= */ 3);
  
  // DOGM128 Shield (http://shieldlist.org/schmelle2/dogm128) + DOGXL160 Shield
  // u8g2.begin(/* menu_select_pin= */ 2, /* menu_next_pin= */ 3, /* menu_prev_pin= */ 7, /* menu_home_pin= */ 8);

  // MKR Zero Test Board
  // u8g2.begin(/*Select=*/ 0, /*Right/Next=*/ 1, /*Left/Prev=*/ 2, /*Up=*/ 4, /*Down=*/ 3, /*Home/Cancel=*/ A6); 

  // Arduboy
  //u8g2.begin(/*Select=*/ A0, /*Right/Next=*/ 5, /*Left/Prev=*/ 9, /*Up=*/ 8, /*Down=*/ 10, /*Home/Cancel=*/ A1); // Arduboy DevKit
  //u8g2.begin(/*Select=*/ 7, /*Right/Next=*/ A1, /*Left/Prev=*/ A2, /*Up=*/ A0, /*Down=*/ A3, /*Home/Cancel=*/ 8); // Arduboy 10 (Production)

  u8g2.setFont(u8g2_font_6x12_tr);
}

struct menu_entry_type
{
  const uint8_t *font;
  uint16_t icon;
  const char *name;
};

struct menu_state
{
  int16_t menu_start;		/* in pixel */
  int16_t frame_position;		/* in pixel */
  uint8_t position;			/* position, array index */
};

/*
  Icon configuration
  Width and height must match the icon font size
  GAP: Space between the icons
  BGAP: Gap between the display border and the cursor.
*/
#define ICON_WIDTH 32
#define ICON_HEIGHT 32
#define ICON_GAP 4
#define ICON_BGAP 16
#define ICON_Y 32+ ICON_GAP

struct menu_entry_type menu_entry_list[] =
{
  { u8g2_font_open_iconic_embedded_4x_t, 65, "Clock Setup"},
  { u8g2_font_open_iconic_embedded_4x_t, 66, "Gear Game"},
  { u8g2_font_open_iconic_embedded_4x_t, 67, "Flash Light"},
  { u8g2_font_open_iconic_embedded_4x_t, 68, "Home"},
  { u8g2_font_open_iconic_embedded_4x_t, 72, "Configuration"},
  { NULL, 0, NULL } 
};

int8_t button_event = 0;		// set this to 0, once the event has been processed

void check_button_event(void)
{
  if ( button_event == 0 )
    button_event = u8g2.getMenuEvent();
}


void draw(struct menu_state *state)
{
  int16_t x;
  uint8_t i;
  x = state->menu_start;
  i = 0;
  while( menu_entry_list[i].icon > 0 )  
  {
    if ( x >= -ICON_WIDTH && x < u8g2.getDisplayWidth() )
    {
      u8g2.setFont(menu_entry_list[i].font);
      u8g2.drawGlyph(x, ICON_Y, menu_entry_list[i].icon );
    }
    i++;
    x += ICON_WIDTH + ICON_GAP;
    check_button_event();
  }
  u8g2.drawFrame(state->frame_position-1, ICON_Y-ICON_HEIGHT-1, ICON_WIDTH+2, ICON_WIDTH+2);
  u8g2.drawFrame(state->frame_position-2, ICON_Y-ICON_HEIGHT-2, ICON_WIDTH+4, ICON_WIDTH+4);
  u8g2.drawFrame(state->frame_position-3, ICON_Y-ICON_HEIGHT-3, ICON_WIDTH+6, ICON_WIDTH+6);
  check_button_event();
}


void to_right(struct menu_state *state)
{
  if ( menu_entry_list[state->position+1].font != NULL )
  {
    if ( (int16_t)state->frame_position+ 2*(int16_t)ICON_WIDTH + (int16_t)ICON_BGAP < (int16_t)u8g2.getDisplayWidth() )
    {
      state->position++;
      state->frame_position += ICON_WIDTH + (int16_t)ICON_GAP;
    }
    else
    {
      state->position++;      
      state->frame_position = (int16_t)u8g2.getDisplayWidth() - (int16_t)ICON_WIDTH - (int16_t)ICON_BGAP;
      state->menu_start = state->frame_position - state->position*((int16_t)ICON_WIDTH + (int16_t)ICON_GAP);
    }
  }
}

void to_left(struct menu_state *state)
{
  if ( state->position > 0 )
  {
    if ( (int16_t)state->frame_position >= (int16_t)ICON_BGAP+(int16_t)ICON_WIDTH+ (int16_t)ICON_GAP )
    {
      state->position--;
      state->frame_position -= ICON_WIDTH + (int16_t)ICON_GAP;
    }    
    else
    {
      state->position--; 
      state->frame_position = ICON_BGAP;
      state->menu_start = state->frame_position - state->position*((int16_t)ICON_WIDTH + (int16_t)ICON_GAP);      
    }
  }
}


uint8_t towards_int16(int16_t *current, int16_t dest)
{
  if ( *current < dest )
  {
    (*current)++;
    return 1;
  }
  else if ( *current > dest )
  {
    (*current)--;
    return 1;
  }
  return 0;
}

uint8_t towards(struct menu_state *current, struct menu_state *destination)
{
  uint8_t r = 0;
  uint8_t i;
  for( i = 0; i < 6; i++ )
  {
    r |= towards_int16( &(current->frame_position), destination->frame_position);
    r |= towards_int16( &(current->menu_start), destination->menu_start);
  }
  return r;
}



struct menu_state current_state = { ICON_BGAP, ICON_BGAP, 0 };
struct menu_state destination_state = { ICON_BGAP, ICON_BGAP, 0 };

void loop(void) {
  do
  {
    u8g2.firstPage();
    do
    {
      draw(&current_state);  
      u8g2.setFont(u8g2_font_helvB10_tr);  
      u8g2.setCursor((u8g2.getDisplayWidth()-u8g2.getStrWidth(menu_entry_list[destination_state.position].name))/2,u8g2.getDisplayHeight()-5);
      u8g2.print(menu_entry_list[destination_state.position].name);
      check_button_event();
      delay(10);
    } while( u8g2.nextPage() );
    if ( button_event == U8X8_MSG_GPIO_MENU_NEXT )
      to_right(&destination_state);
    if ( button_event == U8X8_MSG_GPIO_MENU_PREV )
      to_left(&destination_state);
    if ( button_event == U8X8_MSG_GPIO_MENU_SELECT )
    {
      u8g2.setFont(u8g2_font_helvB10_tr);  
      u8g2.userInterfaceMessage("Selection:", menu_entry_list[destination_state.position].name, "", " Ok ");
    }
    if ( button_event > 0 )	// all known events are processed, clear event
      button_event = 0;
  } while ( towards(&current_state, &destination_state) );
}