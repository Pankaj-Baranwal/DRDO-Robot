import serial, time
arduino = serial.Serial('/dev/ttyACM1', 9600)


while True:
	option = int(raw_input("Enter 1"))
	write_serial = arduino.write(str(option))
	arduino.read()
	read_serial = arduino.read()	
	print read_serial


