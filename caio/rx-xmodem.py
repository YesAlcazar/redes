import serial
import time

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
ser = serial.Serial('/dev/pts/18', timeout=1)

def calculate_checksum(data):
    return sum(data) & 0xFF

def receive_packet():
    start_time = time.time()
    while time.time() - start_time < TIMEOUT:
        header = ser.read(1)
        if header == SOH:
            packet_number = ser.read(1)[0]
            packet_number_complement = ser.read(1)[0]
            if packet_number + packet_number_complement != 255:
                ser.write(NAK)
                continue

            data = ser.read(PACKET_SIZE)
            checksum = ser.read(1)[0]

            if calculate_checksum(data) != checksum:
                ser.write(NAK)
                continue

            ser.write(ACK)
            return packet_number, data
        elif header == EOT:
            ser.write(ACK)
            return None
        elif header == CAN:
            raise Exception("Transmission cancelled by sender")

    raise Exception("Timeout waiting for packet")

def receive_file(filename):
    with open(filename, 'wb') as file:
        expected_packet = 1

        # Inicia a transmissão
        ser.write(NAK)

        while True:
            try:
                result = receive_packet()
                if result is None:  # EOT received
                    break

                packet_number, data = result
                if packet_number == expected_packet:
                    file.write(data.rstrip(b'\x1A'))  # Remove padding
                    expected_packet = (expected_packet + 1) % 256
                else:
                    raise Exception(f"Unexpected packet number. Expected {expected_packet}, got {packet_number}")

            except Exception as e:
                print(f"Error: {str(e)}")
                if str(e).startswith("Timeout"):
                    ser.write(NAK)
                else:
                    ser.write(CAN)
                    ser.write(CAN)
                    raise


filename = input("Digite o nome do arquivo para salvar os dados recebidos: ")

print(f"Aguardando recebimento do arquivo. Será salvo como: {filename}")

try:
    receive_file(filename)
    print(f"Arquivo recebido e salvo como '{filename}' com sucesso!")
except Exception as e:
    print(f"Erro durante a recepção: {str(e)}")
finally:
    ser.close()
