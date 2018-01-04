from . import Modulator
from .SNMPComm import SNMPComm
import logging
import time, math
from ..System import Mode, Transponder

logger = logging.getLogger(__name__)

class DM240XR(Modulator):

	def __init__(self, id="DM240XR", ip="192.168.10.10", port=161, type="int", community="public"):
		"""
		Creates an DM240XR object, which starts a connection for reading and writing commands to the DM240XR.
	

		Input:
			id: string
			type: string interface type
			port: string interface address

		Output:
			DM240XR object

		~~~ Valid ranges ~~~
		type:        ['GPIB', 'IP']
		port:        ['28' or '192.10.10.10']
		cnr:         [0, 20] dB
		"""
		self.comm = SNMPComm(ip=ip,type=type, port=port, community=community)
		self.type=type
		super().__init__(id=id)

	def setBroadcastStandard(self, bcstd):
		"""
		Sets the broadcast standard

		Input:
			bcstd: string broadcast standard

		Output:
			None
		"""
		# Create dictionary to convert string broadcast standard to integer value
		convert = {
		"DIRECTV": 9,
		"DVBS": 0,
		"DVB-S2": 13
		}

		# Construct SNMP command
		value = convert[bcstd]
		OID = ".1.3.6.1.4.1.2591.1.1.32.0"
		command = OID + " -val:%d" % value

		# Send SNMP command
		self.comm.write(command)
		logger.info("Set broadcast standard: %s" % bcstd)
		super().setBroadcastStandard(bcstd)
	
	def getBroadcastStandard(self):
		"""
		Gets the broadcast standard

		Input:
			None

		Output:
			string broadcast standard
		"""
		# Construct SNMP request
		OID = ".1.3.6.1.4.1.2591.1.1.32.0"
		request = OID

		# Request value
		value = int(self.comm.query(request))
		logger.info("broadcast standard request returned: %r" % value)

		# Convert value to string broadcast standard
		convert = {
		9: "DIRECTV",
		0: "DVBS",
		13: "DVB-S2"
		}
		bcstd = convert[value]
		
		# Return the broadcast standard
		logger.info("Got broadcast standard: %s" % bcstd)
		super().setBroadcastStandard(bcstd)
		return bcstd

	def setConstellation(self, mod):
		"""
		Sets the constellation

		Input:
			mod: string constellation

		Output:
			None
		"""
		# Create dictionary to convert string constellation to integer value
		# Construct SNMP command
		# Send SNMP command
		convert = {
		"QPSK": 0,
		"8PSK": 2
				}

		# Construct SNMP command
		value = convert[mod]
		OID = ".1.3.6.1.4.1.2591.1.1.18.0"
		command = OID + " -val:%d" % value

		# Send SNMP command
		self.comm.write(command)
		logger.info("Set broadcast standard: %s" % mod)
		super().setConstellation(mod)

	def getConstellation(self):
		"""
		Gets the constellation

		Input:
			None

		Output:
			string constellation
		"""
		# Construct SNMP request
		# Request value
		# Convert value to string constellation
		# Return the constellation
		OID = ".1.3.6.1.4.1.2591.1.1.18.0"
		request = OID

		# Request value
		value = int(self.comm.query(request))
		logger.info("contallation request returned: %r" % value)

		# Convert value to string broadcast standard
		convert = {
		0: "QPSK",
		2: "8PSK"
				}
		mod = convert[value]
		
		# Return the broadcast standard
		logger.info("Got constallation: %s" % mod)
		super().setConstellation(mod)
		return mod

	def setCodeRate(self, fec):
		"""
		Sets the code rate

		Input:
			fec: string code rate

		Output:
			None
		"""
		# Create dictionary to convert string code rate to integer value
		convert = {
		"QPSK": 0,
		"8PSK": 2
				}

		# Construct SNMP command
		value = convert[mod]
		OID = ".1.3.6.1.4.1.2591.1.1.18.0"
		command = OID + " -val:%d" % value

		# Send SNMP command
		self.comm.write(command)
		logger.info("Set broadcast standard: %s" % mod)
		super().setConstellation(mod)

	def getCodeRate(self):
		"""
		Gets the code rate

		Input:
			None

		Output:
			string code rate
		"""
		# Construct SNMP request
		# Request value
		# Convert value to string code rate
		# Return the code rate
		return getCodeRate

	def setFrequency(self, freq):
		"""
		Sets the center frequency

		Input:  
			freq: float center frequency

		Output: 
			None
		"""
		# Convert float frequency to integer value
		# Construct SNMP command
		# Send SNMP command
		pass

	def getFrequency(self):
		"""
		Gets the center frequency

		Input:  
			None

		Output: 
			float center frequency
		"""
		# Construct SNMP request
		# Request value
		# Convert value to float frequency
		# Return the frequency
		OID = ".1.3.6.1.4.1.2591.1.1.18.0"
		request = OID

		# Request value
		value = int(self.comm.query(request))
		logger.info("contallation request returned: %r" % value)

		# Convert value to string broadcast standard
		convert = {
		0: "QPSK",
		2: "8PSK"
				}
		mod = convert[value]
		
		# Return the broadcast standard
		logger.info("Got constallation: %s" % mod)
		super().setConstellation(mod)
		return mod
		return None

	def setSymbolRate(self, symb):
		"""
		Sets the symbol rate

		Input:  
			symb: float symbol rate

		Output: 
			None
		"""
		# Convert float symbol rate to integer value
		# Construct SNMP command
		# Send SNMP command
		pass

	def getSymbolRate(self):
		"""
		Gets the symbol rate

		Input:  
			None

		Output: 
			float symbol rate
		"""
		# Construct SNMP request
		# Request value
		# Convert value to float symbol rate
		# Return the symbol rate
		return None

	def setAlpha(self, roll):
		"""
		Sets the roll-off (in percent)

		Input:  
			roll: float roll-off (in percent)

		Output: 
			None
		"""
		# Convert float roll-off to integer value
		# Construct SNMP command
		# Send SNMP command
		pass

	def getAlpha(self):
		"""
		Gets the roll-off (in percent)

		Input:  
			None

		Output: 
			float roll-off (in percent)
		"""	
		# Construct SNMP request
		# Request value
		# Convert value to float roll-off
		# Return the roll-off
		return None

	def setPilots(self, pilots):
		"""
		Sets the pilots-enabled state

		Input:  
			pilots: True or False

		Output: 
			None
		"""
		# Create dictionary to convert boolean pilot symbols state to integer value
		# Construct SNMP command
		# Send SNMP command
		pass

	def getPilots(self):
		"""
		Gets the pilots-enabled state

		Input:  
			None

		Output: 
			True or False
		"""
		# Construct SNMP request
		# Request value
		# Convert value to boolean pilot symbols state
		# Return the pilot symbols
		return None

	def setScramblingCode(self, scramb):
		"""
		Sets the scrambling code

		Input:  
			scramb: integer scrambling code

		Output: 
			None
		"""
		# Create dictionary to convert integer scrambling code to integer value
		# Construct SNMP command
		# Send SNMP command
		pass

	def getScramblingCode(self):
		"""
		Gets the scrambling code

		Input:  
			None

		Output: 
			integer scrambling code
		"""
		# Construct SNMP request
		# Request value
		# Convert value to integer scrambling code
		# Return the scrambling code
		return None

	def setRfEnable(self, state):
		"""
		Sets DM240XR RF output state

		Input:
			state: True or False

		Output:
			None
		"""
		# Create dictionary to convert boolean RF-enabled state to integer value
		# Construct SNMP command
		# Send SNMP command
		pass

	def getRfEnable(self):
		"""
		Gets DM240XR RF output state

		Input:
			None

		Output:
			True or False
		"""
		# Construct SNMP request
		# Request value
		# Convert value to boolean RF-enabled state
		# Return the broadcast standard
		return None

	def setPower(self, power):
		"""
		Sets DM240XR RF output power

		Input:
			power: float power in dBm

		Output:
			None
		"""
		# Convert float power to integer value
		# Construct SNMP command
		# Send SNMP command
		pass

	def getPower(self):
		"""
		Gets DM240XR RF output power

		Input:
			None

		Output:
			float power in dBm
		"""
		# Construct SNMP request
		# Request value
		# Convert value to float power
		# Return the power
		return None