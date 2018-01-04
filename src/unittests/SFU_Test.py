import logging, unittest
from . import BaseTests
from .context import SCTA
from SCTA.System import Mode, LocalOscillator, Transponder
from SCTA.Instrumentation import SFU

# Setup debug logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class SFU_Test(BaseTests.BaseModulatorTest):

	TEST_CLASS = SFU
	TEST_PROTOCOL = 'IP'
	TEST_PORT = '192.168.10.78'
	TEST_NOISES = [0.0 + 2*x for x in list(range(11))]	# 0 - 20 dB
	TEST_CWS = [True, False]
	TEST_PHASENOISES = [True, False]
	
	instrument = TEST_CLASS(type=TEST_PROTOCOL, port=TEST_PORT)

	# def __del__(self):
	# 	self.instrument.comm.instrument.close()

	def setUp(self):
		self.instrument.setBroadcastStandard("DVB-S2")
		self.instrument.setScramblingCode(0)

	def getInstrument(self):
		return self.instrument

	def test_setNoiseLevel(self):
		for noise in self.TEST_NOISES:
			yield self.check_setNoiseLevel, noise

	def check_setNoiseLevel(self, test_noise):
		self.instrument.setNoiseLevel(test_noise)
		actual_noise = self.instrument.getNoiseLevel()
		assert (test_noise == actual_noise)

	def test_setCW(self):
		for cw in self.TEST_CWS:
			yield self.check_setCW, cw

	def check_setCW(self, test_cw):
		self.instrument.setCW(test_cw)
		actual_cw = self.instrument.getCW()
		assert (test_cw == actual_cw)

	def test_setPhaseNoise(self):
		for phasenoise in self.TEST_PHASENOISES:
			yield self.check_setPhaseNoise, phasenoise

	def check_setPhaseNoise(self, test_phasenoise):
		self.instrument.setPhaseNoise(test_phasenoise)
		actual_phasenoise = self.instrument.getPhaseNoise()
		assert (test_phasenoise == actual_phasenoise)

if __name__ == '__main__' and __package__ is None:
	
	# Runs each test_ method in order
	unittest.main()
