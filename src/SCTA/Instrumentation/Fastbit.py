from . import Comm
import logging
import time
from datetime import timedelta

logger = logging.getLogger(__name__)

class Fastbit(object):

	def __init__(self, id="Fastbit", type="GPIB", port="15"):
		"""Constructor.

		~~~ Valid ranges ~~~
		type:        [GPIB, IP]
		port:        [1-32]
		"""
		self.comm = Comm(protocol=type, port=port)
		self.setInterface("SERIAL")
		self.setPattern("PRBS")
		self.setPayload("PN23")
		self.comm.write("RESULT_MODE TOTAL")
	
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

	def setPacketLength(self, length):
		"""
		Sets the packet length "block len" on the analyzer. Typical 188 for DVB-S2.
		Block lenght options are:
		8
		187
		188
		184
		1000
		"""
		self.comm.write("BLOCK_SIZE %d" % length)

	def getPacketLength(self):
		"""
		Queries the packet length on the Analzer.
		"""
		length=self.comm.query("BLOCK_SIZE?")
		length = length.replace("BLOCK_SIZE ", "")
		return int(length)

	def setTestTime(self, delta):
		"""
		Configures the Fastbit to timed testing.
		Input should be a timedelta object.

		"""
		# time=time.split(":")
		# hh=int(time[0])
		# mm=int(time[1])
		# ss=int(time[2])
		# secs=(ss+60*(mm+60*(hh)))
		logger.debug("time is: %r" % delta)
		secs = delta.total_seconds()
		logger.debug("seconds are: %d" % secs)
		self.comm.write("TEST_TIMED ENABLE")
		self.comm.write("TEST_LENGTH %d" % secs)


	def getTestTime(self):
		"""
		Returns the test time as a time delta object.
		"""
		secs=self.comm.query("TEST_LENGTH?")
		secs = int(secs.replace("TEST_LENGTH ", ""))
		# format_time=time.strftime('%H:%M:%S', time.gmtime("secs"))
		# return format_time
		return timedelta(seconds=secs)


	def setInterface(self, interface="SERIAL"):
		"""
		Sets the analyzer interface to either SERIAL or PARALLEL.
		"""
		if interface=="PARALLEL":
			interface="PARA"
		self.comm.write("AN_INPUT %s" % interface)

	def getInterface(self):
		"""
		Returns the analyzer input interface which is either SERIAL or PARALLEL.
		"""
		interface=self.comm.query("AN_INPUT?")
		interface = interface.replace("AN_INPUT ", "")
		if interface=="PARA":
			interface = "PARALLEL"
		return interface

	def getStats(self):

		"""
		Returns the test statistics for the total time under the test. 
		bitErrors= current bit errors encountered
		errorRate= current bit error rate 
		elapsedtime= Current elapsed test time since test started

		"""
		self.comm.write("RESULT_MODE TOTAL")
		biterrors=self.comm.query("ERROR_COUNT?")
		biterrors=int(biterrors.replace("ERROR_COUNT ",""))
		bitcount=self.comm.query("BIT_COUNT?")
		bitcount=int(bitcount.replace("BIT_COUNT ",""))
		errorRate=self.comm.query("ERROR_RATE?")
		errorRate=float(errorRate.replace("ERROR_RATE ", ""))
		elapsedTime=self.comm.query("ELAPSED_TIME?")
		elapsedTime=elapsedTime.replace("ELAPSED_TIME ", "")
		elapsedTime=elapsedTime.replace('\"', '')
		days_time = elapsedTime.split("-")
		days = int(days_time[0])
		time1 = days_time[1]
		time1=time1.split(":")
		hh=int(time1[0])
		mm=int(time1[1])
		ss=int(time1[2])
		delta = timedelta(days=days, hours=hh, minutes=mm, seconds=ss)
		# elapsedSecs=(ss+60*(mm+60*(hh+24*(days))))

		return { 
			'bitErrors':biterrors,
			'errorRate':errorRate,
			# 'elapsedTime':elapsedSecs
			'elapsedTime':delta,
			'bitCount':bitcount

		}


	def resetStats(self):
		"""
		Resets stats and sets test time back to zero. 
		"""
		self.comm.write("TESTRESTART")
		time.sleep(1)

	def runBert(self):
		"""
		Starts the test. Fastbit analyzer needs to be configured prior to this command.
		"""
		self.comm.write("TEST_RUN RUN")

	def setPattern(self, pattern="PRBS"):
		"""
		Sets the Analyzer input pattern on the Fireberd. Choices are:
		PRBS
		MIX
		WORD

		"""
		self.comm.write("AN_PATTERN %s" % pattern)

	def getPattern(self):
		"""
		Returns the Analyzer input pattern.
		"""
		pattern=self.comm.query("AN_PATTERN?")
		pattern=pattern.replace("AN_PATTERN ", "")
		return pattern

	def setPayload(self, prbs="PN23"):
		"""
		Sets the PRBS pattern to:
		PN7 = PRBS pattern of leng 2^7-1
		PN11 = PRBS pattern of 2^11-1
		PN15 = PRBS pattern of 2^15-1
		PN20 = PRBS pattern of 2^20-1
		PN23 = PRBS pattern of 2^23-1
		"""
		self.comm.write("AN_PRBS %s" % prbs)

	def getPayload(self):
		"""
		Obtains the PRBS pattern the Fastbit is currently set to.

		"""
		prbs=self.comm.query("AN_PRBS?")
		prbs=prbs.replace("AN_PRBS ", "")
		return prbs

	def getSyncLoss(self):
		"""
		Returns true when PRBS sync has been lost and False when sync is acquired.

		"""
		sync=self.comm.query("STAT_SYNC?")

		if sync=="STAT_SYNC OFF":
			return True
		if sync=="STAT_SYNC CURRENT":
			return False
