import serial

sa=serial.Serial("/dev/pts/17")

msg=input("msg: ")
l=len(msg)
sa.write(l.to_bytes(1,"big"))
sa.write(msg.encode())

msg=sa.read(4)
print(msg.decode())
