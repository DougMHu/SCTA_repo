"""
Network Anaylyzer Demo

Authors:
	- Douglas Hu:	dmhu@directv.com
	- Luis Perez: 	jlperez@directv.com
Organization:	Space and Communications Department (DirecTV / AT&T)

Date Created:	2016-11-03T15:20:00
Last Updated:	2016-11-08T10:08:00
Version:		beta

Description: >
	This simple script uses the SCTA libraries to accomplish a network analyzer-like function.
	It uses an SFU and FSW to sweep across frequency and measure channel power. The path loss 
	between the SFU and FSW is calculated by the difference between the SFU output power and
	the FSW measured power.

Usage: |
	From command line:
		python NetAnDemo.py

	Supported Options:
		- 
"""
import argparse
import SCTA_context
from SCTA.Simulation import RunAsSimulation
from SCTA.System import Transponder
from SCTA.Instrumentation import SFU, FSW
from SCTA.DataLogging import DataLogger

# Create a CSV file to store insertion loss over frequency
csvfile = DataLogger(filename='NetAnDemo', format='csv', csv_header=['Frequency (MHz)', 'Loss (dB)'])

# Initialize test equipment: SFU and FSW
sfu = SFU(type='IP', port='192.168.2.11')
fsw = FSW(type='IP', port='192.168.10.76')

# Choose what AMC mode and input power to generate
amc_mode = 11
input_power = -50
txpdr = Transponder(mode=amc_mode)
sfu.setTransponder(txpdr)
sfu.setPower(input_power)
fsw.setTransponder(txpdr)

# Create a list of frequencies to loop over (in MHz)
start = 250
stop = 2150
step = 100
Lband = list(range(start, stop, step))
print('Lband = ', Lband)

# For each frequency, get a power measurement, calculate the insertion loss, and write results to the CSV file
for freq in Lband:
	sfu.setFrequency(freq*1e6)
	fsw.setFrequency(freq*1e6)
	sfu_pwr = sfu.getPower()
	fsw_pwr = fsw.getPower()
	loss = sfu_pwr - fsw_pwr
	print('freq = ', freq)
	print('sfu_pwr = ', sfu_pwr)
	print('fsw_pwr = ', fsw_pwr)
	print('loss = ', loss)
	sample = [freq, loss]
	csvfile.push(sample)
