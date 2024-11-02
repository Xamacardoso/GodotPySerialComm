#include <Esplora.h>

void setup() {
  Serial.begin(9600);  // Inicia a comunicação serial na mesma taxa de transmissão configurada no Godot e no Python
}

void loop() {
  // Lê os valores do joystick
  int joystickX = Esplora.readJoystickX();  // Valor de -512 a 512
  int joystickY = Esplora.readJoystickY();  // Valor de -512 a 512

  // Lê os valores do acelerômetro
  int accelX = Esplora.readAccelerometer(X_AXIS);  // Valor aproximado entre -512 a 512
  int accelY = Esplora.readAccelerometer(Y_AXIS);  // Valor aproximado entre -512 a 512
  int accelZ = Esplora.readAccelerometer(Z_AXIS);  // Valor aproximado entre -512 a 512

  // Formata a saída em uma string, separando cada valor por vírgulas
  String data = "[" + String(joystickX) + "," + String(joystickY) + "," +
                String(accelX) + "," + String(accelY) + "," + String(accelZ) + "]";

  // Envia os dados pela serial
  Serial.println(data);

  // Aguarda um curto período antes de enviar novamente
  delay(100);  // Ajuste o delay conforme necessário para o ritmo de leitura desejado
}
