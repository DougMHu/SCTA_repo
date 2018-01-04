from . import Modulator
from . import TelnetComm
from ..System import Mode, Transponder
import logging
import time

logger = logging.getLogger(__name__)

class SLG(Modulator):

	def __init__(self, id="SLG", ip="192.168.10.1", port=5025, numMods=32):
		"""Constructor.

		~~~ Valid ranges ~~~
		type:        [GPIB, IP]
		port:        [28 or 192.10.10.10]
		cnr:         [0, 20] dB
		"""

		self.comm = TelnetComm(ip=ip, port=port, commands='SCPI')
		self.cnr=None
		self.numMods=numMods
		self.bcstd="DVB-S2"
		for mods in list(range(1, numMods+1)):
			self.setCarrierType("SINGLE", mods)
			if mods<=16:
				self.setInputSource("PN", mods)
			else:
				self.setInputSource("LOAD", mods)

	def loadConfigFile(self, file):
		"""
		Loads the selected file to the SLG.
		"""
		self.comm.write("MMEMory:LOAD:STATe 0, '%s'" % file)

	def setTransponder(self, txpdr, modNumber):
		"""
		Sets the transponder settings to the SLG from the Modulator class.
		"""
		#self.setInputSource("PN", modNumber)		#Input set to Load for testing of SLG class. Default should be seto to PN23 for mods 1-16 and LOAD for 17-32 since the SLG is not able to set data on mods higher than 16. 
		self.setCarrierType("SINGLE", modNumber)
		self.setMode(txpdr.getMode(), modNumber)
		# set this transponder's parameters to corresponding input parameters
		self.setFrequency(txpdr.getFrequency(), modNumber)
		self.setSymbolRate(txpdr.getSymbolRate(), modNumber)
		self.setAlpha(txpdr.getAlpha(), modNumber)
		self.setPilots(txpdr.getPilots(), modNumber)

	def getTransponder(self, modNumber):
		"""
		Gets the current transponder parameters

		Input:
			None

		Output:
			Transponder object
		"""
		mode = self.getMode(modNumber)
		freq = self.getFrequency(modNumber)
		symb = self.getSymbolRate(modNumber)
		roll = self.getAlpha(modNumber)
		scramb = 0
		pilots = self.getPilots(modNumber)
		# pol = self.getPolarity()
		# LO = self.getLocalOscillator()
		return Transponder(mode=mode, freq=freq, symb=symb, roll=roll, scramb=scramb, pilots=pilots)#, pol=pol, LO=LO)


	def setAllTransponders(self, txpdr):
		for mod in list(range(1, self.numMods+1)):
			self.setTransponder(txpdr, mod)
		"""	self.setMode(txpdr.getMode(), mod)
			# set this transponder's parameters to corresponding input parameters
			self.setFrequency(txpdr.getFrequency(), mod)
			self.setSymbolRate(txpdr.getSymbolRate(), mod)
			self.setAlpha(txpdr.getAlpha(), mod)
			self.setPilots(txpdr.getPilots(), mod)"""



	def getMode(self, modNumber):
		"""
		Gets the current mode

		Input:
			None

		Output:
			Either an integer AMC Mode Number or a custom Mode Object
		"""
		mode = Mode(bcstd=self.getBroadcastStandard(modNumber), mod=self.getConstellation(modNumber), fec=self.getCodeRate(modNumber))
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
		self.setConstellation(mode.getConstellation(), modNumber)
		self.setCodeRate(mode.getCodeRate(), modNumber)


	def setPower(self, power, modNumber):
		"""
		Sets Power to desired level for modulator selected.
		"""
		self.comm.write("POW:CHAN"+str(modNumber)+":LEV %f"% power)



	def getPower(self, modNumber):
		power=float(self.comm.query("POW:CHAN%d:LEV?" % modNumber))
		return power

	def setFrequency(self, freq, modNumber):
		self.comm.write("FREQ:CHAN%d:FREQ %d"% (modNumber, freq))


	def getFrequency(self, modNumber):
		freq=float(self.comm.query("FREQ:CHAN%d:FREQ?" % modNumber))
		return freq


	def setSymbolRate(self, symb, modNumber):
		self.comm.write("MOD:CHAN%d:SYMB %s" % (modNumber,symb))

	def getSymbolRate(self, modNumber):
		symb=float(self.comm.query("MOD:CHAN%d:SYMB?" % modNumber))
		return symb

	def setPilots(self, pilots, modNumber):
		if pilots==True:
			self.comm.write("MOD:CHAN%d:FORM:PIL ON" % modNumber)
		if pilots==False:
			self.comm.write("MOD:CHAN%d:FORM:PIL OFF" % modNumber)


	def getPilots(self, modNumber):
		pilots=self.comm.query("MOD:CHAN%d:FORM:PIL?" % modNumber)
		if pilots=="ON":
			return True
		if pilots=="OFF":
			return False



	def setCarrierType(self, carrier, modNumber):
		"""
		Selects the carrier type for an output channel:
		SINGle= (defaul)_
		MULTiple
		CW
		"""
		self.comm.write("MOD:CHAN%d:CARRier %s"% (modNumber, carrier))

	def getCarrierType(self, modNUmber):
		"""
		Returns the carrier type for the selected output channel.
		"""
		carrier=self.comm.query("MOD:CHAN"+str(modNUmber)+":CARR?")
		if carrier=="SING":
			carrier="SINGLE"
		if carrier=="MULT":
			carrier="MULTIPLE"
		if carrier=="CW":
			carrier="CW"
		return carrier


	def setModulatorState(self, state, modNumber):
		"""
		This function will set the modulator state to ON/FF:

		state: True (ON), False (OFF)
		modNumber: modulator number on the SLG (1-32)
		"""
		if state==True:
			self.comm.write("MODulator:CHANnel%d:STATe ON" % modNumber)
		if state==False:
			self.comm.write("MODulator:CHANnel%d:STATe OFF" % modNumber)


	def getModulatorState(self, modNumber):
		"""
		This function will obtain the current modulator state of the SLG. 
		Returns True for ON, False for OFF
		"""
		state=self.comm.query("MODulator:CHANnel%d:STATe?"% modNumber)
		if state=="ON":
			return True
		if state=="OFF":
			return False


	def setInputSource(self, source, modNumber):
		"""Constructor.
		Possible settings are:
		ASIA
		ASIB
		ETHA
		ETHB
		AWG
		LOAD
		PN
		TSG
		"""
		self.comm.write("MOD:CHAN%d:SOUR %s" % (modNumber,source))
		if source=="PN":
			self.comm.write("MOD:CHAN%d:SOUR PN23 SYNC"% modNumber)


	def getInputSource(self, modNumber):
		"""
		Returns the input source.
		"""
		source=self.comm.query("MOD:CHAN%d:SOUR?" % modNumber)
		return source


	def setConstellation(self, constellation, modNumber):
		if constellation=="8PSK":
			self.comm.write("MOD:CHAN"+str(modNumber)+":FORM:CONS PSK8")
		else: 
			self.comm.write("MOD:CHAN"+str(modNumber)+":FORM:CONS "+str(constellation))


	def getConstellation(self, modNumber):
		constellation=self.comm.query("MOD:CHAN%d:FORM:CONS?"% modNumber)
		if constellation=="PSK8":
			return "8PSK"
		return constellation

	def setBroadcastStandard(self, bcstd, modNumber):
		if bcstd=="DVB-S2":
			self.comm.write("MOD:CHAN%d:FORM DVBS2" % modNumber)
		self.comm.write("MOD:CHAN%d:FORM %s"% (modNumber, bcstd))


	def getBroadcastStandard(self, modNumber):
		bcstd=str(self.comm.query("MOD:CHAN%d:FORM?"% modNumber))
		if bcstd=="DVBS2":
			return "DVB-S2"
		return bcstd


	def setCodeRate(self, fec, modNumber):
		"""
		This function will set the FEC code rate for each modulator in the SLG. 
		"""
		fec=fec.replace("/","_")
		self.comm.write("MOD:CHAN%d:FORM:RATE R%s"% (modNumber, fec))


	def getCodeRate(self, modNumber):
		"""
		This function will obtain the current FEC rate for the selected modulator on the SLG.
		"""
		fec=self.comm.query("MOD:CHAN%d:FORM:RATE?"% modNumber)
		fec=fec.replace("R","")
		fec=fec.replace("_","/")
		return fec

	def setAlpha(self, alpha, modNumber):
		"""
		This function will set the roll-off (Alpha) on the desired modulator.
		"""
		alpha=int(alpha)
		self.comm.write("MOD:CHAN%d:ROLL %d"%(modNumber, alpha))

	def getAlpha(self, modNumber):
		alpha=int(self.comm.query("MOD:CHAN%d:ROLL?"% modNumber))
		return alpha


	def setBandRange(self, band):
		if band=="250":
			band="B0250_0750"
		if band=="550":
			band="B0550_1050"
		if band=="950":
			band="B0950_1450"
		if band=="1250":
			band="B1250_1750"
		if band=="1550":
			band="B1550_2150"
		if band=="2050":
			band="B2050_2650"
		if band=="2500":
			band="B2500_3000"
		self.comm.write("OUTPut:BAND %s"% band)

	def getBandRange(self):
		band=self.comm.query("OUTP:BAND?")
		if band=="B025":
			band="250"
		if band=="B055":
			band="550"
		if band=="B095":
			band="950"
		if band=="B125":
			band="1250"
		if band=="B155":
			band="1550"
		if band=="B205":
			band="2050"
		if band=="B250":
			band="2500"
		return band



