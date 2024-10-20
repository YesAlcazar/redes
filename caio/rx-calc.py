import serial

ser = serial.Serial('/dev/pts/18', timeout=1)

def calcular(n1, n2, op):
    if op == '+':
        return n1 + n2
    elif op == '-':
        return n1 - n2
    elif op == '*':
        return n1 * n2
    elif op == '/':
        try:
            return n1 // n2  # Divisão inteira
        except ZeroDivisionError:
            return "Erro: Divisão por zero"


while True:
    # Espera por dados
    dados = ser.readline().decode().strip()

    if dados:
        # Separação dos dados
        try:
            n1, n2, op = dados.split(';')
            n1 = int(n1)
            n2 = int(n2)
        except ValueError:
            resultado = "Erro: Dados inválidos"
        else:
            # Cálculo
            resultado = calcular(n1, n2, op)
        # Envio do resultado
        ser.write(f"{resultado}\n".encode())
