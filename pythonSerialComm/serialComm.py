import sys
import time
import socket
import threading

# Biblioteca para acessar as portas seriais do arduino.
import serial
import serial.tools.list_ports

def readData(baudrate, udp_ip, udp_port):
    '''Lê a primeira porta serial que está tentando enviar informações
    e envia as informações para a Godot via UDP.'''

    state = {"readAttempts": 0, "portIndex": 0} # Estado de tentativas e index da porta na lista de portas

    def connectSerial(state):
        '''Tenta conectar na primeira porta serial que está enviando informações'''
        ports = serial.tools.list_ports.comports()  # Pega a lista de portas que estão usando conexão serial

        # Enquanto houver portas disponíveis
        while ports:
            try:
                ser = serial.Serial(ports[state["portIndex"]].device, baudrate, timeout=1)  # Tenta conectar com a porta serial do Arduino
                print(f"Conectado à porta serial: {ser.port}")
                return ser
            
            # Se der erro de conexão com uma porta, tenta a próxima até dar certo
            except (serial.SerialException, IndexError) as e:
                print("Erro de comunicação serial: ", e)
                print("Tentando conectar à próxima porta...")

                state["portIndex"] = (state["portIndex"] + 1) % len(ports)
                if state["portIndex"] == 0:  # Todas as portas foram tentadas, espera antes de tentar novamente
                    print("Todas as portas foram tentadas!! Aguardando 3 segundos para tentar novamente")
                    time.sleep(3)
                    ports = serial.tools.list_ports.comports()  # Atualiza a lista de portas
        print("Sem portas seriais disponíveis para conexão")
        return None

    ser = None
    
    # Configura o socket UDP para mandar o pacote
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_address = (udp_ip, udp_port)

    while True:
        try:
            # Se a porta for nula, tenta conectar denovo
            if ser is None:
                ser = connectSerial(state)
                if ser is None:
                    print("Reconectando em 3 segundos...")
                    time.sleep(3)
                    continue

            if ser.in_waiting > 0:  # Se há dados esperando para serem lidos do Arduino
                # Decodifica e remove caracteres indesejados
                state["readAttempts"] = 0
                line = ser.read_all().decode('utf-8', errors='ignore').strip()
                clean_line = line.replace("\r", "").replace("\n", "")  # Remove caracteres adicionais, se presentes
                print("Linha:", clean_line)  # Imprime a linha limpa no console para verificação

                try:
                    udp_socket.sendto(clean_line.encode(), udp_address)  # Envia um pacote via UDP que contém a linha
                    print("Pacote enviado.")
                except Exception as e:
                    print(f"Erro ao enviar pacote: {e}")

            else:
                print("Sem mensagens enviadas")
                state["readAttempts"] += 1 # Aumenta as tentativas de leitura
                if state["readAttempts"] > 4:
                    state["portIndex"] = (state["portIndex"] + 1) % len(serial.tools.list_ports.comports())
                    state["readAttempts"] = 0 # Reseta as tentativas de leitura e tenta conectar-se novamente
                    ser = connectSerial(state)

            time.sleep(0.1)  # Delay de leitura; ajuste conforme necessário

        except (serial.SerialException, Exception) as e:
            print(f"Erro de leitura/envio de dados: {e}")
            if ser:
                ser.close()  # Fecha a conexão serial para poder tentar uma nova conexão
            ser = None

if __name__ == "__main__":
    if len(sys.argv) > 3:
        baudrate = int(sys.argv[1])
        ip = sys.argv[2]
        port = int(sys.argv[3])

        # Inicia a leitura serial em threading para aumento de desempenho
        serial_thread = threading.Thread(target=readData, args=(baudrate, ip, port))
        serial_thread.start()
        serial_thread.join()
    else:
        print("Uso: python serial_comm.py <baudrate> <ip> <port>")
