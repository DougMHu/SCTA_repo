from . import Modulator
from .SNMPComm import SNMPComm
import logging
import time, math
from ..System import Mode, Transponder

logger = logging.getLogger(__name__)

class VTM(Modulator):
	constellation={
	43: ("QPSK", "1/2"),
	44: ("QPSK", "3/5"),
	45: ("QPSK", "2/3"),
	46: ("QPSK", "3/4"),
	47: ("QPSK", "4/5"),
	48: ("QPSK", "5/6"),
	49:	("QPSK", "8/9"),
	50:	("QPSK", "9/10"),
	51:	("8PSK", "3/5"),
	52:	("8PSK", "2/3"),
	53:	("8PSK", "3/4"),
	54:	("8PSK", "5/6"),
	55:	("8PSK", "8/9"),
	56:	("8PSK", "9/10")
	}

	reverse_const={}
	for key in constellation:
		value=constellation[key]
		reverse_const[value]=key

	dataSource={
	3: ("ETHERNET INPUT A"),
	11: ("PN23 INSERT"),
	13: ("PN23 INVERT"),
	14: ("RAMP GENERATOR"),
	15: ("PN15"),
	16: ("PN23 BONDED"),
	17: ("PN23 BONDED INVERT")
	}

	reverse_dataSource={}
	for key in dataSource:
		value=dataSource[key]
		reverse_dataSource[value]=key


	def __init__(self, id="VTM", ip="192.168.10.1", port=161, type="int", numMods=1):
		"""
		Creates an VTM object, which starts a connection for reading and writing commands to the VTM.
	

		Input:
			id: string
			type: string interface type
			port: string interface address

		Output:
			VTM object

		~~~ Valid ranges ~~~
		type:        ['GPIB', 'IP']
		port:        ['28' or '192.10.10.10']
		cnr:         [0, 20] dB
		"""

		self.comm = SNMPComm(ip=ip,type=type, port=port)
		self.numMods=numMods
		self.type=type

		#super ().__init__(id=id)
		self.config()
		

	def __del__(self):
		self.close()

	def close(self):
		"""
		Closes the connection with the VTM
		NOTE: YOU MUST CALL THIS AFTER YOU ARE FINISHED WITH THE VTM

		Input:
			None

		Output:
			None
		"""
		#self.comm.instrument.close()

	def mode(self, mode="VTM"):
		"""
		Configures VTM to different modes:
		VTM: set mode="VTM"
		VTM:Lab set mode="LAB"
		CCM: set mode="CCM"

		"""


	def config(self):
		"""
		Configures VTM for operation. Only called by VTM __init__
		WARNING: NOT A USER FUNCTION

		Input:
			None

		Output:
			None
		"""
		OID=".1.3.6.1.4.1.9633.24.1.3.1.1.8.0"		# sets the number of carries on the VTM.
		value=(" -val:%d" % self.numMods)
		code=OID+value
		self.comm.write(code)

	def setTransponder(self, txpdr, modNumber):
		"""
		Sets the transponder settings to the SLG from the Modulator class.
		"""
		#self.setInputSource("PN", modNumber)		#Input set to Load for testing of SLG class. Default should be seto to PN23 for mods 1-16 and LOAD for 17-32 since the SLG is not able to set data on mods higher than 16. 
		# self.setMode(txpdr.getMode(), modNumber)
		bcstd = txpdr.getBroadcastStandard()
		const = txpdr.getConstellation()
		code_rate = txpdr.getCodeRate()
		self.setBroadcastStandard(bcstd, modNumber)
		self.setConstellationCodeRate(const, code_rate, modNumber)
		# set this transponder's parameters to corresponding input parameters
		self.setFrequency(txpdr.getFrequency(), modNumber)
		self.setSymbolRate(txpdr.getSymbolRate(), modNumber)
		self.setAlpha(txpdr.getAlpha(), modNumber)
		self.setPilots(txpdr.getPilots(), modNumber)
		self.setScramblingCode(txpdr.getScramblingCode(), modNumber)

	def getTransponder(self, modNumber):
		bcstd=self.getBroadcastStandard(modNumber)
		modCod=self.getConstellationCodeRate(modNumber)
		mod=modCod[0]
		fec=modCod[1]
		freq=self.getFrequency(modNumber)
		symRate=self.getSymbolRate(modNumber)
		alpha=self.getAlpha(modNumber)
		pilots=self.getPilots(modNumber)
		scrambling=self.getScramblingCode(modNumber)
		txpdr=Transponder(bcstd=bcstd, mod=mod, fec=fec, freq=freq, symb=symRate, roll=alpha, scramb=scrambling, pilots=pilots)
		return txpdr


	def setBroadcastStandard(self, bcstd, modNumber):
		if bcstd!= "DVB-S2":
			raise AttributeError("Only DVB-S2 not supported")
		else:
			bcstd="DVB-S2"
		logger.info("Set broadcast standard: %s" % bcstd)
		logger.info("Only DVB-S2 supported on VTM")
	def getBroadcastStandard(self, modNumber):
		bcstd="DVB-S2"
		logger.info("Got broadcast standard: %s" % bcstd)
		return bcstd

	def setPower(self, power, modNumber):
		"""
		Sets VTM RF power

		Input:
			power: float power in dBm

		Output:
			None
		"""
		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.6." 
		value=(" -val:%d" % (power*10))
		code=OID+str(modNumber)+str(value)
		self.comm.write(code)

	def getPower(self, modNumber):
		"""
		Gets VTM RF power

		Input:
			None

		Output:
			float power in dBm
		"""
		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.6." 
		code=OID+str(modNumber)
		power=(self.comm.query(code))
		power=float(power)/10
		logger.info("Got power: %f dBm" % power)
		return power

	def setFrequency(self, freq, modNumber):

		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.5." 
		value=(" -val:%d" % freq)
		code=OID+str(modNumber)+str(value)
		self.comm.write(code)
		logger.info("Set frequency: %f MHz" % (freq/1e6))
	
	def getFrequency(self, modNumber):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.5." 
		code=OID+str(modNumber)
		freq=float(self.comm.query(code))
		logger.info("Got frequency: %f MHz" % (freq/1e6))
		return freq

	def setSymbolRate(self, rate, modNumber):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.8.1" 
		value=(" -val:%d" % rate)
		code=OID+str(value)
		self.comm.write(code)
		logger.info("Code sent is: %r" % code)
		logger.info("Set symbol rate: %f MBaud" % (rate/1e6))

	def getSymbolRate(self, modNumber):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.8.1" 
		code=OID
		symb=int(self.comm.query(code))
		logger.info("Got symbol rate: %f MBaud" % (float(symb)/1e6))
		return (symb)

	def setPilots(self, pilots, modNumber):
		if pilots is True:
			pil = 2
		else:
			pil = 1	
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.5.1"
		code=(OID+" -val:%d"% pil)
		self.comm.write(code)
		# super().setPilots(pilots)
		logger.info("Set pilot symbols enabled state: %r" % pilots)

	def getPilots(self, modNumber):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.5.1"
		code=(OID)
		pilots=int(self.comm.query(code))
		logger.info("pilots status returned: %r" % pilots)
		if pilots == 1:
			pilots = False
		if pilots == 2:
			pilots = True
		# super().setPilots(pilots)
		# pilots = super().getPilots()
		logger.info("Got pilot symbols enabled state: %r" % pilots)
		return pilots

	def setCW(self, cw, modNumber):
		"""
		Sets Carrier Wave Enabled state

		Input:
			cw: True or False

		Output:
			None
		"""
		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.4.1"
		if cw==False:
			value=2
		if cw==True:
			value=1
		code=(OID+" -val:%d" % value)
		self.comm.write(code)
		logger.info("Set Carrier Wave Enabled state: %r" % cw)

	def getCW(self, modNumber):
		"""
		Gets Carrier Wave Enabled state

		Input:
			None

		Output:
			True or False
		"""
		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.4.1"
		state=self.comm.query(OID)
		if state=="1":
			cw=True
		if state=="2":
			cw=False
		logger.info("Got Carrier Wave Enabled state: %r" % cw)
		return cw
	

	def setAlpha(self, alpha, modNumber):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.7.1" 
		value=(" -val:%d"% alpha)
		code=OID+value
		self.comm.write(code)
		logger.info("Set roll-off factor: %f%%" % alpha)

	def getAlpha(self, modNumber):		
		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.7.1"
		code=OID
		alpha=self.comm.query(code)
		alpha=float(alpha)
		# super().setAlpha(alpha)
		# alpha = super().getAlpha()
		logger.info("Got roll-off factor: %f%%" % alpha)
		return alpha


	def setScramblingCode(self, scramb, modNumber):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.10."
		value=(" -val:%d" % scramb)
		code=OID+str(modNumber)+str(value)
		self.comm.write(code)
	
	def getScramblingCode(self, modNumber):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.10."
		code=(OID+str(modNumber))
		scramb=int(self.comm.query(code))
		# super().setScramblingCode(scramb)
		# scramb = super().getScramblingCode()
		logger.info("Got scrambling code: %d" % scramb)
		return scramb


	def rfEnable(self, rf):
		if (rf==True):
			rf=2
		if (rf==False):
			rf=1
		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.3.1"
		value=(" -val:%d -tp:%s" % (rf, self.type))
		code=OID+value
		self.comm.write(code)
		logger.info("set rf to: %d" % rf)

	def getrfEnable(self):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.4.1.3.1"
		rf=int(self.comm.query(OID))
		logger.info("the rfEnable get state is: %d" % rf)
		if (rf==2):
			return True
		if (rf==1):
			return False
		
	def getMode(self, modNumber):
		"""
		Gets the current mode

		Input:
			None

		Output:
			Either an integer AMC Mode Number or a custom Mode Object
		"""
		bcstd = self.getBroadcastStandard(modNumber)
		(mod, fec) = self.getConstellationCodeRate(modNumber)
		mode = Mode(bcstd=bcstd, mod=mod, fec=fec)
		num = Mode.toAMC(mode)
		if num is None:
			return mode
		else:
			return num

	def setMode(self, mode, modNumber):
		"""
		Sets the current mode

		Input:
			Either an integer AMC Mode Number or a custom Mode Object

		Output:
			None
		"""
		# If AMC mode number is specified, get the corresponding mode object
		if type(mode) is int:
			num = mode
			mode = Mode.fromAMC(num)
		self.setBroadcastStandard(mode.getBroadcastStandard(), modNumber)
		self.setConstellationCodeRate(mode.getConstellation(), mode.getCodeRate(), modNumber)

	def getConstellationCodeRate(self, modNumber):
		"""
		Returns the constellation and code rate as an ordered pair.

		Input:
			None

		Output:
			ordered pair: (string constellation, string code rate)
		"""
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.3.1"
		if self.getBroadcastStandard(modNumber) == "DVB-S2":
			modcod=int(self.comm.query(OID))
			logger.debug("the modcod is: %d" % modcod)
			mod=self.constellation[modcod][0]
			logger.debug("the DVB-S2 mod is: %s" % mod)
			fec=self.constellation[modcod][1]
			logger.debug("The DVB-S2 fec is: %s" % fec)
			return (mod, fec)

		if self.getBroadcastStandard(modNumber)=="DVBS":
			print ("DVBS stanard not supported in VTM!!!!")
		if self.getBroadcastStandard(modNumber)=="DIRECTV":
			print ("DIRECTV stanard not supported in VTM!!!!")
		

	def setConstellationCodeRate(self, mod, fec, modNumber):
		"""
		Sets the constellation and code rate simultaneously.
		If the constellation and code rate combination is invalid, it raises an exception.

		Input:
			string mod: constellation
			string fec: code rate
			Valid combinations:
			 (x,y)
					 
		Output:
			None
		"""
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.3.1"
		if self.getBroadcastStandard(modNumber) == "DVB-S2":
			######## REPLACE THIS WITH YOUR OWN CODE ########        
			value=(mod, fec)
			logger.info("mod is %r" % mod)
			logger.info("fec is %r" % fec)
			if value in self.reverse_const:
				index=self.reverse_const[value]
				logger.info("setting index to: %r" % index)
				code=(" -val:%d" % index)
				self.comm.write(OID+code)
			else:
				print("Combination not available for DVB-S2")
		if self.getBroadcastStandard(modNumber)=="DVBS":
			raise AttributeError("'VTM' does not support DVBS standard")
		if self.getBroadcastStandard(modNumber)=="DIRECTV":
			raise AttributeError("'VTM' does not support DIRECTV standard")

	def setDataSource(self, source):

		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.2.1"
		if source in self.reverse_dataSource:
				index=self.reverse_dataSource[source]
				logger.info("setting index to: %r" % index)
				code=(" -val:%d" % index)
				self.comm.write(OID+code)

	def getDataSource(self):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.2.1" 
		code=OID
		source=int(self.comm.query(code))
		index=self.dataSource[source]
		return index



	def setDataPID(self, PID):
		if PID>8190:
			logger.info("PID set is: %r" % PID)
			raise AttributeError(" Data PID must be set between 0 - 8190")
		else:
			OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.17.1"
			value=(" -val:%d" % PID)
			code=OID+value
			logger.info("code sent is %r" % code)
			self.comm.write(code)

	def getDataPID(self):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.17.1"
		code=OID
		data=int(self.comm.query(code))
		logger.info("query sent is: %r" % code)
		return data

	def setMarkerPID(self, PID):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.18.1"
		if int(PID)>8190:
			logger.info("Marker PID is: %r" % PID)
			raise AttributeError(" Marker PID must be set between 0 - 8190")
		value=(" -val:%s" % PID)
		code=OID+value
		self.comm.write(code)

	def getMarkerPID(self):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.18.1"
		code=OID
		marker=int(self.comm.query(code))
		return marker


	def setChunkSize(self, size):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.20.1"
		if 10>int(size)>250:
			logger.info("size is: %r" % size)
			raise AttributeError("Chunk size needs to be between 10 -250")
		value=(" -val:%s" % size)
		code=OID+value
		self.comm.write(code)

	def getChunkSize(self):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.20.1"
		code=OID
		chunk=int(self.comm.query(code))
		return chunk

	def setBondedRate(self, rate):
		if int(rate)>300799982071:
			raise AttributeError(" Rate must be set between 0 - 300799.982071 MBit/s")
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.19.1"
		value=(" -val:%s" % rate)
		code=OID+value
		self.comm.write(code)


	def getBondedRate(self):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.19.1"
		code=OID
		rate=int(self.comm.query(code))
		return rate

	def setSkew(self, skew, carrier):
		if int(skew)>221040:
			raise AttributeError("Skew must be between 0 and 221040 Symbols")
		OID=".1.3.6.1.4.1.9633.24.1.3.1.1.19.1.2."
		value=(" -val:%s" % skew)
		code=OID+str(carrier)+ value
		self.comm.write(code)

	def getSkew(self, carrier):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.1.19.1.2."
		code=OID+str(carrier)
		skew=int(self.comm.query(code))
		return skew

	def setPhaseNoise(self, freq, noise):
		if freq==17000000:
			channel=8
		else:
			channel=int(math.log(freq, 10))
		OID=".1.3.6.1.4.1.9633.24.1.3.1.1.21.1.2."
		value=(" -val:%s" % (noise*10))
		code=OID+str(channel)+ value
		logger.info("string sent is: %r" % code)
		self.comm.write(code)

	def getPhaseNoise(self, freq):
		if freq==17000000:
			channel=8
		else:
			channel=int(math.log(freq, 10))
		OID=".1.3.6.1.4.1.9633.24.1.3.1.1.21.1.2."
		code=OID+str(channel)
		logger.info("string sent is: %r" % code)
		noise=float(self.comm.query(code))/10
		return noise

	def enablePhaseNoise(self, enabled):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.1.20.0"
		if enabled==True:
			value=" -val:2"
		if enabled==False:
			value=" -val:1"
		code=OID+value

	def setVTMMode(self, mode):
		logger.info("input mode is: %r" % mode)
		OID=".1.3.6.1.4.1.9633.24.1.3.1.1.1.0"
		if mode=="VTM":
			mode=3
		if mode=="LAB":
			mode=4
		if mode=="CCM":
			mode=1
		if mode=="ACM":
			mode=2
		value=(" -val:%d -t:60" % mode)
		code=OID+value
		logger.info("code sent is: %r" % code)
		self.comm.write(code)

	def getVTMMode(self):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.1.1.0"
		mode=int(self.comm.query(OID))
		logger.info("getVTMmode is: %r" % mode)
		if mode==1:
			return "CCM"
		if mode==2:
			return "ACM"
		if mode==3:
			return "VTM"
		if mode==4:
			return "LAB"


	@property
	def setConstellation(self):
		   raise AttributeError( "'VTM' object has no method 'setConstellation'" )

	@property
	def getConstellation(self):
		   raise AttributeError( "'VTM' object has no method 'getConstellation'" )

	@property
	def setCodeRate(self):
		   raise AttributeError( "'VTM' object has no method 'setCodeRate'" )

	@property
	def getCodeRate(self):
	   raise AttributeError( "'VTM' object has no method 'getCodeRate'" )    



