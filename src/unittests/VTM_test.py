import pyvisa, logging, unittest
from . import BaseTests
from .context import SCTA
from SCTA.System import Mode, LocalOscillator, Transponder
from SCTA.Instrumentation import VTM 

# Setup debug logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VTM_Test(BaseTests.BaseModulatorTest):

	TEST_CLASS = VTM
	TEST_PROTOCOL = 'IP'
	TEST_IP='10.23.120.151'
	TEST_NUMMODS=5

	TEST_MODNUMBERS = list(range(1,TEST_NUMMODS+1))# list(range(17,28))
	TEST_BCSTDS = ["DVB-S2"] #, "DIRECTV", "DVBS"
	TEST_MODS = ["8PSK", "QPSK"]
	TEST_FECS_DVBS2 = ['1/2', '3/5', '2/3', '3/4', '4/5', '5/6', '8/9', '9/10']
	TEST_FREQS = [950e6 + x*100e6 for x in list(range(10))]	# L-Band frequencies: 250 - 2150 Hz
	TEST_SYMBS = [20e6, 30e6]		# Baud
	TEST_PILOTSS = [True, False]	# ON/OFF
	TEST_ROLLS = [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0]
	#TEST_SCRAMBS = list(range(11))	# 0 - 10
	TEST_INDICES = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]	# removed DIRECTV modes because SLG does not support
	TEST_TXPDRS = [Transponder(mode=index) for index in TEST_INDICES]
	TEST_PWRS = [-34.0 + x*5 for x in list(range(6))]	# -70 to -30 dBm
	TEST_CARRIERS = [True, False]
	TEST_MODSTATES = [True, False]
	TEST_SOURCES=["ETHERNET INPUT A", "PN23 INSERT", "PN23 INVERT", "RAMP GENERATOR", "PN15", "PN23 BONDED", "PN23 BONDED INVERT"]
	TEST_DATAPID=[3134, 5238, 1334]
	TEST_MARKERPID=[1313, 3018, 2334]
	TEST_CHUNKSIZE=[10, 34, 24, 42]
	TEST_BONDEDRATE=[20000000, 30000000, 15000000, 55000000]
	TEST_SKEW=[10, 5000, 40000]
	TEST_PHASE=[-53.3, -55.8, -78.3, -88.1, -92.1, -95.3, -96.8, -115.8]
	TEST_PHASEFREQS=[10, 100, 1000, 10000, 100000, 1E6, 10E6, 17E6]
	TEST_VTMMODE=["CCM", "LAB", "VTM"]


	#rm = pyvisa.ResourceManager()
	instrument = TEST_CLASS(ip=TEST_IP, numMods=TEST_NUMMODS)
	
	def __del__(self):
		# Does not need to explicitly close because TelnetComm Manager handles closes all resources at exist
		# self.instrument.comm.instrument.close()
		pass
	
	def getInstrument(self):
		return self.instrument

	def test_setVTMMode(self):
		for mode in self.TEST_VTMMODE:
			yield self.check_setVTMMode, mode

	def check_setVTMMode(self, test_mode): 
		self.getInstrument().setVTMMode(test_mode)
		actual_mode=self.getInstrument().getVTMMode()
		logger.info("test mode is %r" % test_mode)
		logger.info("actual mode is %r" % actual_mode)
		assert (test_mode == actual_mode)

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

	@unittest.skip("Skipping setConstellationCodeRate")
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

	@unittest.skip("Skipping setFrequency")
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

	@unittest.skip("Skipping setMode")
	def test_setMode(self):
		for modNumber in self.TEST_MODNUMBERS:
			for mode in self.TEST_INDICES:
				yield self.check_setMode, mode, modNumber

	def check_setMode(self, test_mode, modNumber):
		self.getInstrument().setMode(test_mode, modNumber)
		actual_mode = self.getInstrument().getMode(modNumber)
		logger.info("the actual setMode is: %r" % actual_mode)
		logger.info("the test setMode is: %r" % test_mode)
		assert (test_mode == actual_mode)

	@unittest.skip("Skipping setTransponder")
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

	def test_rfEnable(self):
 		for modState in self.TEST_MODSTATES:
 			yield self.check_rfEnable, modState 

	def check_rfEnable(self, test_modState):
		self.getInstrument().rfEnable(test_modState)
		actual_modState = self.getInstrument().getrfEnable()
		logger.info("actual state: %r" % actual_modState)
		logger.info("test state: %r" % test_modState)
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

	def test_setDataSource(self):
			for source in self.TEST_SOURCES:
				yield self.check_setDataSource, source
		
	def check_setDataSource(self, test_source):
		self.getInstrument().setDataSource(test_source)
		actual_source = self.getInstrument().getDataSource()
		logger.info("test source is %r" % test_source)
		logger.info("actual source is %r"% actual_source)
		assert (test_source == actual_source)

	def test_setDataPID(self):
		for PID in self.TEST_DATAPID:
			yield self.check_setDataPID, PID
		
	def check_setDataPID(self, test_PID):
		self.getInstrument().setDataPID(test_PID)
		actual_PID = self.getInstrument().getDataPID()
		logger.info("test pid is %r" % test_PID)
		logger.info("actual PID is %r"% actual_PID)
		assert (test_PID == actual_PID)


	def test_setMarkerPID(self):
		for PID in self.TEST_MARKERPID:
			yield self.check_setMarkerPID, PID
		
	def check_setMarkerPID(self, test_PID):
		self.getInstrument().setMarkerPID(test_PID)
		actual_PID = self.getInstrument().getMarkerPID()
		logger.info("test pid is %r" % test_PID)
		logger.info("actual PID is %r"% actual_PID)
		assert (test_PID == actual_PID)

	def test_setChunkSize(self):
		for size in self.TEST_CHUNKSIZE:
			yield self.check_setChunkSize, size

	def check_setChunkSize(self, test_size):
		self.getInstrument().setChunkSize(test_size)
		actual_size=self.getInstrument().getChunkSize()
		logger.info("test chunk size is %r" % test_size)
		logger.info("actual chunk size is %r " % actual_size)
		assert (test_size==actual_size)

	def test_setBondedRate(self):
		for rate in self.TEST_BONDEDRATE:
			yield self.check_setBondedRate, rate

	def check_setBondedRate(self, test_rate):
		self.getInstrument().setBondedRate(test_rate)
		actual_rate=self.getInstrument().getBondedRate()
		logger.info("test rate is %r" % test_rate)
		logger.info("actual rate is %r" % actual_rate)
		assert (test_rate == actual_rate)

	def test_setSkew(self):
		for modNumber in self.TEST_MODNUMBERS:
			for skew in self.TEST_SKEW:
				yield self.check_setSkew, skew, modNumber

	def check_setSkew(self, test_skew, modNumber): 
		self.getInstrument().setSkew(test_skew, modNumber)
		actual_skew=self.getInstrument().getSkew(modNumber)
		logger.info("test skew is %r" % test_skew)
		logger.info("actual skew is %r" % actual_skew)
		assert (test_skew == actual_skew)

	def test_setPhaseNoise(self):
		for FREQS, phase in zip(self.TEST_PHASEFREQS, self.TEST_PHASE):
			yield self.check_setPhaseNoise, FREQS, phase

	def check_setPhaseNoise(self, test_freq, test_phase): 
		self.getInstrument().setPhaseNoise(test_freq, test_phase)
		actual_phase=self.getInstrument().getPhaseNoise(test_freq)
		logger.info("test skew is %r" % test_phase)
		logger.info("actual skew is %r" % actual_phase)
		assert (test_phase == actual_phase)





