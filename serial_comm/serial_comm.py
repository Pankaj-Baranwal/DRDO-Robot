import serial, time
arduino = serial.Serial('/dev/ttyACM0', 9600)

while True:
	option = raw_input("Enter a-i or l,r or z.")
	write_serial = arduino.write(str(option))
	arduino.read()
	read_serial = arduino.read()
	print read_serial


