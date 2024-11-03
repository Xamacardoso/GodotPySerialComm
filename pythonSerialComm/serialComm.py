import sys
import time
import socket
import threading

# Bilblioteca para acessar as portas seriais do arduino.
import serial
import serial.tools.list_ports


def readData(baudrate, udp_ip, udp_port):
    '''Lê a primeira porta serial que está tentando enviar informações
    e envia as informações para a Godot via UDP.'''

    def connectSerial():
        '''Tenta conectar na primeira porta serial que está enviando informações'''
        ports = serial.tools.list_ports.comports(); # Pega a lista de portas que estão usando conexão serial
        for port in ports:
            try:
                ser = serial.Serial(port.device, baudrate, timeout=1)  # Tenta conectar com a porta serial do Arduino
                print(f"Conectado à porta serial: {port.device}")
                return ser

            except (serial.SerialException, IndexError) as e:
                print("Erro de comunicação serial: ", e);

        print("Sem portas seriais disponíveis para conexão")
        return None

    ser = None
    
    # Configura o socket UDP para mandar o pacote
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_adress = (udp_ip, udp_port)
    while True:

        # Tenta conectar contínuamente a uma porta serial
        try:
            ser = connectSerial()
            if ser is None:
                print("Reconectando em 3 segundos...")
                time.sleep(3)
                continue

            if ser.in_waiting > 0:  # Se há dados esperando para serem lidos do Arduino
                
                # Decodifica e remove caracteres indesejados
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                # Remove caracteres adicionais, se presentes
                clean_line = line.replace("\r", "").replace("\n", "")  

                print(clean_line)  # Imprime a linha limpa no console para verificação
                try:
                    udp_socket.sendto(clean_line.encode(), udp_adress) # Envia um pacote via UDP que contém a linha
                    print("Pacote enviado.")
                except Exception as e:
                    print(f"Erro ao enviar pacote: {e}")            
            time.sleep(0.1)  # Delay de leitura; ajuste conforme necessário

        except (serial.SerialException, Exception) as e:
            print(f"Erro de leitura/envio de dados: {e}")
            ser.close() # Fecha a conexão serial para poder tentar uma nova conexão
            ser = None


if __name__ == "__main__":
    if len(sys.argv) > 3:
        baudrate = int(sys.argv[1])
        ip = sys.argv[2]
        port = int(sys.argv[3])

        # Inicia a leitura serial em threadding para aumento de desempenho
        serial_thread = threading.Thread(target=readData, args=(baudrate, ip, port))
        serial_thread.start()
        serial_thread.join()

    else:
        print("Uso: python serial_comm.py <baudrate> <ip> <port>")
    
