import logging, unittest
from . import BaseTests
from .context import SCTA
from SCTA.System import Mode, LocalOscillator, Transponder
from SCTA.Instrumentation import FSW, SFU
import SCTA.utils.dougStatsKit as myStats

# Setup debug logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class FSW_Test(BaseTests.BaseDemodulatorTest):

	AUX_CLASS = SFU
	AUX_PROTOCOL = 'IP'
	AUX_PORT = '192.168.2.11'
	TEST_CLASS = FSW
	TEST_PROTOCOL = 'IP'
	TEST_PORT = '192.168.10.76' #'192.168.2.10'
	TEST_CONSTELLATION= '8PSK'
	TEST_SYMB = 30e6
	TEST_ROLL = 20
	TEST_FREQ = 1500e6
	TEST_SWEEP = 2
	TEST_AVGS = [10, 100, 1000]
	TEST_WINDOWS = ['VSA', 'Spectrum']

	test_instrument = TEST_CLASS(type=TEST_PROTOCOL, port=TEST_PORT)
	#aux_instrument = AUX_CLASS(type=AUX_PROTOCOL, port=AUX_PORT)

	# def __del__(self):
	# 		self.test_instrument.comm.instrument.close()

	def setUp(self):
		self.test_instrument.setBroadcastStandard("DVB-S2")
		self.test_instrument.setScramblingCode(0)

	def getInstrument(self):
		return self.test_instrument

	def configTestSignal(self):
		txpdr = Transponder(mode=4, freq=974e6, symb=20e6)
		#self.aux_instrument.setTransponder(txpdr)
		#self.aux_instrument.setPower(-50)
		self.test_instrument.setTransponder(txpdr)

	# def test_config(self):
	# 	for window in self.TEST_WINDOWS:
	# 		yield self.check_config, window

	# def check_config(self, window):
	# 	self.test_instrument.config(window)

	# Fail on purpose to see debug output. Verify by inspection that measurement is correct
	def test_getSpectrumChannelPower(self):
		self.test_instrument.configureFor('Spectrum')
		self.configTestSignal()
		power = self.test_instrument.getSpectrumChannelPower()
		logger.debug("Spectrum Channel Power = %f" % power)
		assert False

	# Fail on purpose to see debug output. Verify by inspection that measurement is correct
	def test_getAllMeasurements(self):
		self.test_instrument.configureFor('VSA')
		self.configTestSignal()
		results=self.test_instrument.getAllMeasurements()
		logger.debug("all measurements are: %s" % str(results))
		assert False

	# Fail on purpose to see debug output. Verify by inspection that measurement is correct
	def test_getVSAChannelPower(self):
		self.test_instrument.configureFor('VSA')
		self.configTestSignal()
		power=self.test_instrument.getVSAChannelPower()
		logger.debug("the VSA ch power only is: %f" % power)
		assert False

	# Fail on purpose to see debug output. Verify by inspection that measurement is correct
	def test_getMER(self):
		self.test_instrument.configureFor('VSA')
		self.configTestSignal()
		mer=self.test_instrument.getMER()
		logger.debug("the mer only is: %f" % mer)
		assert False

	# Fail on purpose to see debug output. Verify by inspection that measurement is correct
	def test_getPhaseError(self):
		self.test_instrument.configureFor('VSA')
		self.configTestSignal()
		phase=self.test_instrument.getPhaseError()
		logger.debug("the phase error only is: %f" % phase)
		assert False

	# Fail on purpose to see debug output. Verify by inspection that measurement is correct
	def test_getCarrierFrequencyError(self):
		self.test_instrument.configureFor('VSA')
		self.configTestSignal()
		freqerror=self.test_instrument.getCarrierFrequencyError()
		logger.debug("the frequency error only is: %f" % freqerror)
		assert False

	# Fail on purpose to see debug output. Verify by inspection that measurement is correct
	def test_sweepAverage(self):
		self.test_instrument.configureFor('VSA')
		self.configTestSignal()
		for avg in self.TEST_AVGS:
			yield self.check_sweepAverage, avg

	def check_sweepAverage(self, avg):
		# Take 10 samples of averaged measurements over `avg` samples
		num = 10
		listOfDicts = [self.test_instrument.getAllMeasurements(avg=avg) for i in list(range(num))]
		# Regroup the list of measurement dictionaries into a dictionary of measurement lists
		dictOfLists = {}
		dict1 = listOfDicts[0]
		# initialize empty list for each measurement type
		for key in dict1:
			dictOfLists[key] = []
		# append each measurement to its corresponding list
		for dictionary in listOfDicts:
			for key in dictionary:
				dictOfLists[key].append(dictionary[key])
		# Calculate batch margin of error on 10 measurements
		logger.debug("avg = %d" % avg)
		for measurement in dictOfLists:
				samples = dictOfLists[measurement]
				mean = myStats.sample_mean(samples)
				moe = myStats.MOE(samples)
				logger.debug("\tmeasurement = %s" % measurement)
				logger.debug("\t\tmean = %f" % mean)
				logger.debug("\t\tMOE = %f" % moe)
		assert False

	def test_setSpan(self):
		self.test_instrument.configureFor('Spectrum')
		self.test_instrument.setSpan(self.TEST_SYMB)
		actual_symb=int(self.test_instrument.getSpan())
		assert ((self.TEST_SYMB) == actual_symb)

	def test_setSweepTime(self):
		self.test_instrument.configureFor('Spectrum')
		self.test_instrument.setSweepTime(self.TEST_SWEEP)
		actual_sweep=self.test_instrument.getSweepTime()
		assert (self.TEST_SWEEP == actual_sweep)


