# Testing the System Class
import logging, unittest
from .context import SCTA
from SCTA.System import Mode, LocalOscillator, Transponder
from SCTA.Specs import AMC_Spec

# Setup debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Mode_Test(object):

	INDICES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24]
	BCSTDS = ["DIRECTV", "DVBS", "DVB-S2"]
	MODS = ["8PSK", "QPSK"]
	FECS = ['1/2', '3/5', '2/3', '3/4', '4/5', '5/6', '6/7', '7/8', '8/9', '9/10']

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_constructor(self):
		for bcstd in self.BCSTDS:
			for mod in self.MODS:
				for fec in self.FECS:
					yield self.check_constructor, bcstd, mod, fec

	def check_constructor(self, test_bcstd, test_mod, test_fec):
		mode = Mode(test_bcstd, test_mod, test_fec)
		bcstd = mode.getBroadcastStandard()
		mod = mode.getConstellation()
		fec = mode.getCodeRate()
		assert (test_bcstd == bcstd)
		assert (test_mod == mod)
		assert (test_fec == fec)

	def test_fromAMC(self):
		for index in self.INDICES:
			yield self.check_fromAMC, index

	def check_fromAMC(self, index):
		mode = Mode.fromAMC(index)
		bcstd = mode.getBroadcastStandard()
		mod = mode.getConstellation()
		fec = mode.getCodeRate()
		bcstd_AMC = AMC_Spec.getBroadcastStandard(index)
		mod_AMC = AMC_Spec.getConstellation(index)
		fec_AMC = AMC_Spec.getCodeRate(index)
		assert (bcstd_AMC == bcstd)
		assert (mod_AMC == mod)
		assert (fec_AMC == fec)

	def test_setMode(self):
		for bcstd in self.BCSTDS:
			for mod in self.MODS:
				for fec in self.FECS:
					mode = Mode(bcstd, mod, fec)
					yield self.check_setMode, mode

	def check_setMode(self, test_mode):
		mode = Mode()
		mode.setMode(test_mode)
		assert (mode == test_mode)

	def test_setModeFromAMC(self):
		for index in self.INDICES:
			yield self.check_setModeFromAMC, index

	def check_setModeFromAMC(self, index):
		mode = Mode()
		mode.setModeFromAMC(index)
		bcstd = mode.getBroadcastStandard()
		mod = mode.getConstellation()
		fec = mode.getCodeRate()
		bcstd_AMC = AMC_Spec.getBroadcastStandard(index)
		mod_AMC = AMC_Spec.getConstellation(index)
		fec_AMC = AMC_Spec.getCodeRate(index)
		assert (bcstd_AMC == bcstd)
		assert (mod_AMC == mod)
		assert (fec_AMC == fec)

class LocalOscillatorTest(unittest.TestCase):

	def setUp(self):
		self.LO = LocalOscillator()

	def tearDown(self):
		pass

	@unittest.skip("UNIMPLEMENTED")
	def test_constructor(self):
		pass

	@unittest.skip("UNIMPLEMENTED")
	def test_getDownconversion(self):
		pass
		
	@unittest.skip("UNIMPLEMENTED")
	def test_getUpconversion(self):
		pass

class Transponder_Test(object):

	INDICES = [16, None]
	BCSTD = 'DIRECTV'
	MOD = 'QPSK'
	FEC = '6/7'
	FREQS = [250.0 + x*100 for x in list(range(20))]	# Checks L-Band frequencies: 250 - 2150
	SYMBS = [20e6, 30e6]
	ROLLS = [20.0, 35.0]
	SCRAMBS = [592]
	PILOTSS = [True, False]

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_constructor(self):
		for index in self.INDICES:
			for freq in self.FREQS:
				for symb in self.SYMBS:
					for roll in self.ROLLS:
						for scramb in self.SCRAMBS:
							for pilots in self.PILOTSS:
								yield self.check_constructor, index, self.BCSTD, self.MOD, self.FEC, freq, symb, roll, scramb, pilots

	def check_constructor(self, test_index, test_bcstd, test_mod, test_fec, test_freq, test_symb, test_roll, test_scramb, test_pilots):
		txpdr = Transponder(mode=test_index, bcstd=test_bcstd, mod=test_mod, fec=test_fec, freq=test_freq, symb=test_symb, roll=test_roll, scramb=test_scramb, pilots=test_pilots)
		index = txpdr.getMode()
		if test_index is None:
			assert (txpdr.getBroadcastStandard() == self.BCSTD)
			assert (txpdr.getConstellation() == self.MOD)
			assert (txpdr.getCodeRate() == self.FEC)
		else:
			assert (index == test_index)
			assert (txpdr.getBroadcastStandard() == AMC_Spec.getBroadcastStandard(index))
			assert (txpdr.getConstellation() == AMC_Spec.getConstellation(index))
			assert (txpdr.getCodeRate() == AMC_Spec.getCodeRate(index))
		freq = txpdr.getFrequency()
		symb = txpdr.getSymbolRate()
		roll = txpdr.getAlpha()
		scramb = txpdr.getScramblingCode()
		pilots = txpdr.getPilots()
		assert (freq == test_freq)
		assert (symb == test_symb)
		assert (roll == test_roll)
		assert (scramb == test_scramb)
		assert (pilots == test_pilots)

	# def test_fromAMC(self):
	# 	bcstd = self.MODE.getBroadcastStandard()
	# 	mod = self.MODE.getConstellation()
	# 	fec = self.MODE.getCodeRate()
	# 	bcstd_AMC = AMC_Spec.getBroadcastStandard(self.INDEX)
	# 	mod_AMC = AMC_Spec.getConstellation(self.INDEX)
	# 	fec_AMC = AMC_Spec.getCodeRate(self.INDEX)
	# 	self.assertEqual(bcstd_AMC, bcstd)
	# 	self.assertEqual(mod_AMC, mod)
	# 	self.assertEqual(fec_AMC, fec)

if __name__ == '__main__':
	unittest.main()