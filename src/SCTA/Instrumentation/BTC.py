from . import Modulator
from . import Comm
import logging
import time
from .ResourceManagers import PyvisaResourceManager
from ..System import Mode, Transponder

logger = logging.getLogger(__name__)

class BTC(Modulator):
	constellation={
	1: ("QPSK", "1/4"),
	2: ("QPSK", "1/3"),
	3: ("QPSK", "2/5"),
	4: ("QPSK", "1/2"),
	5: ("QPSK", "3/5"),
	6: ("QPSK", "2/3"),
	7: ("QPSK", "3/4"),
	8: ("QPSK", "4/5"),
	9: ("QPSK", "5/6"),
	10:("QPSK", "8/9"),
	11:("QPSK", "9/10"),
	12:("8PSK", "3/5"),
	13:("8PSK", "2/3"),
	14:("8PSK", "3/4"),
	15:("8PSK", "5/6"),
	16:("8PSK", "8/9"),
	17:("8PSK", "9/10")


	}

	reverse_const={}
	for key in constellation:
		value=constellation[key]
		reverse_const[value]=key

	def __init__(self, id="BTC", type="GPIB", port="28", numMods=2):
		"""
		Creates an BTC object, which starts a connection for reading and writing commands to the BTC.
		With no inputs specified, it assumes the host computer's interface is GPIB at port 28.

		Input:
			id: string
			type: string interface type
			port: string interface address/ port

		Output:
			BTC object

		~~~ Valid ranges ~~~
		type:        ['GPIB', 'IP']
		port:        ['28' or '192.10.10.10']
		cnr:         [0, 20] dB
		"""

		self.comm = Comm(protocol=type, port=port)
		self.cnr=None
		self.numMods=numMods
		#super ().__init__(id=id)
		self.config()
		

	def __del__(self):
		self.close()

	def close(self):
		"""
		Closes the connection with the BTC
		NOTE: YOU MUST CALL THIS AFTER YOU ARE FINISHED WITH THE BTC

		Input:
			None

		Output:
			None
		"""
		self.comm.instrument.close(),

	def config(self):
		"""
		Configures BTC for operation. Only called by BTC __init__
		WARNING: NOT A USER FUNCTION

		Input:
			None

		Output:
			None
		"""
		self.comm.write("&GTR")
		logger.info("BTC device ID: %s" % (self.comm.query("*IDN?")) )
		self.comm.write("SYST:DISP:UPD ON")
		for mods in list(range(1, self.numMods+1)):
			self.comm.write("SOUR%d:DM:NOIS:AWGN:COUP ON"% mods) 				#Sets bandwidth coupling ON
			self.comm.write("SOUR%d:NOIS:AWGN ON" % mods)
			self.comm.write("SOUR%d:NOIS:COUP ON")							#Enables bandwith coupling ON in AWGN/Impulsive noise Tab
			self.comm.write("SOUR%d:DM:NOIS:AWGN:COUP ON" % mods)
			self.comm.write("SOUR%d:DM:NOISE:AWGN OFF" % mods)				#Disables AWGN in DTV tab
			self.comm.write("SOUR%d:NOIS:AWGN ON")							#Enables AWGN in AWGN/Impulsive noise tab
			self.comm.write("SOUR%d:DM:TYPE DTV" % mods)					#Configures BTC to DTV mode 
			self.comm.write("SOUR%d:IQC:DVBS2:SOUR TEST" % mods)			#Configures BTC for Test mode
			self.comm.write("SOUR%d:IQC:DVBS2:FECF NORM" % mods)			#Configures BTC FEC 
			self.comm.write("SOUR%d:IQC:DVBS2:TSP S187" % mods)			#Configures BTC for 187 byte packets for DVBS2
			self.comm.write("SOUR%d:IQC:DVBS2:PRBS:SEQ P23_1" % mods)	#Configures packets to have PRBS 2^(23-1)
			self.enableFading(False, mods)
			self.enableDistortion(False, mods)
			self.setNoiseState("OFF", mods)
			self.setPhaseNoise(False, mods)
		logger.info("BTC configuration complete")

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
		if bcstd=="DIRECTV":
			self.comm.write("SOUR%d:DM:TRAN:STAN DIR" % modNumber)					#Configures BTC to DTV mode 

		if bcstd=="DVB-S2":
			self.comm.write("SOUR%d:DM:TRAN:STAN DVS2" % modNumber)

		if bcstd=="DVBS":

			#Changes made by Chuck 10/31/2016
			#self.comm.write("SOUR:DM:TRAN:STAN "+str(bcstd))			#Configures BTC for DVBS2 standard
			#Wrong SCPI command
			self.comm.write("SOUR%d:DM:TRAN:STAN DVBS" % modNumber)
		# super().setBroadcastStandard(bcstd)
		logger.info("Set broadcast standard: %s" % bcstd)

	def getBroadcastStandard(self, modNumber):
		bcstd=self.comm.query("SOUR%d:DM:TRAN:STAN?" % modNumber)
		if bcstd=="DVS2":
			bcstd = "DVB-S2"
		if bcstd == "DIR":
			bcstd = "DIRECTV"
		if bcstd=="DVBS":
			bcstd="DVBS"
		# super().setBroadcastStandard(bcstd)
		# bcstd = super().getBroadcastStandard()
		logger.info("Got broadcast standard: %s" % bcstd)
		return bcstd

	def setPower(self, power, modNumber):
		"""
		Sets BTC RF power

		Input:
			power: float power in dBm

		Output:
			None
		"""
		self.comm.write("SOUR%d:POW:LEV:IMM:AMPL %f" % (modNumber, power) )
		self.power=power
		logger.info("Set power: %f dBm" % power)

	def getPower(self, modNumber):
		"""
		Gets BTC RF power

		Input:
			None

		Output:
			float power in dBm
		"""
		self.power = float(self.comm.query("SOUR%d:POW:LEV:IMM:AMPL?" % modNumber))
		logger.info("Got power: %f dBm" % self.power)
		return self.power

	def setFrequency(self, freq, modNumber):
		self.comm.write("SOUR%d:FREQ:ACT:CENT %s" % (modNumber, freq))
		# super().setFrequency(freq)
		logger.info("Set frequency: %f MHz" % (freq/1e6))
	
	def getFrequency(self, modNumber):
		freq=float(self.comm.query("SOUR%d:FREQ:ACT:CENT?" % modNumber))
		# super().setFrequency(freq)
		# freq = super().getFrequency()
		logger.info("Got frequency: %f MHz" % (freq/1e6))
		return freq

	def setSymbolRate(self, rate, modNumber):
		standard=self.getBroadcastStandard(modNumber)
		if standard=="DVBS":
			standard="DVBS1"
		if standard=="DVB-S2":
			standard="DVBS2"
		if standard=="DIR":
			standard="DIR"
		self.comm.write("SOUR%d:IQC:%s:SYMB:RATE %s" %(modNumber, standard, rate))
		# super().setSymbolRate(rate)
		logger.info("Set symbol rate: %f MBaud" % (rate/1e6))

	def getSymbolRate(self, modNumber):
		standard=self.getBroadcastStandard(modNumber)
		if standard=="DVBS":
			standard="DVBS1"
		if standard=="DVB-S2":
			standard="DVBS2"
		if standard=="DIR":
			standard="DIR"
		symb=float(self.comm.query("SOUR%d:IQC:%s:SYMB:RATE?" %(modNumber, standard)))
		# super().setSymbolRate(symb)
		# symb = super().getSymbolRate()
		logger.info("Got symbol rate: %f MBaud" % (symb/1e6))
		return symb

	def setNoiseLevel(self, cnr, modNumber):
		"""
		Sets Carrier-to-Noise Ratio

		Input:
			cnr: float cnr in dB

		Output:
			None
		"""
		self.comm.write("SOUR%d:NOIS:CN %f" % (modNumber, cnr))
		self.cnr=cnr
		logger.info("Set CNR: %f dB" % cnr)

	def getNoiseLevel(self, modNumber):
		"""
		Gets Carrier-to-Noise Ratio

		Input:
			None

		Output:
			float cnr in dB 
		"""
		self.cnr=float(self.comm.query("SOUR%d:NOIS:CN?" % modNumber))
		logger.info("Got CNR: %f dB" % self.cnr)
		return self.cnr

	def setNoiseState(self, state, modNumber):
		"""
		Sets Noise-Enabled state
		OFF: Sets Noise to OFF
		ADD: Adds noise to signal
		ONLY: Sets noise ONLY without additional signa

		Input:
			state: ADD, OFF or ONLY

		Output:
			None
		"""
		self.comm.write("SOUR%d:NOISE:STAT %s" % (modNumber, state))
		logger.info("Set Noise-Enabled: %s" % state)

	def getNoiseState(self, modNumber):
		"""
		Sets Noise-Enabled state

		Input:
			None

		Output:
			True or False
		"""
		noise=self.comm.query("SOUR%d:NOIS:STAT?" % modNumber)
		logger.info("Got Noise-Enabled: %s" % noise)
		return noise

	def setPilots(self, pilots, modNumber):
		if pilots is True:
			pil = 'ON'
		else:
			pil = 'OFF'	
		self.comm.write("SOUR%d:DVBS2:PIL %s" % (modNumber, pil))
		# super().setPilots(pilots)
		logger.info("Set pilot symbols enabled state: %r" % pilots)

	def getPilots(self, modNumber):
		pilots=self.comm.query("SOUR%d:DVBS2:PIL?" % modNumber)
		if pilots == '1':
			pilots = True
		if pilots == '0':
			pilots = False
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
		if cw==False:
			self.comm.write("SOUR%d:MOD:STAT ON" % modNumber)
		if cw==True:
			self.comm.write("SOUR%d:MOD:STAT OFF" % modNumber)
		logger.info("Set Carrier Wave Enabled state: %r" % cw)

	def getCW(self, modNumber):
		"""
		Gets Carrier Wave Enabled state

		Input:
			None

		Output:
			True or False
		"""
		state=self.comm.query("SOUR%d:MOD:STAT?"% modNumber)
		if state=="1":
			cw=False
		if state=="0":
			cw=True
		logger.info("Got Carrier Wave Enabled state: %r" % cw)
		return cw
	

	def setAlpha(self, alpha, modNumber):
		standard=self.getBroadcastStandard(modNumber)
		if standard=="DVBS":
			standard="DVBS1"
		if standard=="DVB-S2":
			standard="DVBS2"
		if standard=="DIR":
			standard="DIR"
		self.comm.write("SOUR%d:IQC:%s:ROLL %f" % (modNumber, standard,(alpha/100)))
		# super().setAlpha(alpha)
		logger.info("Set roll-off factor: %f%%" % alpha)

	def getAlpha(self, modNumber):		
		standard=self.getBroadcastStandard(modNumber)
		if standard=="DVBS":
			standard="DVBS1"
		if standard=="DVB-S2":
			standard="DVBS2"
		if standard=="DIR":
			standard="DIR"
		roll = self.comm.query("SOUR%d:IQC:%s:ROLL?" % (modNumber, standard))
		alpha=float(roll)*100
		# super().setAlpha(alpha)
		# alpha = super().getAlpha()
		logger.info("Got roll-off factor: %f%%" % alpha)
		return alpha


	def setPhaseNoise(self, phase, modNumber):
		"""
		Sets Phase Noise Enabled state

		Input:
			phase: True or False

		Output:
			None
		"""
		standard=self.getBroadcastStandard(modNumber)
		if standard=="DVBS":
			standard="DVBS1"
		if standard=="DVB-S2":
			standard="DVBS2"
		if standard=="DIR":
			standard="DIR"
		self.comm.write("SOUR%d:IQC:%s:PHAS:SHAPe1" %(modNumber, standard))
		self.comm.write("SOUR%d:IQC:%s:PHAS:MAGN 13" % (modNumber, standard))
		if phase == True:
			phase="ON"
		if phase == False:
			phase="OFF"
		self.comm.write("SOUR%d:IQC:%s:PHAS:STAT %s" % (modNumber, standard, phase))
		logger.info("Set Phase Noise Enabled state: %r" % phase)

	def getPhaseNoise(self, modNumber):
		"""
		Gets Phase Noise Enabled state

		Input:
			None

		Output:
			True or False
		"""
		standard=self.getBroadcastStandard(modNumber)
		if standard=="DVBS":
			standard="DVBS1"
		if standard=="DVB-S2":
			standard="DVBS2"
		if standard=="DIR":
			standard="DIR"

		state=self.comm.query("SOUR%d:IQC:%s:PHAS:STAT?" %(modNumber, standard))
		if state=="0":
			state=False	
		if state=="1":
			state=True
		logger.info("Got Phase Noise Enabled state: %r" % state)
		return state

	def setScramblingCode(self, scramb, modNumber):
		modulation=self.getBroadcastStandard(modNumber)
		if modulation!="DVB-S2":
			logger.error("DVB-S2 needs to be enabled before setting scrambling code")
		else:
			self.comm.write("SOUR%d:IQC:DVBS2:SPEC:SETT:STAT ON" % modNumber)
			self.comm.write("SOUR%d:IQC:DVBS2:SPEC:SCR:SEQ %d" % (modNumber, scramb))
		# super().setScramblingCode(scramb)
		logger.info("Set scrambling code: %d" % scramb)
	
	def getScramblingCode(self, modNumber):
		scramb=int(self.comm.query("SOUR%d:IQC:DVBS2:SPEC:SCR:SEQ?" % modNumber))
		# super().setScramblingCode(scramb)
		# scramb = super().getScramblingCode()
		logger.info("Got scrambling code: %d" % scramb)
		return scramb

	#def loadMultipath(self, modNumber, ):


	#def createMultipath(self, modNumber, taps, filename):
	#	enter frquency, gain and delay = -20e6, -1, 0

	def rfEnable(self, rf, modNumber):
		if (rf==True):
			rf="ON"
		if (rf==False):
			rf="OFF"
		self.comm.write("OUTP%d:STAT %s" %(modNumber, rf))
		
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
		if self.getBroadcastStandard(modNumber) == "DVB-S2":
			modcod=int(self.comm.query("SOUR%d:IQC:DVBS2:TSL1:MODCOD?" %(modNumber)))
			logger.debug("the modcod is: %d" % modcod)
			mod=self.constellation[modcod][0]
			logger.debug("the DVB-S2 mod is: %s" % mod)
			fec=self.constellation[modcod][1]
			logger.debug("The DVB-S2 fec is: %s" % fec)
			return (mod, fec)

		if self.getBroadcastStandard(modNumber)=="DVBS":
			standard="DVBS1"
		if self.getBroadcastStandard(modNumber)=="DIRECTV":
			standard="DIR"
		mod=self.comm.query("SOUR%d:IQC:%s:CONS?" %(modNumber, standard))
		if mod=="S4":
			mod="QPSK"
		if mod=="S8":
			mod="8PSK"
		fec=self.comm.query("SOUR%d:IQC:%s:RATE?" % (modNumber, standard))
		logger.debug("checking %s the fec after query is: %s" % (standard, fec))
		fec=fec.replace("R","")
		fec=fec.replace("_", "/")
		return (mod, fec)

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
		if self.getBroadcastStandard(modNumber) == "DVB-S2":
			######## REPLACE THIS WITH YOUR OWN CODE ########        
			value=(mod, fec)
			if value in self.reverse_const:
				index=self.reverse_const[value]
				self.comm.write("SOUR%d:IQC:DVBS2:TSL1:MODC %d" %(modNumber, index))
			else:
				print("Combination not available for DVB-S2")
		if self.getBroadcastStandard(modNumber)=="DVBS":
			if mod=="QPSK":
				mod="S4"
			if mod=="8PSK":
				mod="S8"
			self.comm.write("SOUR%d:IQC:DVBS1:CONS %s" %(modNumber, mod))
			fec=fec.replace("/","_")
			self.comm.write("SOUR%d:IQC:DVBS1:RATE R%s" %(modNumber, fec))
		if self.getBroadcastStandard(modNumber)=="DIRECTV":
			if mod=="QPSK":
				mod="S4"
			self.comm.write("SOUR%d:IQC:DIR:CONS %s" %(modNumber,mod))
			fec=fec.replace("/","_")
			self.comm.write("SOUR%d:IQC:DIR:RATE R%s" %(modNumber, fec))
			#

	@property
	def setConstellation(self):
		   raise AttributeError( "'BTC' object has no method 'setConstellation'" )

	@property
	def getConstellation(self):
		   raise AttributeError( "'BTC' object has no method 'getConstellation'" )

	@property
	def setCodeRate(self):
		   raise AttributeError( "'BTC' object has no method 'setCodeRate'" )

	@property
	def getCodeRate(self):
	   raise AttributeError( "'BTC' object has no method 'getCodeRate'" )    


	def enableDistortion(self, enable, modNumber):
		if enable==True:
			enable="ON"
		if enable==False:
			enable="OFF"
		self.comm.write("SOUR%d:DIST:TX %s" %(modNumber, enable))


	def loadDistortion(self, distortionFile, modNumber):
		distortionFile="D:\\Distortion\\TX\\"+distortionFile
		self.comm.write("SOUR%d:DIST:TX:FREQ:RESP:LOAD '%s'" %(modNumber, distortionFile))

	def loadFading(self, fadingFile, modNumber):
		fadingFile="D:\\fading\\user\\"+fadingFile
		logger.debug("loading profile %s" % fadingFile)
		self.comm.write("SOUR%d:FSIM:LOAD '%s'" %(modNumber,fadingFile))


	def enableFading(self, fading, modNumber):
		if fading==True:
			fading="ON"
		if fading==False:
			fading="OFF"
		self.comm.write("SOUR%d:FSIM:STAT %s" % (modNumber, fading))
	

	def setSignalNoiseLevel(self, cnr, modNumber):
		"""
		Sets Carrier-to-Noise Ratio

		Input:
			cnr: float cnr in dB

		Output:
			None
		"""
		self.comm.write("SOUR%d:DM:NOIS:AWGN:CN %f" % (modNumber, cnr))
		self.cnr=cnr
		logger.info("Set CNR: %f dB" % cnr)

	def getSignalNoiseLevel(self, modNumber):
		"""
		Gets Carrier-to-Noise Ratio

		Input:
			None

		Output:
			float cnr in dB 
		"""
		self.cnr=float(self.comm.query("SOUR%d:DM:NOIS:AWGN:CN?" % modNumber))
		logger.info("Got CNR: %f dB" % self.cnr)
		return self.cnr

	def setSignalNoiseState(self, state, modNumber):
		"""
		Sets Noise-Enabled state
		OFF: Sets Noise to OFF
		ADD: Adds noise to signal
		ONLY: Sets noise ONLY without additional signa

		Input:
			state: ADD, OFF or ONLY

		Output:
			None
		"""
		if state==True:
			state="ON"
		if state==False:
			state="OFF"
		self.comm.write("SOUR%d:DM:NOISE:AWGN %s" % (modNumber, state))
		logger.info("Set Noise-Enabled: %s" % state)

	def getSignalNoiseState(self, modNumber):
		"""
		Sets Noise-Enabled state

		Input:
			None

		Output:
			True or False
		"""
		noise=int(self.comm.query("SOUR%d:DM:NOISE:AWGN?" % modNumber))
		logger.info("Got Noise-Enabled: %s" % noise)
		if noise==0:
			noise=False
		if noise==1:
			noise=True
		return noise

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