'''	def setConstellation(self, modulation, modNumber):
		
		standard=self.getBroadcastStandard()
		if standard=="DVBS":
			standard==DVBS1
		if standard=="DVB-S2":
			standard==DVBS2
		if standard=="DIR":
			standard="DIR"

		if modulation=="QPSK":
			mod="S4"
		if modulation=="8PSK":
			mod="S8"
		self.comm.write("SOUR%d:IQC:%s:CONS %s" %(modNumber, standard, mod))
		# super().setConstellation(modulation)
		logger.info("Set constellation: %s" % modulation)


	def getConstellation(self, modNumber):
		standard=self.getBroadcastStandard()
		rate=mode.getCodeRate
		if (standard=="DVBS"):
			standard="DVBS1"
		if standard=="DIR":
			standard="DIR"
		if standard=="DVB-S2":
			modcod=int(self.comm.query("SOUR%d:IQC:DVBS2:TSL1:MODC?" % modNumber))
			modulation=self.constellation[modcod][0]
			return modulation
		modulation=self.comm.query("SOUR%d:IQC:%s:CONS?" %(modNumber, standard))
		if modulation=="S4":
			modulation="QPSK"
		if modulation=="S8":
			modulation="8PSK"
		# super().setConstellation(modulation)
		# modulation = super().getConstellation()
		logger.info("Got constellation: %s" % modulation)
		return modulation

	def setCodeRate(self, fec, modNumber):
		standard=self.getBroadcastStandard(modNumber)
		if standard=="DVB-S2":
			modcod=int(self.comm.query("SOUR%d:IQC:DVBS2:TSL1:MODC?" % modNumber))
			modulation=self.constellation[modcod][1]
			return modulation
		else:
			if (standard=="DVBS"):
				standard="DVBS1"
			code_rate=fec.replace("/","_")
			self.comm.write("SOUR%d:IQC:%s:RATE R%s" %(modNumber, standard, code_rate))
		# super().setCodeRate(fec)
		logger.info("Set code rate: %s" % fec)

	def getCodeRate(self, modNumber):
		standard=self.getBroadcastStandard()
		if standard=="DVB-S2":
			modcod=int(self.comm.query("SOUR%d:IQC:DVBS2:TSL1:MODC?" % modNumber))
			modulation=self.constellation[modcod][1]
			return modulation
		if (standard=="DVBS"):
			standard="DVBS1"		
		fec=self.comm.query("SOUR%d:IQC:%s:RATE?" %(modNumber, standard))
		fec=fec.replace("_","/")
		fec=fec.replace("R","")
		if fec=="9/1":
			return "9/10"
		# super().setCodeRate(fec)
		# fec = super().getCodeRate()
		logger.info("Got code rate: %s" % fec)
		return fec'''