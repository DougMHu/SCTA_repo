from . import Demodulator
from . import Comm
import logging
import time
from .SNMPComm import SNMPComm

# Setup debug logging
logger = logging.getLogger(__name__)

class VTR(Demodulator):

	constellation={
	1: ("DVBS", "QPSK", "1/2"),
	2: ("DVBS", "QPSK", "2/3"),
	3: ("DVBS", "QPSK", "3/4"),
	4: ("DVBS", "QPSK", "5/6"),
	5: ("DVBS", "QPSK", "7/8"),
	43: ("DVB-S2", "QPSK", "1/2"),
	44: ("DVB-S2", "QPSK", "3/5"),
	45: ("DVB-S2", "QPSK", "2/3"),
	46: ("DVB-S2", "QPSK", "3/4"),
	47: ("DVB-S2", "QPSK", "4/5"),
	48: ("DVB-S2", "QPSK", "5/6"),
	49:	("DVB-S2", "QPSK", "8/9"),
	50:	("DVB-S2", "QPSK", "9/10"),
	51:	("DVB-S2", "8PSK", "3/5"),
	52:	("DVB-S2", "8PSK", "2/3"),
	53:	("DVB-S2", "8PSK", "3/4"),
	54:	("DVB-S2", "8PSK", "5/6"),
	55:	("DVB-S2", "8PSK", "8/9"),
	56:	("DVB-S2", "8PSK", "9/10")
	}

	reverse_const={}
	for key in constellation:
		value=constellation[key]
		reverse_const[value]=key

	dataSource={
	3: ("ETHERNET INPUT A"),
	11: ("PN23 INSERT"),
	13: ("PN23 INVERT"),
	14: ("RAMP GENERATOR"),
	15: ("PN15"),
	16: ("PN23 BONDED"),
	17: ("PN23 BONDED INVERT")
	}

	reverse_dataSource={}
	for key in dataSource:
		value=dataSource[key]
		reverse_dataSource[value]=key


	def __init__(self, id="FSW", type="GPIB", port="30", window="VSA"):
		"""
		Creates an FSW object, which starts a connection for reading and writing commands to the FSW.
		With no inputs specified, it assumes the host computer's interface is GPIB at port 30.

		Input:
			id: string
			type: string interface type
			port: string interface address/ port

		Output:
			SFU object

		~~~ Valid ranges ~~~
		type:        ['GPIB', 'IP']
		port:        ['28' or '192.10.10.10']
		"""
		self.comm = Comm(protocol=type, port=port)
		super().__init__(id=id)
		self.configureFor(window)

	def __del__(self):
		self.close()

	def close(self):
		"""
		Closes the connection with the FSW
		NOTE: YOU MUST CALL THIS AFTER YOU ARE FINISHED WITH THE FSW

		Input:
			None

		Output:
			None
		"""
		self.comm.instrument.close()
	

	def setSymbolRate(self, rate):
		"""
        Sets the symbol rate

        Input:  
            symb: float symbol rate

        Output: 
            None
        """
		OID=".1.3.6.1.4.1.9633.28.1.3.1.1.13.0" 
		value=(" -val:%d" % rate)
		code=OID+str(value)
		self.comm.write(code)
		logger.info("Set Symbol Rate: %f MHz" % (freq/1e6))

	def getSymbolRate(self):
		"""
        Gets the symbol rate

        Input:  
            None

        Output: 
            float symbol rate
        """
      
		OID=".1.3.6.1.4.1.9633.28.1.3.1.1.13.0" 
		code=OID
		rate=self.comm.query(code)
		logger.info("Got Symbol Rate: %f MHz" % (rate/1e6))

	def setAlpha(self, alpha):
		OID=".1.3.6.1.4.1.9633.28.1.3.1.1.11.0" 
		value=(" -val:%d"% alpha)
		code=OID+value
		self.comm.write(code)
		logger.info("Set roll-off factor: %f%%" % alpha)

	def getAlpha(self):
		OID=".1.3.6.1.4.1.9633.28.1.3.1.1.11.0" 
		code=OID
		self.comm.query(code)
		logger.info("Got roll-off factor: %f%%" % alpha)

	def setFrequency(self, freq, modNumber):
		OID=".1.3.6.1.4.1.9633.28.1.3.1.4.1.2." 
		value=(" -val:%d" % freq)
		code=OID+str(modNumber)+str(value)
		self.comm.write(code)
		logger.info("Set frequency: %f MHz" % (freq/1e6))

	def getFrequency(self, modNumber):
		ID=".1.3.6.1.4.1.9633.28.1.3.1.4.1.2." 
		code=OID+str(modNumber)
		freq=self.comm.query(code)
		logger.info("Got frequency: %f MHz" % (freq/1e6))
		return freq


	def setScramblingCode(self, scram, modNumber):
		OID=".1.3.6.1.4.1.9633.28.1.3.1.4.1.3." 
		value=(" -val:%d" % scramb)
		code=OID+str(modNumber)+str(value)
		self.comm.write(code)
		logger.info("Set scramling code: %d" % scram)

	def getScramblingCode(self, modNumber):
		OID=".1.3.6.1.4.1.9633.28.1.3.1.4.1.3." 
		code=OID+str(modNumber)
		scram=self.comm.query(code)
		logger.info("Got Scrambling Code: %d " % scram)
		return scram

	def setPilots(self, pilots):
		if pilots is True:
			pil = 2
		else:
			pil = 1	
		OID=".1.3.6.1.4.1.9633.28.1.3.1.1.12.0"
		code=(OID+" -val:%d"% pil)
		self.comm.write(code)
		# super().setPilots(pilots)
		logger.info("Set pilot symbols enabled state: %r" % pilots)

	def getPilots(self):
		OID=".1.3.6.1.4.1.9633.28.1.3.1.1.12.0"
		code=(OID)
		pilots=int(self.comm.query(code))
		logger.info("pilots status returned: %r" % pilots)
		if pilots == 1:
			pilots = False
		if pilots == 2:
			pilots = True
		# super().setPilots(pilots)
		# pilots = super().getPilots()
		logger.info("Got pilot symbols enabled state: %r" % pilots)
		return pilots

	def setBroadcastStandard(self, bcstd, modNumber):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.3.1"
		modcod=int(self.comm.query(OID))
		logger.debug("the modcod is: %d" % modcod)
		bcstd=self.constellation[modcod][0]

	def getBroadcastStandard(self, modNumber):
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.3.1"
		modcod=int(self.comm.query(OID))
		logger.debug("the modcod is: %d" % modcod)
		bcstd=self.constellation[modcod][0]
		return bcstd

	def getConstellationCodeRate(self, modNumber):
		"""
		Returns the constellation and code rate as an ordered pair.

		Input:
			None

		Output:
			ordered pair: (string constellation, string code rate)
		"""
		OID=".1.3.6.1.4.1.9633.24.1.3.1.3.1.3.1"
		if self.getBroadcastStandard(modNumber) == "DVB-S2":
			modcod=int(self.comm.query(OID))
			logger.debug("the modcod is: %d" % modcod)
			bcstd=self.constellation[modcod][0]
			mod=self.constellation[modcod][1]
			logger.debug("the DVB-S2 mod is: %s" % mod)
			fec=self.constellation[modcod][2]
			logger.debug("The DVB-S2 fec is: %s" % fec)
			return (mod, fec)

		if self.getBroadcastStandard(modNumber)=="DVBS":
			print ("DVBS stanard not supported in VTM!!!!")
		if self.getBroadcastStandard(modNumber)=="DIRECTV":
			print ("DIRECTV stanard not supported in VTM!!!!")
		

	def setConstellationCodeRate(self, mod, fec, modNumber):
		"""
		Sets the constellation and code rate simultaneously.
		If the constellation and code rate combination is invalid, it raises an exception.

		Input:
			string mod: constellation
			string fec: code rate
			Valid combinations:
			 (x,y)
					 
		Output:
			None
		"""
		OID=".1.3.6.1.4.1.9633.28.1.3.1.1.10.0"
		if self.getBroadcastStandard(modNumber) == "DVB-S2":
			######## REPLACE THIS WITH YOUR OWN CODE ########        
			value=("DVB-S2", mod, fec)
			logger.info("mod is %r" % mod)
			logger.info("fec is %r" % fec)
			if value in self.reverse_const:
				index=self.reverse_const[value]
				logger.info("setting index to: %r" % index)
				code=(" -val:%d" % index)
				self.comm.write(OID+code)
			else:
				print("Combination not available for DVB-S2")
		if self.getBroadcastStandard(modNumber)=="DVBS":
			raise AttributeError("'VTM' does not support DVBS standard")
		if self.getBroadcastStandard(modNumber)=="DIRECTV":
			raise AttributeError("'VTM' does not support DIRECTV standard")

	def enableReceiver(self, state):
		if state==True:
			state=2
		if state==False:
			state=1

		OID=".1.3.6.1.4.1.9633.28.1.3.1.1.14.0" 
		value=(" -val:%d" % state)
		code=OID+str(value)
		self.comm.write(code)
		logger.info("Set input receiver state: %d" % state)

	def getEnableReceiver(self):
		OID=".1.3.6.1.4.1.9633.28.1.3.1.1.14.0" 
		code=OID
		state=int(self.comm.query(code))
		if state==1:
			state=False
		if state==2:
			state=True
		return state
		logger.info("Set input receiver state: %d" % state)

	def setRFInputPort(self, port):
		OID=".1.3.6.1.4.1.9633.28.1.3.1.1.8.0" 
		value=(" -val:%d" % port)
		code=OID+str(value)
		self.comm.write(code)
		logger.info("Set input Port: %d" % port)

	def getRFInputPort(self):
		OID=".1.3.6.1.4.1.9633.28.1.3.1.1.8.0" 
		code=OID
		port=self.comm.query(code)
		logger.info("Got input Port: %d" % port)

	def getSNR(self, modNumber):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.7.1.2." 
		code=OID+modNumber+str(value)
		snr=float(self.comm.query(code))
		logger.info("Got input SNR: %.2%f" % snr)

	def getPower(self, modNumber):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.7.1.4." 
		code=OID+modNumber+str(value)
		power=float(self.comm.query(code))
		logger.info("Got input power: %.2%f" % power)

	def getDemodLock(self, modNumber):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.7.1.5." 
		code=OID+modNumber+str(value)
		demod=int(self.comm.query(code))
		if demod==1:
			demod=True
		if demod==2:
			demod=False
		logger.info("Got Demod Lock: %r" % demod)
		return demod


	def getTotalPackets(self, modNumber):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.7.1.7." 
		code=OID+modNumber
		packets=int(self.comm.query(code))
		logger.info("Got Packet count: %r" % packets)
		return packets


	def CRCCount(self, modNumber):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.7.1.8." 
		code=OID+modNumber
		crc=int(self.comm.query(code))
		logger.info("Got CRC count: %r" % crc)
		return crc

	def getPacketErrorCount(self, modNumber):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.7.1.10." 
		code=OID+modNumber
		packets=int(self.comm.query(code))
		logger.info("Got Packet Error count: %r" % packets)
		return packets


	def resetCounter(self, reset, modNumber):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.7.1.12.1" 
		value=(" -val:%d" % port)
		code=OID+str(value)
		self.comm.write(code)
		logger.info("Set input Port: %d" % port)


	def getSkew(self):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.1.13.0" 
		code=OID
		skew=int(self.comm.query(code))
		logger.info("Got Skew: %r" % skew)
		return skew

	def getNullPacketCount(self):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.1.15.0" 
		code=OID
		null=int(self.comm.query(code))
		logger.info("Got Null Packet Count: %r" % null)
		return null

	def getBufferOverruns(self):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.1.17.0" 
		code=OID
		overrrun=int(self.comm.query(code))
		logger.info("Got Buffer Overruns: %r" % overrrun)
		return overrrun

	def getCurrentChunkSize(self):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.1.19.0" 
		code=OID
		chunk=int(self.comm.query(code))
		logger.info("Got Chunk Size: %r" % chunk)
		return chunk

	def getBondedSize(self):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.1.19.0" 
		code=OID
		chunk=int(self.comm.query(code))
		logger.info("Got Chunk Size: %r" % chunk)
		return chunk

	def getBondedLock(self):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.1.22.0" 
		code=OID
		lock=int(self.comm.query(code))
		if lock==1:
			lock=True
		if lock==2:
			lock=False
		logger.info("Got Rebonding lock status: %r" % lock)
		return lock

	def getOutputDataRate(self):
		OID=".1.3.6.1.4.1.9633.28.1.3.2.1.24.0" 
		code=OID
		rate=float(self.comm.query(code))
		logger.info("Got Output data Rate: %r" % rate)
		return rate