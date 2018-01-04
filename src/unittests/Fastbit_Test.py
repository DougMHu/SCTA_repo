import logging, unittest
from .context import SCTA
from SCTA.System import Mode, Transponder
from SCTA.Instrumentation import Fastbit
from datetime import timedelta

# Setup debug logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class Fastbit_Test(object):

	TEST_CLASS = Fastbit
	TEST_PROTOCOL = 'GPIB'
	TEST_PORT = '8'
	TEST_LENGTHS = [8, 187, 188, 184, 1000]
	TEST_PAYLOADS = ["PN7", "PN11", "PN15", "PN20", "PN23"]
	TEST_PATTERNS = ['PRBS', 'MIX', 'WORD']
	TEST_TESTTIMES = [10, 30, 60]#, 120, 300]
	TEST_INTERFACES = ['SERIAL', 'PARALLEL']
	timedelt = timedelta(seconds=00)
	instrument = TEST_CLASS(type=TEST_PROTOCOL, port=TEST_PORT)

	def setUp(self):
		pass

	def test_setPayload(self):
		for payload in self.TEST_PAYLOADS:
			yield self.check_setPayload, payload

	def check_setPayload(self, test_payload):
		self.instrument.setPayload(test_payload)
		actual_payload = self.instrument.getPayload()
		logger.debug("actual_payload = %s" % actual_payload)
		assert (test_payload == actual_payload)

	def test_setPacketLength(self):
		for length in self.TEST_LENGTHS:
			yield self.check_setPacketLength, length

	def check_setPacketLength(self, test_length):
		self.instrument.setPacketLength(test_length)
		actual_length = self.instrument.getPacketLength()
		logger.debug("actual_length = %s" % actual_length)
		assert (test_length == actual_length)

	def test_setPattern(self):
		for pattern in self.TEST_PATTERNS:
			yield self.check_setPattern, pattern

	def check_setPattern(self, test_pattern):
		self.instrument.setPattern(test_pattern)
		actual_pattern = self.instrument.getPattern()
		logger.debug("actual_pattern = %s" % actual_pattern)
		assert (test_pattern == actual_pattern)

	def test_setTestTime(self):
		for testtime in self.TEST_TESTTIMES:
			yield self.check_setTestTime, timedelta(seconds=testtime)

	def check_setTestTime(self, test_testtime):
		self.instrument.setTestTime(test_testtime)
		actual_testtime = self.instrument.getTestTime()
		assert (test_testtime == actual_testtime)

	def test_setInterface(self):
		for interface in self.TEST_INTERFACES:
			yield self.check_setInterface, interface

	def check_setInterface(self, test_interface):
		self.instrument.setInterface(test_interface)
		actual_interface = self.instrument.getInterface()
		logger.debug("actual_interface = %s" % actual_interface)
		assert (test_interface == actual_interface)

	def test_resetStats(self):
		self.instrument.resetStats()
		ber_stats = self.instrument.getStats()
		assert (ber_stats['bitErrors'] == 0)
		assert (ber_stats['errorRate'] == 0)
		logger.debug("elapsed time = %r" % ber_stats['elapsedTime'])
		logger.debug("timedelta is: %r" % self.timedelt)
		assert (ber_stats['elapsedTime'] == self.timedelt)

	def test_getStats(self):
		pass

	def test_getSyncLoss(self):
		# Assumes that the input source is from the Fastbit Generator
		# Assumes that the generator is set to Serial, PRBS, PN23
		self.instrument.resetStats()
		lost = self.instrument.getSyncLoss()
		logger.debug("lost = %r" % lost)
		assert (not lost)
		ber_stats = self.instrument.getStats()
		assert (ber_stats['bitErrors'] == 0)
		assert (ber_stats['errorRate'] == 0)
		assert (ber_stats['bitCount'] > 0)
		# Now change the payload to the wrong sequence, and expect errors and sync loss
		self.instrument.setPayload("PN7")
		self.instrument.resetStats()
		lost = self.instrument.getSyncLoss()
		logger.debug("Lost = %r" % lost)
		assert (lost)
		ber_stats = self.instrument.getStats()
		assert (ber_stats['bitErrors'] > 0)
		assert (ber_stats['errorRate'] > 0)
		assert (ber_stats['bitCount'] > 0)
		self.instrument.setPayload("PN23")


if __name__ == '__main__' and __package__ is None:
	
	# Runs each test_ method in order
	unittest.main()
