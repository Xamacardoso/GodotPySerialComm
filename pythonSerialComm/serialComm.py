import sys
import time
import socket

# Bilblioteca para acessar as portas seriais do arduino.
import serial
import serial.tools.list_ports


def readData(baudrate, udp_ip, udp_port):
    '''Lê a primeira porta serial que está tentando enviar informações
    e envia as informações para a Godot via UDP.'''

    try:
        ports = serial.tools.list_ports.comports(); # Pega a lista de portas que estão usando conexão serial
        port = ports[0].name;  # Tenta conectar com a primeira porta serial
        ser = serial.Serial(port, baudrate, timeout=1)  # Tenta conectar com a porta serial do Arduino
        
        # Mostra as portas seriais disponíveis
        print("Portas: ")
        for port in ports:
            print(port.name)


        # Configura o socket UDP para mandar o pacote
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_adress = (udp_ip, udp_port)

        while True:
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
                    break

            time.sleep(0.1)  # Delay de leitura; ajuste conforme necessário

    except serial.SerialException as e:
        print(f"Erro de comunicação serial: {e}")

    except IndexError as e:
        print(f"Erro, não há conexões seriais disponíveis!")

    except Exception as e:
        print(f"Erro de conexão UDP: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        baudrate = int(sys.argv[1])
        ip = sys.argv[2]
        port = int(sys.argv[3])
        readData(baudrate, ip, port)
    else:
        print("Uso: python serial_comm.py <baudrate> <ip> <port>")
