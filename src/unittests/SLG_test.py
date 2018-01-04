import pyvisa, logging, unittest
from . import BaseTests
from .context import SCTA
from SCTA.System import Mode, LocalOscillator, Transponder
from SCTA.Instrumentation import FSW, SLG

# Setup debug logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class SLG_Test(object):

	TEST_CLASS = SLG
	TEST_PROTOCOL = 'IP'
	TEST_IP='192.168.10.1'
	TEST_PORT = 5025
	TEST_NUMMODS=32

	TEST_MODNUMBERS = list(range(1,TEST_NUMMODS+1))# list(range(17,28))
	TEST_BCSTDS = ["DVBS", "DVB-S2"]
	TEST_MODS = ["8PSK", "QPSK"]
	TEST_FECS = ['1/2', '3/5', '2/3', '3/4', '4/5', '5/6', '6/7', '7/8', '8/9', '9/10']
	TEST_FREQS = [250e6 + x*100e6 for x in list(range(20))]	# L-Band frequencies: 250 - 2150 Hz
	TEST_SYMBS = [20e6, 30e6]		# Baud
	TEST_PILOTSS = [True, False]	# ON/OFF
	TEST_ROLLS = [20.0, 35.0]
	#TEST_SCRAMBS = list(range(11))	# 0 - 10
	TEST_INDICES = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23]	# removed DIRECTV modes because SLG does not support
	TEST_TXPDRS = [Transponder(mode=index) for index in TEST_INDICES]
	TEST_PWRS = [-45.0 + x*5 for x in list(range(9))]	# -70 to -30 dBm
	TEST_CARRIERS = ["SINGLE", "MULTIPLE", "CW"]
	TEST_MODSTATES = [True, False]
	TEST_INPUTSOURCES = ["ASIA", "ASIB", "ETHA", "ETHB", "AWG", "LOAD", "PN", "TSG"]
	TEST_BANDRANGES = ["250", "550", "950", "1250", "1550", "2050", "2500"]
	TEST_CONFIGFILES = ["/DSWM/SLG1_DSWM_US_23CH_1B_20MS.cfg"]


	rm = pyvisa.ResourceManager()
	instrument = TEST_CLASS(ip=TEST_IP, port=TEST_PORT, numMods=TEST_NUMMODS)

	def __del__(self):
		# Does not need to explicitly close because TelnetComm Manager handles closes all resources at exist
		# self.instrument.comm.instrument.close()
		pass

	def getInstrument(self):
		return self.instrument

	def test_setBroadcastStandard(self):
		for modNumber in self.TEST_MODNUMBERS:
			for bcstd in self.TEST_BCSTDS:
				yield self.check_setBroadcastStandard, bcstd, modNumber

	def check_setBroadcastStandard(self, test_bcstd, modNumber):
		self.getInstrument().setBroadcastStandard(test_bcstd, modNumber)
		actual_bcstd = self.getInstrument().getBroadcastStandard(modNumber)
		assert (actual_bcstd == test_bcstd)

	def test_setConstellation(self):
		for modNumber in self.TEST_MODNUMBERS:
			for mod in self.TEST_MODS:
				yield self.check_setConstellation, mod, modNumber

	def check_setConstellation(self, test_mod, modNumber):
		self.getInstrument().setConstellation(test_mod, modNumber)
		actual_mod = self.getInstrument().getConstellation(modNumber)
		assert (test_mod == actual_mod)

	def test_setCodeRate(self):
		for modNumber in self.TEST_MODNUMBERS:
			for fec in self.TEST_FECS:
				yield self.check_setCodeRate, fec, modNumber

	def check_setCodeRate(self, test_fec, modNumber):
		self.getInstrument().setCodeRate(test_fec, modNumber)
		actual_fec = self.getInstrument().getCodeRate(modNumber)
		assert (test_fec == actual_fec)

	def test_setFrequency(self):
		for modNumber in self.TEST_MODNUMBERS:
			for band in self.TEST_BANDRANGES:
				start = int(band)
				freq=int(start*1e6)
				logger.debug("band = %d" % start)
				self.getInstrument().setBandRange(band)
				for index in list(range(freq, freq+int(400e6), int(50e6))):
					yield self.check_setFrequency, freq, modNumber

	def check_setFrequency(self, test_freq, modNumber):
		self.getInstrument().setFrequency(test_freq, modNumber)
		actual_freq = self.getInstrument().getFrequency(modNumber)
		assert (test_freq == actual_freq)


	def test_setSymbolRate(self):
		for modNumber in self.TEST_MODNUMBERS:
			for symb in self.TEST_SYMBS:
				yield self.check_setSymbolRate, symb, modNumber

	def check_setSymbolRate(self, test_symb, modNumber):
		self.getInstrument().setSymbolRate(test_symb, modNumber)
		actual_symb = self.getInstrument().getSymbolRate(modNumber)
		assert (test_symb == actual_symb)

	def test_setPilots(self):
		for modNumber in self.TEST_MODNUMBERS:
			for pilots in self.TEST_PILOTSS:
				yield self.check_setPilots, pilots, modNumber

	def check_setPilots(self, test_pilots, modNumber):
		self.getInstrument().setPilots(test_pilots, modNumber)
		actual_pilots = self.getInstrument().getPilots(modNumber)
		assert (test_pilots == actual_pilots)

	def test_setAlpha(self):
		for modNumber in self.TEST_MODNUMBERS:
			for roll in self.TEST_ROLLS:
				yield self.check_setAlpha, roll, modNumber

	def check_setAlpha(self, test_roll, modNumber):
		self.getInstrument().setAlpha(test_roll, modNumber)
		actual_roll = self.getInstrument().getAlpha(modNumber)
		assert (test_roll == actual_roll)

	def test_setMode(self):
		for modNumber in self.TEST_MODNUMBERS:
			for mode in self.TEST_INDICES:
				yield self.check_setMode, mode, modNumber

	def check_setMode(self, test_mode, modNumber):
		self.getInstrument().setMode(test_mode, modNumber)
		actual_mode = self.getInstrument().getMode(modNumber)
		assert (test_mode == actual_mode)

	def test_setTransponder(self):
		self.getInstrument().setBandRange("950")
		for modNumber in self.TEST_MODNUMBERS:
			for index in self.TEST_INDICES:
				logger.debug("index = %d" % index)
				txpdr = Transponder(mode=index, freq=1200e6)
				logger.debug("txpdr = %r" % txpdr)
				if index == 3:
					assert txpdr.getBroadcastStandard() == 'DVB-S2'
				yield self.check_setTransponder, txpdr, modNumber

	def check_setTransponder(self, test_txpdr, modNumber):
		self.getInstrument().setTransponder(test_txpdr, modNumber)
		actual_txpdr = self.getInstrument().getTransponder(modNumber)
		logger.debug("test_txpdr: %r" % test_txpdr)
		logger.debug("actual_txpdr: %r" % actual_txpdr)
		assert (test_txpdr == actual_txpdr)
		for state in self.TEST_MODSTATES:
			self.check_setModulatorState(state, modNumber)

	# def test_setAllTransponders(self):
	# 	for txpdr in self.TEST_TXPDRS:
	# 		yield self.check_setAllTransponders, txpdr

	# def check_setAllTransponders(self, test_txpdr):
	# 	self.getInstrument().setAllTransponders(test_txpdr)
	# 	for index in self.TEST_MODNUMBERS:
	# 		actual_txpdr = self.getInstrument().getTransponder(index)
	# 		logger.debug("test_txpdr: %r" % test_txpdr)
	# 		logger.debug("actual_txpdr: %r" % actual_txpdr)
	# 		assert (test_txpdr == actual_txpdr)

	def test_setPower(self):
		for modNumber in self.TEST_MODNUMBERS:
			for power in self.TEST_PWRS:
				yield self.check_setPower, power, modNumber
		
	def check_setPower(self, test_power, modNumber):
		self.getInstrument().setPower(test_power, modNumber)
		actual_power = self.getInstrument().getPower(modNumber)
		assert (test_power == actual_power)

	def test_setCarrierType(self):
		for modNumber in self.TEST_MODNUMBERS:
			for carrier in self.TEST_CARRIERS:
				yield self.check_setCarrierType, carrier, modNumber

	def check_setCarrierType(self, test_carrier, modNumber):
		self.getInstrument().setCarrierType(test_carrier, modNumber)
		actual_carrier = self.getInstrument().getCarrierType(modNumber)
		assert (test_carrier == actual_carrier)

	# def test_setModulatorState(self):
	# 	for modNumber in self.TEST_MODNUMBERS:
	# 		for modState in self.TEST_MODSTATES:
	# 			yield self.check_setModulatorState, modState, modNumber

	def check_setModulatorState(self, test_modState, modNumber):
		self.getInstrument().setModulatorState(test_modState, modNumber)
		actual_modState = self.getInstrument().getModulatorState(modNumber)
		assert (test_modState == actual_modState)

	def test_setInputSource(self):
		for modNumber in self.TEST_MODNUMBERS:
			for inputSource in self.TEST_INPUTSOURCES:
				yield self.check_setInputSource, inputSource, modNumber

	def check_setInputSource(self, test_inputSource, modNumber):
		self.getInstrument().setInputSource(test_inputSource, modNumber)
		actual_inputSource = self.getInstrument().getInputSource(modNumber)
		assert (test_inputSource == actual_inputSource)

	def test_setBandRange(self):
		for modNumber in self.TEST_MODNUMBERS:
			for bandRange in self.TEST_BANDRANGES:
				yield self.check_setBandRange, bandRange

	def check_setBandRange(self, test_bandRange):
		self.getInstrument().setBandRange(test_bandRange)
		actual_bandRange = self.getInstrument().getBandRange()
		assert (test_bandRange == actual_bandRange)

	
	def test_loadConfigFile(self):
		for configFile in self.TEST_CONFIGFILES:
			yield self.check_loadConfigFile, configFile

	def check_loadConfigFile(self, test_configFile):
		self.getInstrument().loadConfigFile(test_configFile)
		response = input("Was the Scenario loaded correctly? [y/n]: ") 
		if response == 'y':
			assert True
		else:
			assert False
	
