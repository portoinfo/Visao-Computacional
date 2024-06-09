String comando = ""; //Variável que guarda o comando 
bool comandoFinalizado = false; //Variável que confirma se recebeu o comando completo ou não 
#define relay1 3  //  pin 3
#define relay2 5  // ppin 5
#define relay3 9  //  pin 9

void setup() { 
  Serial.begin(115200); 
  comando.reserve(200); // reserva 200 caracteres para o comando 
  pinMode(relay1, OUTPUT); 
  pinMode(relay2, OUTPUT); 
  pinMode(relay3, OUTPUT); 
  digitalWrite(relay1, LOW);
  digitalWrite(relay2, HIGH);
  digitalWrite(relay3, HIGH);

  digitalWrite(relay1, HIGH);
  delay(500); 
  digitalWrite(relay1, LOW);
  delay(500); 

  delay(500); 
  digitalWrite(relay2, LOW);
  delay(500); 
  digitalWrite(relay2, HIGH); 

  delay(500); 
  digitalWrite(relay3, LOW);
  delay(500); 
  digitalWrite(relay3, HIGH); 
} 

void loop() { 
  
  if(comandoFinalizado){ //Se o comando foi finalizado 
    if(comando.startsWith("0")){  // If received comand = 0 
      digitalWrite(relay1, HIGH); // Active relay 1
    } 
    if(comando.startsWith("1")){ // If received comand = 1
      digitalWrite(relay1, LOW); // Deactive relay 1
    } 
    if(comando.startsWith("2")){  // If received comand = 2
      digitalWrite(relay2, LOW); // Active relay 2
    } 
    if(comando.startsWith("3")){ // If received comand = 3
      digitalWrite(relay2, HIGH); // Deactive relay 2
    } 
    if(comando.startsWith("4")){ // If received comand = 4
      digitalWrite(relay3, LOW); // Active relay 3
    } 
    if(comando.startsWith("5")){ // If received comand = 5
      digitalWrite(relay3, HIGH); // Deactive relay 3
    } 
    comando = ""; // Clean command value
    comandoFinalizado = false; // return FALSE value
  } 
}
 
 void serialEvent(){
    while (Serial.available()){
      char inChar = (char)Serial.read();
      comando += inChar;
      if(inChar == '\n'){
        comandoFinalizado = true;
      }
    }
  }