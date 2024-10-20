import serial
import time
import os
import threading


# Função para replicar mensagens entre portas seriais
def repply_all(msg : bytes, serial_ports : list, sender_port : serial.Serial = None) -> None:
    if sender_port:
        for serial_port in serial_ports:
            if serial_port != sender_port:
                serial_port.write(msg)
                print(f"Enviando mensagem de {sender_port.name} para {serial_port.name}: {msg}")
    else:
        for serial_port in serial_ports:
            serial_port.write(msg)
            print(f"Enviando mensagem de {serial_port.name}: {msg}")

def create_serial_ports(ports : list) -> list:
    return list(serial.Serial(f"/dev/pts/{port}", timeout=1) for port in ports)

# Replicador de mensagens entre portas seriais
if __name__ == '__main__':
    # Configuração e abertura das portas seriais
    ports = list(map(int,input("Digite as portas seriais: ").split()))
    serial_ports = list(serial.Serial(f"/dev/pts/{port}", timeout=1) for port in ports)
    for serial_port in serial_ports:
        print(f"Conectado à porta: {serial_port.name}")
    print("Digite 'exit' em qualquer porta para encerrar a replicação de mensagens.")
    #Modo de operação de replicação de mensagens
    continue_operation = True
    while continue_operation:
        for in_port in serial_ports:
            if in_port.in_waiting > 0:
                msg = in_port.read(in_port.in_waiting)
                continue_operation = msg != b'exit'
                repply_all(msg, serial_ports, in_port)
        time.sleep(0.1)
    # Fechamento das portas seriais                
    for serial_port in serial_ports:
        print(f"Fechando porta: {serial_port.name}")
        serial_port.close()


