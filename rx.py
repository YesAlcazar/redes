import serial

srx = serial.Serial('/dev/pts/39')

r = srx.read(3)
print(r)

srx.write(b'meu consagrado')

srx.close()
