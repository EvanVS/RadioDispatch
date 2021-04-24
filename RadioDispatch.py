import winsound, csv, time, serial
import numpy as np
import sounddevice as sd

# https://github.com/EvanVS/RadioDispatch

# ----------< Configuration >----------

QC2_Tone_A_Duration = 1000 # ms (Default: 1000ms)
QC2_Tone_B_Duration = 3000 # ms (Default: 3000ms)

ST_Tone_Duration = 3000 # ms (Default: 3000ms)

PTT_COM_Port = 'VOX' # Set as 'VOX' for no PTT control. Set as 'COM#' with # being the COM Port number.
PTT_COM_Pin = 'RTS' # RTS or DTR pin for PTT Control

# ----------< Configuration >----------

low_freq = [697, 770, 852, 941]
high_freq = [1209, 1336, 1477, 1633]

# "digit": [low_freq, high_freq]
digits_tones = \
{ "1": [0, 0],
  "2": [0, 1],
  "3": [0, 2],
  "A": [0, 3],
  "4": [1, 0],
  "5": [1, 1],
  "6": [1, 2],
  "B": [1, 3],
  "7": [2, 0],
  "8": [2, 1],
  "9": [2, 2],
  "C": [2, 3],
  "*": [3, 0],
  "0": [3, 1],
  "#": [3, 2],
  "D": [3, 3]
}

valid_digits = "0123456789*#ABCD"

duration = 0.5
volume = 0.5
fs = 44100 # sampling rate

print('\n-----------------------------------')
print('KJ7BRE Communications Paging System')
print('Version: 0.92     github.com/EvanVS')
print('-----------------------------------\n')


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
	PTT(True)
	winsound.Beep(A, QC2_Tone_A_Duration)
	winsound.Beep(B, QC2_Tone_B_Duration)
	PTT(False)
	return True

def ST(A): # Single Tone
	PTT(True)
	winsound.Beep(A, ST_Tone_Duration)
	PTT(False)
	return True

def DTMF(x): # Dual Tone Multi Frequency
	x = str(x)
	digits = list(x.replace(" ",""))
	if(all(d in valid_digits for d in digits)):
		PTT(True)
		for i in digits:
			f1 = low_freq[digits_tones[i][0]]
			f2 = high_freq[digits_tones[i][1]]
			s1 = np.sin(2*np.pi*np.arange(fs*duration)*f1/fs)
			s2 = np.sin(2*np.pi*np.arange(fs*duration)*f2/fs)

			sd.play(s1*volume + s2*volume)
			time.sleep(.5)
		PTT(False)
		return True
	else:
		print("Invalid DTMF String")
		return False

def UNIT(x):
	global unit_id
	global unit_name
	global unit_signal_type
	global unit_tone_a
	global unit_tone_b
	if user_input.lower() != 'help':
		with open('units.csv', 'r') as csv_file:
			units = csv.reader(csv_file)
			for unit in units:
				if unit[0] == x:
					unit_id = unit[0]
					unit_name = unit[1]
					unit_signal_type = unit[2]
					unit_tone_a = unit[3]
					unit_tone_a = int(unit_tone_a)
					if unit_signal_type.upper() == 'QC2':
						unit_tone_b = unit[4]
						unit_tone_b = int(unit_tone_b)
					return True
			return False
	return False

def HELP():
	print('              Unit List')
	print("-----------------------------------")
	with open('units.csv', 'r') as csv_file:
		units = csv.reader(csv_file)
		for unit in units:
			unit_id = unit[0]
			unit_name = unit[1]
			unit_signal_type = unit[2]
			unit_tone_a = unit[3]
			unit_tone_b = unit[4]
			print(f'[ID: {unit_id}][Name: {unit_name}]')


while True:
	sent = False
	print("Command or Unit ID:")
	user_input = input()
	valid_id = UNIT(user_input)

	if valid_id == False:
		if user_input.lower() == 'help':
			HELP()
		else:
			print("Invalid Unit ID")
	if valid_id == True:
		print(f"[Paging][ID: {unit_id}][{unit_name}]")
		if unit_signal_type.upper() == 'QC2':
			sent = QC2(unit_tone_a, unit_tone_b)
			print(f'[Page Sent][Unit {unit_id}][{unit_name}]')
		if unit_signal_type.upper() == 'ST':
			sent = ST(unit_tone_a)
			print(f'[Page Sent][Unit {unit_id}][{unit_name}]')
		if unit_signal_type.upper() == 'DTMF':
			sent = DTMF(unit_tone_a)
			print(f'[Page Sent][Unit {unit_id}][{unit_name}]')
		else:
			print("Invalid Unit Signaling Type")
	print("-----------------------------------")
