char dataString[50] = {0};

void setup() {
Serial.begin(9600);              //Starting serial communication
}
  
void loop() {
	
  Serial.println(dataString);   // send the data
  delay(1000);                  // give the loop some break
}