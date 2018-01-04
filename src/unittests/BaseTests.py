from abc import ABCMeta, abstractmethod
import pyvisa
import logging, unittest
from .context import SCTA
from SCTA.System import Mode, LocalOscillator, Transponder

# Setup debug logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class BaseTests:

	class BaseMoDemTest(object):

		__metaclass__ = ABCMeta

		TEST_CLASS = None		# An instrument class
		TEST_PROTOCOL = None	# Communication protocol
		TEST_PORT = None		# Port number/ address
		TEST_BCSTDS = ["DIRECTV", "DVBS", "DVB-S2"]
		TEST_MODS = ["8PSK", "QPSK"]
		TEST_FECS = ['1/2', '3/5', '2/3', '3/4', '4/5', '5/6', '6/7', '7/8', '8/9', '9/10']
		TEST_FREQS = [250e6 + x*100e6 for x in list(range(20))]	# L-Band frequencies: 250 - 2150 Hz
		TEST_SYMBS = [20e6, 30e6]		# Baud
		TEST_PILOTSS = [True, False]	# ON/OFF
		TEST_ROLLS = [20.0, 35.0]
		TEST_SCRAMBS = list(range(11))	# 0 - 10
		TEST_INDICES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24]

		def setUp(self):
			# self.rm = pyvisa.ResourceManager()
			# self.instrument = self.TEST_CLASS(type=self.TEST_PROTOCOL, port=self.TEST_PORT, rm=self.rm)
			pass
		
		def tearDown(self):
			# self.instrument.comm.instrument.close()
			pass

		@abstractmethod
		def getInstrument(self):
			pass

		def test_setBroadcastStandard(self):
			for bcstd in self.TEST_BCSTDS:
				yield self.check_setBroadcastStandard, bcstd

		def check_setBroadcastStandard(self, test_bcstd):
			self.getInstrument().setBroadcastStandard(test_bcstd)
			actual_bcstd = self.getInstrument().getBroadcastStandard()
			assert (actual_bcstd == test_bcstd)

		@unittest.skip("skipping setConstellation")
		def test_setConstellation(self):
			for mod in self.TEST_MODS:
				yield self.check_setConstellation, mod

		@unittest.skip("skipping setConstellation")
		def check_setConstellation(self, test_mod):
			self.getInstrument().setConstellation(test_mod)
			actual_mod = self.getInstrument().getConstellation()
			assert (test_mod == actual_mod)

		@unittest.skip("skipping code rate")		
		def test_setCodeRate(self):
			for fec in self.TEST_FECS:
				yield self.check_setCodeRate, fec

		@unittest.skip("skipping setConstellation")
		def check_setCodeRate(self, test_fec):
			self.getInstrument().setCodeRate(test_fec)
			actual_fec = self.getInstrument().getCodeRate()
			assert (test_fec == actual_fec)

		def test_setFrequency(self):
			for freq in self.TEST_FREQS:
				yield self.check_setFrequency, freq

		def check_setFrequency(self, test_freq):
			self.getInstrument().setFrequency(test_freq)
			actual_freq = self.getInstrument().getFrequency()
			assert (test_freq == actual_freq)

		def test_setSymbolRate(self):
			for symb in self.TEST_SYMBS:
				yield self.check_setSymbolRate, symb

		def check_setSymbolRate(self, test_symb):
			self.getInstrument().setSymbolRate(test_symb)
			actual_symb = self.getInstrument().getSymbolRate()
			assert (test_symb == actual_symb)

		def test_setPilots(self):
			for pilots in self.TEST_PILOTSS:
				yield self.check_setPilots, pilots

		def check_setPilots(self, test_pilots):
			self.getInstrument().setPilots(test_pilots)
			actual_pilots = self.getInstrument().getPilots()
			assert (test_pilots == actual_pilots)

		def test_setAlpha(self):
			for roll in self.TEST_ROLLS:
				yield self.check_setAlpha, roll

		def check_setAlpha(self, test_roll):
			self.getInstrument().setAlpha(test_roll)
			actual_roll = self.getInstrument().getAlpha()
			assert (test_roll == actual_roll)

		@unittest.skip("skipping setScrambling Code Basetest")
		def test_setScramblingCode(self):
			for scramb in self.TEST_SCRAMBS:
				yield self.check_setScramblingCode, scramb

		@unittest.skip("skipping setScrambling Code Basetest")
		def check_setScramblingCode(self, test_scramb):
			self.getInstrument().setScramblingCode(test_scramb)
			actual_scramb = self.getInstrument().getScramblingCode()
			assert (test_scramb == actual_scramb)

		def test_setTransponder(self):
			for index in self.TEST_INDICES:
				logger.debug("index = %d" % index)
				txpdr = Transponder(mode=index)
				logger.debug("txpdr = %r" % txpdr)
				if index == 3:
					assert txpdr.getBroadcastStandard() == 'DVB-S2'
				yield self.check_setTransponder, txpdr

		def check_setTransponder(self, test_txpdr):
			self.getInstrument().setTransponder(test_txpdr)
			actual_txpdr = self.getInstrument().getTransponder()
			logger.debug("test_txpdr: %r" % test_txpdr)
			logger.debug("actual_txpdr: %r" % actual_txpdr)
			assert (test_txpdr == actual_txpdr)


	class BaseModulatorTest(BaseMoDemTest):

		__metaclass__ = ABCMeta

		TEST_PWRS = [-70.0 + x*5 for x in list(range(9))]	# -70 to -30 dBm
		
		@abstractmethod
		def getInstrument(self):
			pass

		def test_setPower(self):
			for power in self.TEST_PWRS:
				yield self.check_setPower, power
			
		def check_setPower(self, test_power):
			self.getInstrument().setPower(test_power)
			actual_power = self.getInstrument().getPower()
			assert (test_power == actual_power)

	class BaseDemodulatorTest(BaseMoDemTest):
		__metaclass__ = ABCMeta

		@abstractmethod
		def getInstrument(self):
			pass
