from . import Comm
import logging
import time
from datetime import timedelta

logger = logging.getLogger(__name__)

class Fireberd(object):

	def __init__(self, id="Fireberd", type="GPIB", port="15"):
		"""Constructor.

		~~~ Valid ranges ~~~
		type:        [GPIB, IP]
		port:        [1-32]
		"""
		self.comm = Comm(protocol=type, port=port)
		self.setPayload()

	
	def __del__(self):
		self.close()

	def close(self):
		"""
		Closes the connection with the Fastbit

		Input:
			None

		Output:
			None
		"""
		self.comm.instrument.close()

	def setPayload(self, payload="PN23"):
		"""
		Sets the PRBS to the desired setting as:

		PN15 = PRBS pattern of 2^15-1
		PN20 = PRBS pattern of 2^20-1
		PN23 = PRBS pattern of 2^23-1
		"""
		if payload=="PN15":
			self.comm.write("CONFIG:PATTERN 2^15-1")
		if payload=="PN20":
			self.comm.write("CONFIG:PATTERN 2^20-1")
		if payload=="PN23":
			self.comm.write("CONFIG:PATTERN 2^23-1")


	def getPayload(self):
		"""
		Obtains the payload set on the Fireberd.
		"""
		payload=self.comm.query("CONFIG:PATTERN?")
		payload=payload.replace("CONFIG:PATTERN ", "")
		if payload=="2^15-1":
			return "PN15"
		if payload=="2^20-1":
			return "PN20"
		if payload=="2^23-1":
			return "PN23"

		

	def setTestTime(self, timedelta):
		"""
		Sets the test time in HH:MM:SS
	
		"""
		self.comm.write("CONFIG:TEST_INT %s" % time)

	def getTestTime(self):
		"""
		Queries the test time currently set on the Fireberd.
		"""
		time=self.comm.query("CONFIG:TEST_INT?")
		return time

		

	def getStats(self):

		"""
		This will return the bit errors and bit error rate and elpased time during test.

		"""
		biterrors=int(self.comm.query("RESULT? BIT_ERRS"))
		errorRate=float(self.comm.query("RESULT? AVG_BER"))
		elapsedTime=int(self.comm.query("RESULT? ELAP_SEC"))
		elapsedTime=time.strftime('%H:%M:%S', time.gmtime(elapsedTime))
		return { 
			'bitErrors':biterrors,
			'errorRate':errorRate,
			'elapsedTime':elapsedTime
		}

	def resetStats(self):
		"""
		Resets stats and sets test time back to zero. 
		"""
		self.comm.write("RESULT:RESTART")
		

	def runBert(self):
		"""
		Starts the BER test.
		"""
		self.comm.write("RESULT:RESTART")


	def getSyncLoss(self):
		"""
		Returns True if Sync Loss was obtained (sync loss) and False if test signal is Locked and synced.

		"""
		sync=int(self.comm.query("STATUS:LINE_LOSS?"))
		if (sync&4)==4:
			return True		#Checks if the sync result is 
		return False

	def getGenClkLoss(self):
		"""
		Returns True if Gen Clk loss is triggered.
		"""
		genclk=self.comm.query("STATUS:LINE_LOSS?")
		if (genclk&8)==8:
			return True
		return False
	
