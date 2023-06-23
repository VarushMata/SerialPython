//Código en Arduinio para obtener respuesta del color predominante la imagen
//Y encender un led de acuerdo a este color
int LED_R = 4;
int LED_G = 5;
int LED_B = 6;

char dato;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);


}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    dato = Serial.read();
    if(dato == 'R'){
      digitalWrite(4,HIGH);
      digitalWrite(5,LOW);
      digitalWrite(6,LOW);
    }
    else if(dato == 'G'){
      digitalWrite(4,LOW);
      digitalWrite(5,HIGH);
      digitalWrite(6,LOW);
    }
    else if(dato == 'B'){
      digitalWrite(4,LOW);
      digitalWrite(5,LOW);
      digitalWrite(6,HIGH);
    }
  }
}

