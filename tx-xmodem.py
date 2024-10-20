import serial
import time
import os

# Constantes XMODEM
SOH = b'\x01'  # Start of Header
EOT = b'\x04'  # End of Transmission
ACK = b'\x06'  # Acknowledge
NAK = b'\x15'  # Negative Acknowledge
CAN = b'\x18'  # Cancel

# Configuração
PACKET_SIZE = 128
MAX_RETRIES = 10
TIMEOUT = 10

# Configuração da porta serial
ser = serial.Serial('/dev/pts/17', timeout=1)

def calculate_checksum(data):
    return sum(data) & 0xFF

def send_packet(packet_number, data):
    packet = SOH + bytes([packet_number]) + bytes([255 - packet_number]) + data
    checksum = calculate_checksum(data)
    packet += bytes([checksum])

    for _ in range(MAX_RETRIES):
        ser.write(packet)
        response = ser.read(1)
        if response == ACK:
            return True
        elif response == CAN:
            raise Exception("Transmission cancelled by receiver")
    return False

def send_file(filename):
    with open(filename, 'rb') as file:
        packet_number = 1

        # Espera pelo início da transmissão
        start_time = time.time()
        while time.time() - start_time < TIMEOUT:
            if ser.read(1) == NAK:
                break
        else:
            raise Exception("Timeout waiting for transmission start")

        while True:
            data = file.read(PACKET_SIZE)
            if not data:
                break
            if len(data) < PACKET_SIZE:
                data = data.ljust(PACKET_SIZE, b'\x1A')  # Pad com SUB (Ctrl-Z)

            if not send_packet(packet_number, data):
                raise Exception(f"Failed to send packet {packet_number}")

            packet_number = (packet_number + 1) % 256

    # Envio do EOT
    for _ in range(MAX_RETRIES):
        ser.write(EOT)
        if ser.read(1) == ACK:
            return True
    raise Exception("Failed to send EOT")

filename = input("Digite o nome do arquivo a ser enviado: ")

if not os.path.exists(filename):
    print(f"Erro: O arquivo '{filename}' não existe.")

print(f"Enviando arquivo: {filename}")
print("Aguardando receptor...")

try:
    if send_file(filename):
        print("Arquivo enviado com sucesso!")
    else:
        print("Falha ao enviar o arquivo.")
except Exception as e:
    print(f"Erro durante a transmissão: {str(e)}")
finally:
    ser.close()
