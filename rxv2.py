import serial

sc=serial.Serial("/dev/pts/48")

l=sc.read(1)
vl=int(l[0])
msg=sc.read(vl)
print(msg.decode())

msg="Ola\n"
sc.write(msg.encode())
