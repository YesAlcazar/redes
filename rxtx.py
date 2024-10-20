import serial

sb1=serial.Serial("/dev/pts/18")
sb2=serial.Serial("/dev/pts/47")

l=sb1.read(1)
vl=int(l[0])
msg=sb1.read(vl)

sb2.write(l)
sb2.write(msg)

msg=sb2.read(4)
sb1.write(msg)
