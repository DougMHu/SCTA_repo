from . import Modulator
from . import Comm
import logging
import time
from .ResourceManagers import PyvisaResourceManager

logger = logging.getLogger(__name__)

class SFU(Modulator):

	def __init__(self, id="SFU", type="GPIB", port="28"):
		"""
		Creates an SFU object, which starts a connection for reading and writing commands to the SFU.
		With no inputs specified, it assumes the host computer's interface is GPIB at port 28.

		Input:
			id: string
			type: string interface type
			port: string interface address/ port

		Output:
			SFU object

		~~~ Valid ranges ~~~
		type:        ['GPIB', 'IP']
		port:        ['28' or '192.10.10.10']
		cnr:         [0, 20] dB
		"""

		self.comm = Comm(protocol=type, port=port)
		self.cnr=None
		super ().__init__(id=id)
		self.config()

	def __del__(self):
		self.close()

	def close(self):
		"""
		Closes the connection with the SFU
		NOTE: YOU MUST CALL THIS AFTER YOU ARE FINISHED WITH THE SFU

		Input:
			None

		Output:
			None
		"""
		self.comm.instrument.close()

	def config(self):
		"""
		Configures SFU for operation. Only called by SFU __init__
		WARNING: NOT A USER FUNCTION

		Input:
			None

		Output:
			None
		"""
		logger.info("SFU device ID: %s" % (self.comm.query("*IDN?")) )
		self.comm.write("SYST:DISP:UPD ON")
		self.comm.write("SOUR:NOIS:COUP ON") 				#Sets bandwidth coupling ON
		self.comm.write("SOUR:NOISE:AWGN ON")				#Enables AWGN
		self.comm.write("SOUR:DM:SOUR DTV")					#Configures SFU to DTV mode 
		self.comm.write("SOUR:DM:TRAN:STAN DVS2")			#Configures SFU for DVBS2 standard
		self.comm.write("SOUR:IQC:DVBS2:AMC DVS2")			#Configures SFU for DVBS2 Standard)
		self.comm.write("SOUR:IQC:DVBS2:SOUR TEST")			#Configures SFU for Test mode
		self.comm.write("SOUR:IQC:DVBS2:FECF NORM")			#Configures SFU FEC 
		self.comm.write("SOUR:IQC:DVBS2:TSP S187")			#Configures SFU for 187 byte packets for DVBS2
		self.comm.write("SOUR:IQC:DVBS2:PRBS:SEQ P23_1")	#Configures packets to have PRBS 2^(23-1)
		logger.info("SFU configuration complete")

	def setBroadcastStandard(self, bcstd):
		###########################################################
		# BUG: Must send 2 different commands for setting code rate
		# because the broadcast standard works differently for
		# different SFUs.
		###########################################################

		self.comm.write("SOUR:DM:SOUR DTV")					#Configures SFU to DTV mode 

		if bcstd=="DVB-S2":
			self.comm.write("SOUR:DM:TRAN:STAN DVS2")
			self.comm.write("SOUR:IQC:DVBS2:AMC DVS2")

		else:
			#Changes made by Chuck 10/31/2016
			self.comm.write("SOUR:DM:TRAN:STAN "+str(bcstd))			#Configures SFU for DVBS2 standard
			#Wrong SCPI command
			self.comm.write("SOUR:IQC:DVBS2:AMC " +str(bcstd))
		super().setBroadcastStandard(bcstd)
		logger.info("Set broadcast standard: %s" % bcstd)

	def getBroadcastStandard(self):
		###########################################################
		# BUG: Please use super().getBroadcastStandard() because
		# self.getBroadcastStandard() gives inconsistent results
		# See: self.setBroadcastStandard() bug
		###########################################################
		# bcstd=self.comm.query("SOUR:IQC:DVBS2:AMC?")
		# if bcstd=="DVS2":
		# 	bcstd = "DVB-S2"
		# if bcstd == "DIR":
		# 	bcstd = "DIRECTV"
		# super().setBroadcastStandard(bcstd)
		# bcstd = super().getBroadcastStandard()
		# logger.info("Got broadcast standard: %s" % bcstd)
		bcstd = super().getBroadcastStandard()
		return bcstd

	def setPower(self, power):
		"""
		Sets SFU RF power

		Input:
			power: float power in dBm

		Output:
			None
		"""
		self.comm.write("SOUR:POW:LEV:IMM:AMPL " + str(power)+str(""))
		self.power=power
		logger.info("Set power: %f dBm" % power)

	def getPower(self):
		"""
		Gets SFU RF power

		Input:
			None

		Output:
			float power in dBm
		"""
		self.power = float(self.comm.query("SOUR:POW:LEV:IMM:AMPL?"))
		logger.info("Got power: %f dBm" % self.power)
		return self.power

	def setFrequency(self, freq):
		self.comm.write("SOUR:FREQ:ACT:CENT " + str(freq)+str(""))
		super().setFrequency(freq)
		logger.info("Set frequency: %f MHz" % (freq/1e6))
	
	def getFrequency(self):
		freq=float(self.comm.query("SOUR:FREQ:ACT:CENT?"))
		super().setFrequency(freq)
		freq = super().getFrequency()
		logger.info("Got frequency: %f MHz" % (freq/1e6))
		return freq

	def setSymbolRate(self, rate):
		self.comm.write("SOUR:IQC:DVBS2:SYMB:RATE " + str(rate)+str(""))
		super().setSymbolRate(rate)
		logger.info("Set symbol rate: %f MBaud" % (rate/1e6))

	def getSymbolRate(self):
		symb=float(self.comm.query("SOUR:IQC:DVBS2:SYMB:RATE?"))
		super().setSymbolRate(symb)
		symb = super().getSymbolRate()
		logger.info("Got symbol rate: %f MBaud" % (symb/1e6))
		return symb

	def setNoiseLevel(self, cnr):
		"""
		Sets Carrier-to-Noise Ratio

		Input:
			cnr: float cnr in dB

		Output:
			None
		"""
		self.comm.write("SOUR:NOIS:CN %f" % cnr + str(""))
		self.cnr=cnr
		logger.info("Set CNR: %f dB" % cnr)

	def getNoiseLevel(self):
		"""
		Gets Carrier-to-Noise Ratio

		Input:
			None

		Output:
			float cnr in dB 
		"""
		self.cnr=float(self.comm.query("SOUR:NOIS:CN?"))
		logger.info("Got CNR: %f dB" % self.cnr)
		return self.cnr

	def setNoiseState(self, state):
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

		self.comm.write("SOUR:NOISE:STAT %s" % state)
		logger.info("Set Noise-Enabled: %s" % state)

	def getNoiseState(self):
		"""
		Sets Noise-Enabled state

		Input:
			None

		Output:
			True or False
		"""
		noise=self.comm.query("SOUR:NOIS:STAT?")
		logger.info("Got Noise-Enabled: %s" % noise)
		return noise

	def setPilots(self, pilots):
		if pilots is True:
			pil = 'ON'
		else:
			pil = 'OFF'	
		self.comm.write("SOUR:IQC:DVBS2:PIL %s" % pil)
		super().setPilots(pilots)
		logger.info("Set pilot symbols enabled state: %r" % pilots)

	def getPilots(self):
		pilots=self.comm.query("SOUR:IQC:DVBS2:PIL?")
		if pilots == '1':
			pilots = True
		if pilots == '0':
			pilots = False
		super().setPilots(pilots)
		pilots = super().getPilots()
		logger.info("Got pilot symbols enabled state: %r" % pilots)
		return pilots

	def setCW(self, cw):
		"""
		Sets Carrier Wave Enabled state

		Input:
			cw: True or False

		Output:
			None
		"""
		if cw==False:
			self.comm.write("SOUR:MOD:STAT ON")
		if cw==True:
			self.comm.write("SOUR:MOD:STAT OFF")
		logger.info("Set Carrier Wave Enabled state: %r" % cw)

	def getCW(self):
		"""
		Gets Carrier Wave Enabled state

		Input:
			None

		Output:
			True or False
		"""
		state=self.comm.query("SOUR:MOD:STAT?")
		if state=="1":
			cw=False
		if state=="0":
			cw=True
		logger.info("Got Carrier Wave Enabled state: %r" % cw)
		return cw
	

	def setAlpha(self, alpha):
		self.comm.write("SOUR:IQC:DVBS2:ROLL %f" % (alpha/100))
		super().setAlpha(alpha)
		logger.info("Set roll-off factor: %f%%" % alpha)

	def getAlpha(self):		
		roll = self.comm.query("SOUR:IQC:DVBS2:ROLL?")
		alpha=float(roll)*100
		super().setAlpha(alpha)
		alpha = super().getAlpha()
		logger.info("Got roll-off factor: %f%%" % alpha)
		return alpha


	def setPhaseNoise(self, phase):
		"""
		Sets Phase Noise Enabled state

		Input:
			phase: True or False

		Output:
			None
		"""
		self.comm.write("SOUR:IQC:DVBS2:PHAS:SHAPe1")
		self.comm.write("SOUR:IQC:DVBS2:PHAS:MAGN 13")
		if phase == True:
			self.comm.write("SOUR:IQC:DVBS2:PHAS:STAT ON")
		if phase == False:
			self.comm.write("SOUR:IQC:DVBS2:PHAS:STAT OFF")
		logger.info("Set Phase Noise Enabled state: %r" % phase)

	def getPhaseNoise(self):
		"""
		Gets Phase Noise Enabled state

		Input:
			None

		Output:
			True or False
		"""
		state=self.comm.query("SOUR:IQC:DVBS2:PHAS:STAT?")
		if state=="0":
			state=False	
		if state=="1":
			state=True
		logger.info("Got Phase Noise Enabled state: %r" % state)
		return state

	def setConstellation(self, modulation):
		if modulation=="QPSK":
			mod="S4"
		if modulation=="8PSK":
			mod="S8"
		self.comm.write("SOUR:IQC:DVBS2:CONS %s" % mod)
		super().setConstellation(modulation)
		logger.info("Set constellation: %s" % modulation)


	def getConstellation(self):
		modulation=self.comm.query("SOUR:IQC:DVBS2:CONS?")
		if modulation=="S4":
			modulation="QPSK"
		if modulation=="S8":
			modulation="8PSK"
		super().setConstellation(modulation)
		modulation = super().getConstellation()
		logger.info("Got constellation: %s" % modulation)
		return modulation

	def setCodeRate(self, fec):
		"""
		Sets the FEC code rate on the SFU. 
		"""
		###########################################################
		# BUG: Must use super().getBroadcastStandard() because
		# self.getBroadcastStandard() gives inconsistent results
		# See: self.setBroadcastStandard() bug
		###########################################################
		# BUG: Must send 2 different commands for setting code rate
		# because the broadcast standard works differently for
		# different SFUs.
		###########################################################
		if super().getBroadcastStandard()=="DVB-S2":
			standard="DVBS2"
		if super().getBroadcastStandard()=="DVBS":
			standard="DVBS"
		if super().getBroadcastStandard()=="DIRECTV":
			standard="DIR"
		code_rate=fec.replace("/","_")
		self.comm.write("SOUR:IQC:%s:RATE R%s" % (standard, code_rate))
		self.comm.write("SOUR:IQC:DVBS2:RATE R%s" % (code_rate))
		super().setCodeRate(fec)
		logger.info("Set code rate: %s" % fec)

	def getCodeRate(self):
		"""
		Obtains the code rate from the SFU.
		"""
		###########################################################
		# BUG: Must use super().getCodeRate() because
		# self.getBroadcastStandard() gives inconsistent results
		# See: self.setBroadcastStandard() bug
		###########################################################
		# BUG: Must send 2 different commands for setting code rate
		# because the broadcast standard works differently for
		# different SFUs.
		###########################################################
		# fec=self.comm.query("SOUR:IQC:DVBS2:RATE?")
		# fec=fec.replace("_","/")
		# fec=fec.replace("R","")
		# if fec=="9/1":
		# 	return "9/10"
		# super().setCodeRate(fec)
		# fec = super().getCodeRate()
		# logger.info("Got code rate: %s" % fec)
		fec = super().getCodeRate()
		return fec

	def setScramblingCode(self, scramb):
		"""
		Sets the scrambling code on the SFU. 
		"""
		modulation=super().getBroadcastStandard()
		if modulation!="DVB-S2":
			logger.error("DVB-S2 needs to be enabled before setting scrambling code")
		else:
			self.comm.write("SOUR:IQC:DVBS2:SPEC:SETT:STAT ON")
			self.comm.write("SOUR:IQC:DVBS2:SPEC:SCR:SEQ %d" % scramb)
		super().setScramblingCode(scramb)
		logger.info("Set scrambling code: %d" % scramb)
	
	def getScramblingCode(self):
		"""
		Obtains the current scrambling code set on the SFU. 
		"""
		scramb=int(self.comm.query("SOUR:IQC:DVBS2:SPEC:SCR:SEQ?"))
		super().setScramblingCode(scramb)
		scramb = super().getScramblingCode()
		logger.info("Got scrambling code: %d" % scramb)
		return scramb

	def setTxEnable(self, state):
		"""
		Enables the RF output state on the SFU to ON/OFF based on a True/False boolean.
		True=RF ON
		False=RF OFF
		"""
		if state==True:
			self.comm.write("OUTP:STAT ON")
		if state==False:
			self.comm.write("OUTP:STAT OFF")

	def getTxEnable(self):
		"""
		Queries the RF output state of the SFU. Returns True if the output is ON. False if RF output is off.
		"""
		tx=self.comm.query("OUTP:STAT?")
		if tx=="ON":
			return True
		if tx=="OFF":
			return False