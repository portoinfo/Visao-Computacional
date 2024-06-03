String comando = ""; //Variável que guarda o comando 
bool comandoFinalizado = false; //Variável que confirma se recebeu o comando completo ou não 

void setup() { 
  Serial.begin(115200); 
  comando.reserve(200); // reserva 200 caracteres para o comando 
  pinMode(3, OUTPUT); 
  digitalWrite(3, HIGH); 
} 

void loop() { 
  
  if(comandoFinalizado){ //Se o comando foi finalizado 
    if(comando.startsWith("0")){ // E se o comando recebido for 0 
      digitalWrite(3, HIGH); // Desliga a lâmpada através do relé 
    } 
    if(comando.startsWith("1")){// Se o comando recebido for 1 
      digitalWrite(3, LOW); //Acende a lâmpada através do relé 
    } 
    if(comando.startsWith("2")){ // E se o comando recebido for 2
      digitalWrite(5, LOW); // Apaga ao LED
    } 
    if(comando.startsWith("3")){// Se o comando recebido for 3 
      digitalWrite(5, HIGH); //Acende o LED
    } 
    comando = ""; // Limpa a variável do comando 
    comandoFinalizado = false; // retorna a variável comandoFinalizado como falsa 
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