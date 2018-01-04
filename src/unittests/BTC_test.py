import pyvisa, logging, unittest
from . import BaseTests
from .context import SCTA
from SCTA.System import Mode, LocalOscillator, Transponder
from SCTA.Instrumentation import BTC 

# Setup debug logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class BTC_Test(BaseTests.BaseModulatorTest):

	TEST_CLASS = BTC
	TEST_PROTOCOL = 'IP'
	TEST_IP='192.168.10.11'
	TEST_NUMMODS=2

	TEST_MODNUMBERS = list(range(1,TEST_NUMMODS+1))# list(range(17,28))
	TEST_BCSTDS = ["DVBS", "DVB-S2", "DIRECTV"]
	TEST_MODS = ["8PSK", "QPSK"]
	TEST_FECS_DVBS2 = ['1/2', '3/5', '2/3', '3/4', '4/5', '5/6', '8/9', '9/10']
	TEST_FECS_DIRECTV = ['1/2', '2/3', '6/7']
	TEST_FECS_DVBS = ['1/2', '2/3', '3/4', '5/6', '7/8']
	TEST_FREQS = [250e6 + x*100e6 for x in list(range(20))]	# L-Band frequencies: 250 - 2150 Hz
	TEST_SYMBS = [20e6, 30e6]		# Baud
	TEST_PILOTSS = [True, False]	# ON/OFF
	TEST_ROLLS = [20.0, 35.0]
	#TEST_SCRAMBS = list(range(11))	# 0 - 10
	TEST_INDICES = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23]	# removed DIRECTV modes because SLG does not support
	TEST_TXPDRS = [Transponder(mode=index) for index in TEST_INDICES]
	TEST_PWRS = [-45.0 + x*5 for x in list(range(9))]	# -70 to -30 dBm
	TEST_CARRIERS = [True, False]
	TEST_MODSTATES = [True, False]
	TEST_BANDRANGES = ["250", "550", "950", "1250", "1550", "2050", "2500"]
	TEST_CONFIGFILES = ["/DSWM/SLG1_DSWM_US_23CH_1B_20MS.cfg"]
	TEST_DISTORTION = ["aswm_saw4.distTXfr", "aswm_saw.distTXfr", "default.distTXfr", "aswm_SAW1.distTXfr"]
	TEST_FADING= ["fadingprof4.fad", "MULTIPATH#2.fad"]
	TEST_NOISE=[8, 10, 20]
	TEST_SIGNALNOISE=[9, 11, 19]
	TEST_NOISESTATE=["ADD", "OFF", "ONLY"]
	TEST_SIGNALSTATE=[True, False]

	#rm = pyvisa.ResourceManager()
	instrument = TEST_CLASS(type=TEST_PROTOCOL, port=TEST_IP, numMods=TEST_NUMMODS)
	
	def __del__(self):
		# Does not need to explicitly close because TelnetComm Manager handles closes all resources at exist
		# self.instrument.comm.instrument.close()
		pass
	
	def getInstrument(self):
		return self.instrument
	@unittest.skip("skipping fading")
	def test_loadFading(self):
		for modNumber in self.TEST_MODNUMBERS:
			for fading in self.TEST_FADING:
				self.getInstrument().loadFading(fading, modNumber)
				logger.debug("loading fading %s" % fading)
				response = input("Was the Fading profile loaded correctly? [y/n]: ") 
				if response == 'y':
					assert True
				else:
					assert False

	@unittest.skip("skipping distortion")
	def test_loadDistortion(self):
		for modNumber in self.TEST_MODNUMBERS:
			for distortion in self.TEST_DISTORTION:
				self.getInstrument().loadDistortion(distortion, modNumber)
				response = input("Was the Distorion loaded correctly? [y/n]: ") 
				if response == 'y':
					assert True
				else:
					assert False
	#@unittest.skip("Skipping broadcast standard")
	def test_setBroadcastStandard(self):
		for modNumber in self.TEST_MODNUMBERS:
			for bcstd in self.TEST_BCSTDS:
				yield self.check_setBroadcastStandard, bcstd, modNumber
	#@unittest.skip("Skipping broadcast standard")
	def check_setBroadcastStandard(self, test_bcstd, modNumber):
		self.getInstrument().setBroadcastStandard(test_bcstd, modNumber)
		actual_bcstd = self.getInstrument().getBroadcastStandard(modNumber)
		assert (actual_bcstd == test_bcstd)

	def test_setConstellationCodeRate(self):
		for modNumber in self.TEST_MODNUMBERS:
			for bcstds in self.TEST_BCSTDS:
				logger.debug("Bcstds set is: %s" % bcstds)
				if bcstds=="DIRECTV":
					#self.getInstrument().setBroadcastStandard(bcstds, modNumber)
					self.getInstrument().setBroadcastStandard(bcstds, modNumber)
					for mod in self.TEST_MODS:
						for fec in self.TEST_FECS_DIRECTV:
							yield self.check_setConstellationCodeRate, bcstds, mod, fec, modNumber
				if bcstds=="DVBS":
					self.getInstrument().setBroadcastStandard(bcstds, modNumber)
					for mod in self.TEST_MODS:
						for fec in self.TEST_FECS_DVBS:
							yield self.check_setConstellationCodeRate, bcstds, mod, fec, modNumber
				if bcstds=="DVB-S2":
					self.getInstrument().setBroadcastStandard(bcstds, modNumber)
					for mod in self.TEST_MODS:
						for fec in self.TEST_FECS_DVBS2:
							yield self.check_setConstellationCodeRate, bcstds, mod, fec, modNumber


	def check_setConstellationCodeRate(self, bcstds, test_mod, test_fec, modNumber):
		bcstds=self.getInstrument().getBroadcastStandard(modNumber)
		logger.debug("the BCSTDS is: %s" % bcstds)
		self.getInstrument().setConstellationCodeRate(test_mod, test_fec, modNumber)
		modcod = self.getInstrument().getConstellationCodeRate(modNumber)
		actual_mod=modcod[0]
		actual_fec=modcod[1]
		logger.debug("the actual_mod is: %r" % actual_mod)
		logger.debug("the test mod is: %r" % test_mod)
		logger.debug("the actual_fec is: %s" % actual_fec)
		logger.debug("the test fec is: %s" % test_fec)
		assert (test_mod == actual_mod)
		assert (test_fec== actual_fec)

	@unittest.skip("Skipping code rate")
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
			for freq in self.TEST_FREQS:
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

	def test_setCW(self):
		for modNumber in self.TEST_MODNUMBERS:
			for carrier in self.TEST_CARRIERS:
				yield self.check_setCW, carrier, modNumber

	def check_setCW(self, test_carrier, modNumber):
		self.getInstrument().setCW(test_carrier, modNumber)
		actual_carrier = self.getInstrument().getCW(modNumber)
		assert (test_carrier == actual_carrier)

	# def test_setModulatorState(self):
	# 	for modNumber in self.TEST_MODNUMBERS:
	# 		for modState in self.TEST_MODSTATES:
	# 			yield self.check_setModulatorState, modState, modNumber

	def check_setModulatorState(self, test_modState, modNumber):
		self.getInstrument().setModulatorState(test_modState, modNumber)
		actual_modState = self.getInstrument().getModulatorState(modNumber)
		assert (test_modState == actual_modState)

	def test_setScramblingCode(self):
		for modNumber in self.TEST_MODNUMBERS:
			for scramb in self.TEST_SCRAMBS:
				yield self.check_setScramblingCode, scramb, modNumber

	def check_setScramblingCode(self, test_scramb, modNumber):
		self.getInstrument().setBroadcastStandard("DVB-S2", modNumber)
		self.getInstrument().setScramblingCode(test_scramb, modNumber)
		actual_scramb = self.getInstrument().getScramblingCode(modNumber)
		assert (test_scramb == actual_scramb)

	def test_setNoiseLevel(self):
		for modNumber in self.TEST_MODNUMBERS:
			for noise in self.TEST_NOISE:
				yield self.check_setNoiseLevel, noise, modNumber
		
	def check_setNoiseLevel(self, test_noise, modNumber):
		self.getInstrument().setNoiseLevel(test_noise, modNumber)
		actual_noise = self.getInstrument().getNoiseLevel(modNumber)
		assert (test_noise == actual_noise)

	def test_setSignalNoiseLevel(self):
		for modNumber in self.TEST_MODNUMBERS:
			for noise in self.TEST_SIGNALNOISE:
				yield self.check_setSignalNoiseLevel, noise, modNumber
		
	def check_setSignalNoiseLevel(self, test_noise, modNumber):
		self.getInstrument().setSignalNoiseLevel(test_noise, modNumber)
		actual_noise = self.getInstrument().getSignalNoiseLevel(modNumber)
		assert (test_noise == actual_noise)

	def test_setNoiseState(self):
		for modNumber in self.TEST_MODNUMBERS:
			for noise in self.TEST_NOISESTATE:
				yield self.check_setNoiseState, noise, modNumber
		
	def check_setNoiseState(self, test_state, modNumber):
		self.getInstrument().setNoiseState(test_state, modNumber)
		actual_state = self.getInstrument().getNoiseState(modNumber)
		assert (test_state == actual_state)

	def test_setSignalNoiseState(self):
		for modNumber in self.TEST_MODNUMBERS:
			for state in self.TEST_SIGNALSTATE:
				yield self.check_setSignalNoiseState, state, modNumber
		
	def check_setSignalNoiseState(self, test_state, modNumber):
		self.getInstrument().setSignalNoiseState(test_state, modNumber)
		actual_state = self.getInstrument().getSignalNoiseState(modNumber)
		assert (test_state == actual_state)
'''
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
	
'''

	