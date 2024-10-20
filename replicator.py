import serial
import time
import os

# Replicador de mensagens entre portas seriais
if __name__ == '__main__':
    # Configuração e abertura das portas seriais
    ports = list(map(int,input("Digite as portas seriais: ").split()))
    serial_ports = list(serial.Serial(f"/dev/pts/{port}", timeout=1) for port in ports)
    for serial_port in serial_ports:
        print(f"Conectado à porta: {serial_port.name}")
    #Modo de operação de replicação de mensagens
    continue_operation = True
    while continue_operation:
        for in_port in serial_ports:
            if in_port.in_waiting:
                msg = in_port.read(in_port.in_waiting)
                continue_operation = msg != b'exit'
                for out_port in serial_ports:
                    if in_port != out_port:
                        out_port.write(msg)
                        print(f"Enviando mensagem de {in_port.name} para {out_port.name}: {msg}")
        time.sleep(0.1)
    # Fechamento das portas seriais                
    for serial_port in serial_ports:
        print(f"Fechando porta: {serial_port.name}")
        serial_port.close()