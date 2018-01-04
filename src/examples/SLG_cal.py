import SCTA_context
from SCTA.System import Transponder
from SCTA.Instrumentation import BTC, SLG, FSW
from SCTA.DataLogging import DataLogger
from SCTA.utils.fileparse import csv2dict, dict2csv, importCSV
import pandas as pd

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calibrateDDSS(scenario=1):



	# IP addresses and port numbers
	FSW_IP="192.168.88.243"
	SLG1_IP="192.168.88.2"
	SLG2_IP="192.168.88.3"
	SLG3_IP="192.168.88.4"
	SLG_port=5025
	#BTC_IP="192.168.10.11"
	# Initialize Equipment

	fsw = FSW(type="IP", port=FSW_IP, window="Spectrum")
	slg1= SLG(ip=SLG1_IP, port=SLG_port, numMods=1)
	slg2= SLG(ip=SLG2_IP, port=SLG_port, numMods=1)
	slg3= SLG(ip=SLG3_IP, port=SLG_port, numMods=1)
	#btc = BTC(type="IP", port=BTC_IP)

	# Initialize Transponders
	sideband = Transponder(mode=4, freq=954e6, symb=5e6, roll=20, scramb=0, pilots=True)
	victim = Transponder(mode=12, freq=974e6, symb=20e6, roll=20, scramb=0, pilots=True)

	#initialize SLG Setup


	slg1.loadConfigFile("DSWM\SLG1_DSWM_US_23CH_2B_20MS.cfg")
	slg2.loadConfigFile("DSWM\SLG2_DSWM_US_23CH_2B_20MS.cfg")
	slg3.loadConfigFile("DSWM\SLG3_DSWM_US_23CH_2B_20MS.cfg")

	slg=[slg1, slg2, slg3]
	mod1=list(range(1,10))
	mod2=list(range(1,7))
	mod3=list(range(1,9))
	mods=mod1+mod2+mod3
	powers=[]

	#read spec DSWM23_Scenario 2
	spec = pd.read_csv('C:\\Users\\labuser\\Documents\\SCTA_repo\\src\\SCTA\\Specs\\raw\\DSWM23_Scen2.csv')

	victimFreq = spec[" Primary Tr CF"]
	victim_power=spec["Primary Power"]

	upperFreq=spec[" Upper CF"]
	upperPower=spec[" Upper Power"]

	lowerFreq=spec[" Lower CF"]
	lowerPower=spec[" Lower Power"]

	currentVictimPower=[]
	currentVictimPower.append("dBm")
	currentUpperPower=[]
	currentUpperPower.append("dBm")
	currentLowerPower=[]
	currentLowerPower.append("dBm")

	#configure FSW for channel power mode
	fsw.setTransponder(victim)

	flag=False
	while flag==False:
		#measure channel power across all frequencies and SLG's

		for k in range(1, len(victimFreq)):
			logger.info("%r" % victimFreq)
			logger.info("victimFreq length is: %f" % len(victimFreq))
			freq=int(victimFreq[k])*1e6
			
			fsw.setFrequency(freq)
			logger.info("Frequency is: %r" % freq)
			fsw_power = fsw.getSpectrumChannelPower()
			currentVictimPower.append(round(fsw_power, 2))
		spec['Current Victim Power']=currentVictimPower

		for k in range(1, len(upperFreq)):
			fsw.setTransponder(sideband)
			freq=int(upperFreq[k])*1e6
			
			fsw.setFrequency(freq)

			fsw_power = fsw.getSpectrumChannelPower()
			currentUpperPower.append(round(fsw_power, 2))
		spec['currentUpperPower']=currentUpperPower


		for k in range(1, len(lowerFreq)):
			fsw.setTransponder(sideband)
			freq=int(lowerFreq[k])*1e6
			
			fsw.setFrequency(freq)

			fsw_power = fsw.getSpectrumChannelPower()
			currentLowerPower.append(round(fsw_power, 2))
		spec['currentLowerPower']=currentLowerPower
		print ("table is: %r" % spec)

		#calculate deltas between wanted and measured
		compensation_victim=[]
		compensation_victim.append("dBm")
		for v in range(1, len(victim_power)):
			adjust=int(currentVictimPower[v])-int(victim_power[v])
			compensation_victim.append(adjust)
			spec["compensation_victim"]=compensation_victim
			victim_check=[x <0.2 for x in compensation_victim]

		compensation_upper=[]
		compensation_upper.append("dBm")
		for u in range(1, len(upperPower)):
			adjust=int(currentUpperPower[u])-int(upperPower[u])
			compensation_upper.append(adjust)
			spec["compensation_upper"]=compensation_upper
			upper_check=[x <0.2 for x in compensation_upper]

		compensation_lower=[]
		compensation_lower.append("dBm")
		for l in range(1, len(lowerPower)):
			adjust=int(currentLowerPower[l])-int(lowerPower[l])
			compensation_lower.append(l)
			spec["compensation_lower"]=compensation_lower
			lower_check=[x <0.2 for x in compensation_lower]
		flag=all(lower_check+upper_check+victim_check)


	#current SLG power
		slgVictim=spec[" SLG Primary"]
		slgUpper=spec[" SLG Upper"]
		slgLower=spec[" SLG Lower"]

		modVictim=spec[" Output Primary"]
		current_SLGVictimPower=[]
		current_SLGVictimPower.append("dBm")
		for i in range(1, len(slgVictim)):
			port=modVictim[i]
			slgIndex=slgVictim[i]
			victim=slg[int(slgIndex)].getPower(int(port))
			current_SLGVictimPower.append(victim)
			spec["current_SLGVictimPower"]=current_SLGVictimPower

		modUpper=spec[" Output Upper"]
		current_SLGUpperPower=[]
		current_SLGUpperPower.append("dBm")
		for i in range(len(slgUpper)):
			port=modUpper[int(mod)]
			upper=slg[int(slgIndex)].getPower(int(port))
			current_SLGUpperPower.append(upper)
			spec["current_SLGUpperPower"]=current_SLGUpperPower

		modLower=spec[" Output Lower"]
		current_SLGLowerPower=[]
		current_SLGLowerPower.append("dBm")
		for slgIndex, mod in zip(slgLower, modUpper):
			port=modLower[int(mod)]
			lower=slg[int(slgIndex)].getPower(int(port))
			current_SLGLowerPower.append(lower)
			spec["current_SLGLowerPower"]=current_SLGLowerPower

		#calculate new SLG Powers and set them

		newSLGVictimPower=[]
		newSLGVictimPower.append("dBm")
		for i in range(1, len(current_SLGVictimPower)):
			newVictimPower=int(current_SLGVictimPower[i])-int(compensation_victim[i])
			slg[int(slgVictim[i])].setPower(newVictimPower, int(modVictim[i]))
			newSLGVictimPower.append(newVictimPower)
			spec["newSLGVictimPower"]=newSLGVictimPower

		newSLGUpperPower=[]
		newSLGUpperPower.append("dBm")
		for i in range(1, len(current_SLGUpperPower)):
			newUpperPower=int(current_SLGUpperPower[i])-int(compensation_upper[i])
			slg[int(slgUpper[i])].setPower(newUpperPower, int(modUpper[i]))
			newSLGUpperPower.append(newUpperPower)
			spec["newSLGUpperPower"]=newSLGUpperPower

		newSLGLowerPower=[]
		newSLGLowerPower.append("dBm")
		for i in range(1, len(current_SLGLowerPower)):
			newLowerPower=int(current_SLGLowerPower[i])-int(compensation_lower[i])
			slg[int(slgLower[i])].setPower(newLowerPower, int(modLower[i]))
			newSLGLowerPower.append(newLowerPower)
			spec["newSLGLowerPower"]=newSLGLowerPower
		spec.to_csv("..//src/SCTA/Specs//raw//DSWM23_Scen2_updated.csv", sep='\t')
		debug.info(print spec)


if __name__=="__main__":
	calibrateDDSS()