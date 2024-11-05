# Introdução

Essa é uma aplicação que consiste num projeto Godot que cria um servidor local UDP para recepção de informações de um dispositivo conectado que realiza conexão serial.
Há um script Python que roda em segundo plano que intercepta as informações da conexão serial e envia-as para a Godot via UDP.

# Requisitos

* [Godot 4.x](https://godotengine.org)
* Instalação do [Python](https://www.python.org/downloads/)
* Instalação do pacote _pyserial_ (para a leitura de portas seriais)

## Instalando o pyserial

Com Python instalado, verifique se possui o _pip_ (gerenciador de pacotes do Python) instalado usando:


Linux
```
pip3 --version
```

Windows
```
pip --version
```


Caso o _pip_ não esteja instalado, instale-o usando os seguintes comandos:


Linux
``` 
sudo apt-get install python3-pip
```

Windows
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```


Em seguida, instale o pacote _pyserial_


Linux
```
pip3 install pyserial
```

Windows
``` 
pip install pyserial
```

No Linux, talvez seja necessário atualizar o pyserial para uma versão mais recente caso ele já esteja instalado. Use o seguinte comando:
```
pip3 install --upgrade pyserial
```

# Utilização

Com a Godot, Python e pyserial instalados, clone o repositório na pasta de sua preferência, abra a Godot e escaneie a pasta desse projeto. Em seguida, rode a cena principal ou qualquer outra cena.
