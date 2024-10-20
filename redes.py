import serial
import time

if __init__ == '__main__':
    # Configuração da porta serial
    ports = list(map(int,input("Digite as portas seriais: ").split()))
    serial_ports = list(serial.Serial('/dev/pts/{port}', timeout=1) for port in ports)
    for serial_port in serial_ports:
        print(f"Conectado à porta: {serial_port.name}")

    for serial_port in serial_ports:
        print(f"Fechando porta: {serial_port.name}")
        serial_port.close()