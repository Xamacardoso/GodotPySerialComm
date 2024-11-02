extends Node

const MAX_PACKET_SIZE = 18;

# Cria um servidor local e um buffer para armazenamento de informações
var udpListener = UDPServer.new();
var buffer = PackedByteArray();

# IP de conexão UDP. "127.0.0.1" é o padrão para o servidor local.
# Mudar o IP conforme a necessidade, caso a utilização não seja no servidor local.
var ip = "127.0.0.1"; 
var PORT = 5005; # Porta da conexão UDP

var baud_rate = 9600; # Frequencia de envio de sinais do Arduino

# Adapta o comando para chamar o script python em sistemas windows ou linux
var pythonCMD = "python" if OS.get_name() == "Windows" else  "python3";

var pythonFilePath : String; # Caminho do arquivo python
var procStatus : int;


func _ready():
	# Tenta "ouvir" o envio de pacotes de outras fontes na mesma porta
	if udpListener.listen(PORT) == OK:
		print("Servidor escutando na porta: ", PORT);
	else:
		printerr("Erro ao iniciar o servidor UDP.");

	getAbsFilePath()
	
	# Argumentos da linha de comando que chama o script python
	var cmd = [pythonFilePath, str(baud_rate), ip, PORT];
	
	# Chama o script python em um terminal que executa independentemente do Godot
	procStatus = OS.create_process(pythonCMD, cmd, true);
	
	# Terminal iniciado com sucesso
	if (procStatus != -1):
		print("PID do processo que roda o Python: ", procStatus);
		print("Iniciando leitura...");
	else:
		print("Erro ao iniciar o processo do terminal!");

func _physics_process(delta: float) -> void:
	getUdpData();

## Fecha o terminal quando a janela do jogo é fechada
func _exit_tree() -> void:
	printerr("Fechou");
	OS.kill(procStatus);

## Pega o caminho absoluto do script python para executá-lo no terminal
func getAbsFilePath() -> void:
	var relPythonPath = FileAccess.open("res://pythonSerialComm/serialComm.py", FileAccess.READ) 
	pythonFilePath = relPythonPath.get_path_absolute();
	print("Python Path: ",pythonFilePath);

## Recebe pacotes via UDP e verifica se é necessário tratá-lo caso seja JSON
func getUdpData() -> void:
	udpListener.poll(); # Checa se há algum pacote enviado para o servidor
	
	# Checa se há pacotes sendo enviados para o socket UDP
	if udpListener.is_connection_available():
		
		# Retorna a primeira conexão pendente no mesmo endereço e porta do servidor
		var peer : PacketPeerUDP = udpListener.take_connection();
		
		# Pega o pacote que foi enviado nessa conexão e o adiciona ao buffer
		var packet = peer.get_packet();
		buffer += packet;
		
		 # Converte o buffer em string para verificar o conteúdo
		var data_string = buffer.get_string_from_utf8()
		print("DADOS DO PACOTE: ", data_string)
		printerr("TAMANHO DO PACOTE: ", packet.size())

		# Verifica se o buffer contém uma mensagem completa em JSON
		if data_string.begins_with("{") and data_string.ends_with("}"):
			# Se for uma mensagem JSON completa, processa e limpa o buffer
			processJson(data_string)
			buffer.clear()  # Limpa o buffer após o processamento

		elif buffer.size() > 1:  # Limita o tamanho do buffer
			buffer.clear()  # Limpa o buffer se exceder o tamanho
			
			
## Processa a string JSON recebida
func processJson(data: String):
	var json = JSON.new()
	var parsedJson = json.parse(data) # Converte os dados da string para JSON
	if parsedJson.error == OK:
		var parsed_data = parsedJson.result # Pega o conteúdo do JSON
		print("Dados recebidos e processados:", parsed_data)
	else:
		printerr("Erro ao processar JSON:",parsedJson.error.get_error_message())
