//Includes para a utilização da RadioHead
#include <SPI.h>
#include <RH_RF95.h>

#include <Thermistor.h> 

//Criação de variáveis globais
RH_RF95 rf95;                         //Instancia do modulo de transmissao
int sf = 7;                           //Valores do Spreading Factor{7, 8, 9, 10, 11, 12}; 
int cr = 5;                           //Valores do Coding Rate {5, 6, 7, 8}
int contador = 0;                     //Contador do número da mensagem atual
char id[] = {'0', '1', '2', '3', '4'};//Identificador do número da mensagem atual
int espera = 5000;                    //Tempo de espera entre coletas em ms
uint8_t msg[7];                       //Base da mensagem a ser enviada
Thermistor temp(2);                   //Temp, variável que representa o sensor de temperatura na porta 2
float temperature;    

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
  
    //***** MEDIÇÕES ****/////
  temperature = medeTemp();

  //Preparação da MSG
  //Serial.println(temperature);
  char sz[5], pckt[7];
  dtostrf(temperature,5,2,sz);
  pckt[0] = id[contador];
  pckt[1] = '*';
  for(int i = 0; i < 5; i++){
    pckt[2+i] = sz[i];
  }
  memcpy(msg, &pckt, sizeof(pckt)); //Transforma o char para uint8_t
  Serial.println("Mensagem preparada!");

  //Envio da mensagem
  sendMessage();
  for(int i = 0; i < 7; i++){
    Serial.print( (char) msg[i]);
  }
  Serial.println();
  
  //intervalo entre mensagens
  delay(espera);
  if(contador == 4) contador = 0;
  else contador ++;
}

//Funcao responsavel pelo envio e captura de mensagens
void sendMessage(){
  bool aux = true;
  while(aux){
    rf95.send(msg,sizeof(msg));
    rf95.waitPacketSent();
    if(rf95.waitAvailableTimeout(3000)){
      aux = false;
    }
  }
}

float medeTemp(){
  if(contador < 4){
    return temp.PegaValorTemp(); //Temperature, recebe o valor medido no sensor temp
  }
  return -10.0;
}
  
