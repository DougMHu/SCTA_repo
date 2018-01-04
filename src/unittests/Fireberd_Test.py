import logging, unittest
from .context import SCTA
from SCTA.System import Mode, Transponder
from SCTA.Instrumentation import Fireberd

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class Fireberd_Test(object):

	TEST_CLASS = Fireberd
	TEST_PROTOCOL = 'GPIB'
	TEST_IP='n/a'
	TEST_PORT = '1'
	TEST_PAYLOADS = ["PN15", "PN20", "PN23"]
	TEST_TESTTIMES = ["00:00:05", "00:01:00", "00:05:30"]#, 120, 300]
	TEST_INTERFACES = ['SERIAL', 'PARALLEL']
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

	def test_setTestTime(self):
		for testtime in self.TEST_TESTTIMES:
			yield self.check_setTestTime, testtime

	def check_setTestTime(self, test_testtime):
		self.instrument.setTestTime(test_testtime)
		actual_testtime = self.instrument.getTestTime()
		assert (test_testtime == actual_testtime)
'''
	def test_resetStats(self):
		self.instrument.resetStats()
		ber_stats = self.instrument.getStats()
		assert (ber_stats['bitErrors'] == 0)
		assert (ber_stats['errorRate'] == 0)
		assert (ber_stats['elapsedTime'] == 0)'''

if __name__ == '__main__' and __package__ is None:
	
	# Runs each test_ method in order
	unittest.main()
