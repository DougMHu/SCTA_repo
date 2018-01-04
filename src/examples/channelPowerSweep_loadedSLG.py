import SCTA_context
from SCTA.System import Transponder
from SCTA.Instrumentation import FSW, SLG
from SCTA.DataLogging import DataLogger
import pandas as pd

from collections import deque
import time
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

######################
# Test Spec Parameters
######################
output_filename = "data/slg-loading-dswm/channelPowerSweep_trial2"
adjacent_low_start=954e6
adjacent_low_end=2077e6
adjacent_high_start=994e6
adjacent_high_end=2117e6
lbandStart=974e6
lbandEnd=2097e6
step=51e6
mods=3



spec = pd.read_csv('C:\\Users\\labuser\\Documents\\SCTA_repo\\src\\SCTA\\Specs\\raw\\SPS1025.csv')

################################
# Initialize Equipment Libraries
################################
# IP addresses and port numbers
FSW_IP="192.168.10.10"
SLG1_IP="192.168.10.1"
SLG2_IP="192.168.10.2"
SLG3_IP="192.168.10.3"
SLG_port=5025
# Initialize Equipment

fsw = FSW(type="IP", port=FSW_IP, window="Spectrum")
slg1= SLG(ip=SLG1_IP, port=SLG_port, numMods=1)
slg2= SLG(ip=SLG2_IP, port=SLG_port, numMods=1)
slg3= SLG(ip=SLG3_IP, port=SLG_port, numMods=1)

slg=[slg1, slg2, slg3]

# Create a CSV file to store power over frequency
output_header = ['Desired Frequency (Hz)', 'Measured Power (dB)']
csvfile = DataLogger(filename=output_filename, format='csv', csv_header=output_header)
csvfile1 = DataLogger(filename=output_filename+"updatedPower", format='csv', csv_header=output_header)

# Initialize Transponders
txp1 = Transponder(mode=4, freq=954e6, symb=5e6, roll=20, scramb=0, pilots=True)
txp2 = Transponder(mode=12, freq=974e6, symb=20e6, roll=20, scramb=0, pilots=True)

#initialize SLG Setup

slg1.loadConfigFile("DSWM\SLG1_DSWM_US_23CH_2B_20MS.cfg")
slg2.loadConfigFile("DSWM\SLG2_DSWM_US_23CH_2B_20MS.cfg")
slg3.loadConfigFile("DSWM\SLG3_DSWM_US_23CH_2B_20MS.cfg")
##############
# Begin Script
##############

lower = list(range(int(adjacent_low_start), int(adjacent_low_end)+1, int(step)))	# +1 so list includes the stop frequency
upper = list(range(int(adjacent_high_start), int(adjacent_high_end)+1, int(step)))	# +1 so list includes the stop frequency
victim= list(range(int(lbandStart), int(lbandEnd)+1, int(step)))

fsw.setTransponder(txp1)
for k in lower+upper+victim:
	if k in victim:
		fsw.setTransponder(txp2)
	if k >1815e6:
		k=k+1e6
		fsw.setFrequency(k)
	else:
		fsw.setFrequency(k)

	fsw_power = fsw.getSpectrumChannelPower()
		
	# Log measurements
	sample = [k, fsw_power] 
	csvfile.push(sample)

results=pd.read_csv(output_filename +".csv")
adjusted=[]

for k in lower+upper+victim:
	if k >1815e6:
		k=k+1e6

	#Getting measured power based on frequency
	sample = results[results["Desired Frequency (Hz)"]==k]
	measured_power = sample["Measured Power (dB)"].item()
	#Getting loss compensation based on frequency
	sample_loss=cal[cal["Freq (Hz)"]==int(k)]
	compensation=sample_loss["Loss"].item()
	#Getting spec value to compare the measured power plus the loss compensation
	logger.info("k = %r" % k)
	value=spec[spec["Freq (Hz)"]==int(k)]
	logger.info("spec is %r" % spec)
	logger.info("value is %r" % value)
	desired_value=value["Scen 2 Power (dBm)"].item()
	logger.info("desired value is: %r" % desired_value)
	#Compensating measured value with calibration
	actual_value=measured_power+compensation
	logger.info("actual value is %r" % actual_value)
	#comparing measured compensated value with spec
	adjust_value=actual_value-desired_value
	adjusted.append(adjust_value)
results["adjusted value (dB)"]=adjusted

lines=len(cal.index)
logger.info("cal length is: %r" % lines)
slgPower=[]
for x in (range(0, lines)):
	gen=spec["SLG"][x]
	modNumber=spec["mod"][x]
	logger.info("gen is %r" % gen)
	power=slg[gen-1].getPower(modNumber)
	slgPower.append(power)
results["SLG output Power"]=slgPower
results["SLG new Power"]= results["SLG output Power"]-results["adjusted value (dB)"]
results.to_csv("data/slg-loading-dswm/newSLGSettings.csv")

newvalues=pd.read_csv("data/slg-loading-dswm/newSLGSettings.csv")
for y in (range(0, lines)):
	gen=spec["SLG"][y]
	modNumber=spec["mod"][y]
	power=round(newvalues["SLG new Power"][y], 1)
	if power<-45:
		power=-45
	slg[gen-1].setPower(power, modNumber)

fsw.setTransponder(txp1)
for k in lower+upper+victim:
	if k in victim:
		fsw.setTransponder(txp2)
	if k >1815e6:
		k=k+1e6
		fsw.setFrequency(k)
	else:
		fsw.setFrequency(k)

	fsw_power = fsw.getSpectrumChannelPower()
		
	# Log measurements
	sample = [k, fsw_power] 
	csvfile1.push(sample)