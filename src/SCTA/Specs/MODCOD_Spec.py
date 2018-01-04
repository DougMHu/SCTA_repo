from ..utils import fileparse as fp
import logging
from os import path

MODCOD_Spec_path = path.join(path.dirname(__file__), 'raw/DVBS2_Spec.csv')

logger = logging.getLogger(__name__)

class MODCOD_Spec(object):
	"""Class Definition
	The MODCOD_Spec class gives users access to all the Specification values through the class get methods.
	It contains a dictionary that stores the C/N Threshold for Quasi-Error Free (QEF) performance for each 
	MODCOD specified in the DVB-S2 Specification (EN 302 307-1). The dictionary is addressed by mode number.
	"""
	#######################
	### Class variables ###
	#######################
	filename = MODCOD_Spec_path
	typeLookup = {
		'Index': int,
		'Mode #': int,
		'Broadcast Standard': str,
		'Modulation': str,
		'Code':	str,
		'Inner Code Rate':	str,
		'Min Symbol Rate': float,
		'Typical Symbol Rate': float,
		'Max Symbol Rate': float,
		'Payload Bits/Symbol': float,
		'Payload Rate': float,
		'QEF': float,
		'C/N for QEF Code Only': float,
		'C/N for QEF Modem B-B': float,
		'P0 for 20MB': float,
		'Pmin for 20MB': float,
		'Delta C/N for 20MB': float,
		'P0 for 30MB': float,
		'Pmin for 30 MB': float,
		'Delta C/N for 30 MB': float
	}
	label = 'Mode #'
	MODCOD_Lookup = fp.importCSV(filename=filename, typeLookup=typeLookup, label=label)
	mode_numbers = MODCOD_Lookup.keys()

	#########################
	### Class Get Methods ###
	#########################
	@classmethod
	def getBroadcastStandard(cls, mode):
		"""Looks up the Broadcast Standard for the specified Mode Number"""
		return cls.MODCOD_Lookup[mode]['Broadcast Standard']

	@classmethod
	def getConstellation(cls, mode):
		"""Looks up the Constellation for the specified Mode Number"""
		return cls.MODCOD_Lookup[mode]['Modulation']

	@classmethod
	def getCodeRate(cls, mode):
		"""Looks up the Code Rate for the specified Mode Number"""
		return cls.MODCOD_Lookup[mode]['Inner Code Rate']

	@classmethod
	def getQEFpoint(cls, mode):
		"""Looks up the BER threshold to be considered QEF for the specified Mode Number"""
		return cls.MODCOD_Lookup[mode]['QEF']

	@classmethod
	def getCNRThreshold(cls, mode):
		"""Looks up the BER threshold to be considered QEF for the specified Mode Number"""
		return cls.MODCOD_Lookup[mode]['C/N for QEF Code Only']
