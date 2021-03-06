from ..System import Transponder
import logging

logger = logging.getLogger(__name__)

class Modulator(Transponder):
	def __init__(self, id="mod"):
		"""
		Creates a Modulator object. Used as a template to inherit from for Modulator equipment.
		It has an attribute for storing the current output power.

		Input:
			id: string

		Output:
			Modulator object
		"""
		super().__init__( id=id)
		self.power = -30

	def getTransponder(self):
		"""
		Gets the current transponder parameters

		Input:
			None

		Output:
			Transponder object
		"""
		mode = self.getMode()
		freq = self.getFrequency()
		symb = self.getSymbolRate()
		roll = self.getAlpha()
		scramb = self.getScramblingCode()
		pilots = self.getPilots()
		# pol = self.getPolarity()
		# LO = self.getLocalOscillator()
		return Transponder(mode=mode, freq=freq, symb=symb, roll=roll, scramb=scramb, pilots=pilots)#, pol=pol, LO=LO)