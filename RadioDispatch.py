import winsound
import time
import serial

# ----------< Configuration >----------

QC2_Tone_A_Duration = 1000 # ms (Default: 1000ms)
QC2_Tone_B_Duration = 3000 # ms (Default: 3000ms)

DTMF_Tone_Interval = 25 # ms (Default: 25ms)
DTMF_Tone_Duration = 50 # ms (Default: 50ms)

ST_Tone_Duration = 3000 # ms (Default: 3000ms)

PTT_COM_Port = 'VOX' # Set as 'VOX' for no PTT control. Set as 'COM#' with # being the COM Port number.
PTT_COM_Pin = 'RTS' # RTS or DTR pin for PTT Control

# ----------< Configuration >----------

print('\n-----------------------------------')
print('KJ7BRE Communications Paging System')
print('Version: 0.82B    Evan Vander Stoep')
print('-----------------------------------\n')

help_msg = """

  Unit ID Numbers
--------------------
1 - [Handheld 1]
2 - [Handheld 2]
3 - [Handheld 3]
4 - [Handheld 4]
8 - [Base 1]
9 - [Base 2]
10 - [Anytone 878]
91 - [Siren Attack]
92 - [Siren Alert]
93 - [Siren Test/Cancel]

"""

if PTT_COM_Port.upper() != 'VOX':
	ser = serial.Serial('COM5')
c_state = False

def PTT(state): # Transmiter Control
	if PTT_COM_Port.upper() != 'VOX':
		if PTT_COM_Pin == 'RTS':
			ser.setRTS(state)
		if PTT_COM_Pin == 'DTR':
			ser.setDTR(state)
	c_state = state
	if c_state == None:
		c_state = False
	return c_state

def QC2(A,B): # Quick Call II (2-Tone)
	winsound.Beep(A, QC2_Tone_A_Duration)
	winsound.Beep(B, QC2_Tone_B_Duration)
	PTT(False)
	return True

def ST(A): # Single Tone
	winsound.Beep(A, ST_Tone_Duration)
	PTT(False)
	return True

def DTMF(str): # Dual Tone Multi Frequency
	PTT(False)
	return True

while True:
	sent = False
	print("Command or Unit ID:")
	unit = input()
	if unit.lower() != 'help':
		print(f"[Paging][ID: {unit}]")
	


	# if unit == '{UNIT ID NUMBER}':
	# 	PTT(True)
	# 	sent = QC2(950, 425) # First number = Tone A. Second number = Tone B.
	# 	print('[Page Sent][Unit {UNIT ID NUMBER}][{UNIT NAME}]')

	if unit == '1':
		PTT(True)
		sent = QC2(950, 425)
		print('[Page Sent][Unit 1][Handheld 1]')
	elif unit == '2':
		PTT(True)
		sent = QC2(350, 485)
		print('[Page Sent][Unit 2][Handheld 2]')
	elif unit == '3':
		PTT(True)
		sent = QC2(800, 450)
		print('[Page Sent][Unit 3][Handheld 3]')
	elif unit == '4':
		PTT(True)
		sent = QC2(650, 375)
		print('[Page Sent][Unit 4][Handheld 4]')
	elif unit == '8':
		PTT(True)
		sent = QC2(750, 525)
		print('[Page Sent][Unit 8][Base 1]')
	elif unit == '9':
		PTT(True)
		sent = QC2(700, 450)
		print('[Page Sent][Unit 9][Base 2]')
	elif unit == '10':
		PTT(True)
		sent = QC2(725, 650)
		print('[Page Sent][Unit 10][Anytone 878]')
	elif unit == '91':
		PTT(True)
		sent = QC2(350, 490)
		print('[Page Sent][Siren Alert]')
	elif unit == '92':
		PTT(True)
		sent = QC2(350, 555)
		print('[Page Sent][Siren Attack]')
	elif unit == '93':
		sent = QC2(350, 625)
		print('[Page Sent][Siren Test/Cancel]')
	elif unit.lower() == 'help':
		print(help_msg)
	else:
		print("Invalid Unit ID")
	print("-----------------------------------")