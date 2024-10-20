import serial

# Configuração da porta serial
ser = serial.Serial('/dev/pts/17', timeout=1)

def get_integer_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Por favor, insira um número inteiro válido.")


while True:
    # Entrada de dados
    n1 = get_integer_input("Digite o primeiro número inteiro: ")
    n2 = get_integer_input("Digite o segundo número inteiro: ")
    op = input("Digite a operação (+, -, *, /): ")

    # Validação da operação
    if op not in ['+', '-', '*', '/']:
       print("Operação inválida. Use +, -, * ou /.")
       continue

    # Montagem da mensagem
    mensagem = f"{n1};{n2};{op}\n"

    # Envio da mensagem
    ser.write(mensagem.encode())

    # Espera pela resposta
    resposta = ser.readline().decode().strip()

    # Exibição do resultado
    print(f"Resultado: {resposta}")

    # Pergunta se deseja continuar
    continuar = input("Deseja fazer outro cálculo? (s/n): ")
    if continuar.lower() != 's':
        break

ser.close()
