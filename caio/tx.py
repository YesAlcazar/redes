import serial

stx = serial.Serial('/dev/pts/38')

stx.write(b'ola')

r = stx.read(14)
print(r)

stx.close()

