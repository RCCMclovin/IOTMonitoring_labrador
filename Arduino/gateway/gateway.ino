//Includes para a utilizacao da RadioHead
#include <SPI.h>
#include <RH_RF95.h>

//Criação de variáveis globais
RH_RF95 rf95;                         //Instancia do modulo de transmissao
int sf = 7;                           //Valores do Spreading Factor {7, 8, 9, 10, 11, 12}
int cr = 5;                           //Valores do Coding Rate {5, 6, 7, 8}
char id_anterior = '-';               //Identificador da mensagem anterior

void setup() {
  //Inicializa a serial do Arduino
  Serial.begin(9600);

  //Inicialização do modulo
  if (!rf95.init()){//Caso o módulo falhe a inicialização
    Serial.println("Falha na inicialização, verifique o equipamento");
    while(1);
  }//Caso a inicialização funcione 
  Serial.println("Módulo Inicializado com sucesso!");

  //Configuração dos valores de Spreading Factor e Coding Rate
  rf95.setSpreadingFactor(sf);//valore entre 7 e 12
  Serial.println("Spreading Factor definido para " + String(sf) + ".");
  
  rf95.setCodingRate4(cr);//  fração com denominador de 5 até 8
  Serial.println("Coding Rate definido para " + String(cr) + ".");
  
  //Fim do Set Up
  Serial.println("Fim do Setup.");
  Serial.println("");

}

void loop() {
  receiveMessage();
}

void receiveMessage(){
  //Recebe a mensagem
  if (rf95.available()){
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);
    
    if (rf95.recv(buf, &len)){
      if(id_anterior != (char) buf[0]){
        for(int i = 0; i < 7; i++){
          Serial.print( (char) buf[i]);
        }
        Serial.println();
        id_anterior = (char) buf[0];
      }
      
      //Responde a mensagem
      uint8_t data[] = "Mensagem recebida.";
      rf95.send(data, sizeof(data));
      rf95.waitPacketSent();
      Serial.println("Mensagem Respondida.");
    }
  }
}
