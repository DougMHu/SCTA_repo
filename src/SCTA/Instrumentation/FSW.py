from . import Demodulator
from . import Comm
import logging
import time

# Setup debug logging
logger = logging.getLogger(__name__)

class FSW(Demodulator):

	WINDOWS = ['Spectrum', 'VSA']

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
		# self.close()
		pass

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
	
	def configureFor(self, type='VSA'):
		"""
		Configures FSW for either VSA or Spectrum mode.
		WARNING: Overwrites all previous configurations!

		Input:
			type: string 'VSA' or 'Spectrum'

		Output:
			None
		"""
		logger.info("FSW device ID: %s" % (self.comm.query("*IDN?")) )
		self.reset()	# reset all previous configurations
		
		# Spectrum mode already configured by default
		if (type=="Spectrum"):
			self.selectWindow(type)
			self.setConstellation = super().setConstellation
			self.getConstellation = super().getConstellation
			self.setSymbolRate = super().setSymbolRate
			self.getSymbolRate = super().getSymbolRate
			self.getAlpha = super().getAlpha
			self.setAlpha = super().setAlpha
			self.getPower = self.getSpectrumChannelPower

		# Must create a VSA window
		if (type=="VSA"):
			self.createNewWindow(type)
			self.selectWindow(type)
			self.setConstellation = self.setVSAConstellation
			self.getConstellation = self.getVSAConstellation
			self.setSymbolRate = self.setVSASymbolRate
			self.getSymbolRate = self.getVSASymbolRate
			self.getAlpha = self.getVSAAlpha
			self.setAlpha = self.setVSAAlpha
			self.getPower = self.getVSAChannelPower
		logger.info("FSW configuration complete")

	def setVSAConstellation(self, mod):
		"""
        Sets the constellation

        Input:
            mod: string constellation

        Output:
            None
        """
		super().setConstellation(mod)
		self.selectWindow('VSA')
		if mod=="QPSK":
			self.comm.write("SENS:DDEM:FORM QPSK")
			self.comm.write("SENS:DDEM:MAPP 'DVB_S2'")
		if mod=="8PSK":
			self.comm.write("SENS:DDEM:FORM PSK")
			self.comm.write("SENS:DDEM:PSK:NST 8")
			self.comm.write("SENS:DDEM:MAPP 'DVB_S2'")
		logger.info("Set constellation: %s" % mod)

	def getVSAConstellation(self):
		"""
        Gets the constellation

        Input:
            None

        Output:
            string constellation
        """
		self.selectWindow('VSA')
		constellation=self.comm.query("SENS:DDEM:FORM?")
		if constellation=="PSK":
			order=self.comm.query("SENS:DDEM:PSK:NST?")
			if order=="8":
				constellation = "8PSK"
		super().setConstellation(constellation)
		constellation = super().getConstellation()
		logger.info("Got constellation: %s" % constellation)
		return constellation

	def setVSASymbolRate(self, rate):
		"""
        Sets the symbol rate

        Input:  
            symb: float symbol rate

        Output: 
            None
        """
		super().setSymbolRate(rate)
		self.selectWindow('VSA')
		if self.getSymbolRate() != rate:
			self.comm.write("SENS:DDEM:SRAT %d" % rate)
			logger.info("Set symbol rate: %.2f MBaud" % (rate/1e6))

	def getVSASymbolRate(self):
		"""
        Gets the symbol rate

        Input:  
            None

        Output: 
            float symbol rate
        """
		self.selectWindow('VSA')
		rate = float(self.comm.query("SENS:DDEM:SRAT?"))
		super().setSymbolRate(rate)
		rate = super().getSymbolRate()
		logger.info("Got symbol rate: %.2f MBaud" % (rate/1e6))
		return rate

	def setVSAAlpha(self, alpha):
		super().setAlpha(alpha)
		self.selectWindow('VSA')
		if self.getAlpha() != alpha:
			self.comm.write("SENS:DDEM:TFIL:ALPH %.2f" % (alpha/100))
			logger.info("Set roll-off factor: %.2f" % alpha)

	def getVSAAlpha(self):
		self.selectWindow('VSA')
		alpha=float(self.comm.query("SENS:DDEM:TFIL:ALPH?"))*100
		super().setAlpha(alpha)
		alpha = super().getAlpha()
		logger.info("Got roll-off factor: %.2f" % alpha)
		return alpha

	def setFrequency(self, freq):
		super().setFrequency(freq)
		if self.getFrequency() != freq:
			self.comm.write("SENS:FREQ:CENT %.2f" % freq)
			logger.info("Set frequency: %.2f MHz" % (freq/1e6))

	def getFrequency(self):
		freq=float(self.comm.query("SENS:FREQ:CENT?"))
		super().setFrequency(freq)
		freq = super().getFrequency()
		logger.info("Got frequency: %.2f MHz" % (freq/1e6))
		return freq

	def setSpan(self, symb):
		self.selectWindow('Spectrum')
		self.comm.write("SENS:FREQ:SPAN %.2f" % (symb))

		logger.debug("span= %.2f" % (self.getSpan()))

	def getSpan(self):
		self.selectWindow('Spectrum')
		span=float(self.comm.query("SENS:FREQ:SPAN?"))
		return span

	def setPreAmpState(self, state):
		"""
		Sets Pre-amplifier state to on or off

		Input:
			boolean state

		Output:
			None
		"""
		if state:
			state = "ON"
		else:
			state = "OFF"
		self.comm.write("INPut:GAIN:STATe %s\n" % state)
		logger.info("Set Pre-amplifier state to %s" % state)

	def setElectronicAttenuatorState(self, state):
		"""
		Sets Electronic Attenuator state to on or off

		Input:
			boolean state

		Output:
			None
		"""
		if state:
			state = "ON"
		else:
			state = "OFF"
		self.comm.write("INPut:EATT:STATe %s\n" % state)
		logger.info("Set Electronic Attenuator state to %s" % state)

	def setElectronicAttenuatorAuto(self, auto):
		"""
		Sets Electronic Attenuator to automatic or manual.

		Input:
			boolean auto

		Output:
			None
		"""
		if auto:
			auto = "ON"
			message = "Set Electronic Attenuator to automatic"
		else:
			auto = "OFF"
			message = "Set Electronic Attenuator to manual"
		self.comm.write("INPut:EATT:AUTO %s\n" % auto)
		logger.info(message)

	def getSpectrumChannelPower_preamp(self, preamp=False):
		"""
		Gets Channel Power in FSW's Spectrum mode

		Input:
			None
		
		Output:
			float channel power in dBm
		"""
		self.selectWindow("Spectrum")
		symb = super().getSymbolRate()
		alpha=super().getAlpha()
		self.comm.write("CALC:MARK:FUNC:POW:SEL CPOW")
		self.comm.write("SENS:POW:ACH:BWID:CHAN1 %.2f" % (symb*(1+(alpha/100))))
		self.setSpan(symb*3)
		self.setContinousSweep(True)
		self.setDetector("RMS")
		self.adjustSetting()
		self.setSweepTime()
		self.autoLevel()
		# to fix RF Overload bug, force the preamp off and turn on auto electronic attenuator
		# this must be done after Auto Level, because Auto Level will undo electronic attenuator settings
		self.setPreAmpState(preamp)
		self.setElectronicAttenuatorState(True)
		self.setElectronicAttenuatorAuto(True)
		self.setContinousSweep(False)
		pwr = float(self.comm.query("CALC:MARK:FUNC:POW:RES? CPOW"))
		logger.info("Got Spectrum Channel Power: %.2f dBm" % pwr)
		return pwr

	def getSpectrumChannelPower(self):
		power = self.getSpectrumChannelPower_preamp()
		if power < -60:
			power = self.getSpectrumChannelPower_preamp(preamp=True)
		return power

	def setDetector(self, detector="RMS"):
		self.selectWindow('Spectrum')
		self.comm.write("DET %s" % detector)
		return 0

	def setSweepTime(self, time=1):
		self.sweeptime=time
		self.selectWindow('Spectrum')
		self.comm.write("SENS:SWE:TIME %d" % time)

	def getSweepTime(self):
		self.selectWindow('Spectrum')
		#self.comm.write("INST:SEL Spectrum")
		sweep=self.comm.query("SENS:SWE:TIME?")
		return float(sweep)

	def autoLevel(self):
		self.comm.write("SENS:ADJ:LEV")
		

	def adjustSetting(self):
		self.comm.write("SENSe:POWer:ACHannel:PRESet CPOW")

	def createNewWindow(self, type):
		if type=="VSA":
			self.comm.write("INST:CRE DDEM, '%s'" % type)
		if type=="Spectrum":
			self.comm.write("INST:CRE SANANLYZER, '%s'" % type)

	def selectWindow(self, type):
		"""
		Selects the window in which to send all following commands

		Input:
			type: string 'VSA' or 'Spectrum'

		Output:
			None
		"""
		self.comm.write("INST:SEL %s" % type)
		if type == 'VSA':
			# only need freq, symb, const
			# txpdr = self.getTransponder()
			# self.setTransponder(txpdr)
			pass

		if type == 'Spectrum':
			# only need freq
			pass

	def getWindow(self):
		"""
		Gets the FSW's current window

		Input:
			None

		Output:
			string window type
		"""
		return self.comm.query("INST:SEL?")

	def setSweepAverage(self, count):
		self.selectWindow('VSA')
		self.comm.write("SENS:SWE:COUN %d" % count)

	def getSweepAverage(self):
		self.selectWindow('VSA')
		count=self.comm.query("SENS:SWE:COUN?")
		return count

	def getAllMeasurements(self, avg=100):
		"""
		Gets MER, Power, Phase error, and Carrier frequency error in the FSW's VSA mode

		Input:
			None

		Output:
			a python dictionary of 'mer', 'power', 'phaseerror', and 'carrierfreqerror'
		"""
		self.selectWindow('VSA')
		# self.setSymbolRate(symb)
		logger.info("symb = %.2f" % self.getSymbolRate())
		# self.setFrequency(freq)
		self.setSweepAverage(avg)
		self.autoLevel()
		# to fix RF Overload bug, force the preamp off and turn on auto electronic attenuator
		# this must be done after Auto Level, because Auto Level will undo electronic attenuator settings
		self.setPreAmpState(False)
		self.setElectronicAttenuatorState(True)
		self.setElectronicAttenuatorAuto(True)
		self.setContinousSweep(False)
		mer=float(self.comm.query("CALC2:MARK:FUNC:DDEM:STAT:SNR? AVG"))
		pwr=float(self.comm.query("CALC2:MARK:FUNC:DDEM:STAT:MPOWER? AVG"))
		phaseerror=float(self.comm.query("CALC2:MARK:FUNC:DDEM:STAT:PERR? AVG"))
		carrierfreqerror=float(self.comm.query("CALC2:MARK:FUNC:DDEM:STAT:CFER? AVG"))
		measurements = { 
			'mer':mer,
			'power':pwr,
			'phaseerror':phaseerror,
			'carrierfreqerror':carrierfreqerror
		}
		logger.debug("Got All VSA measurements: %r" % measurements)
		return measurements

	def getVSAChannelPower(self, avg=100):
		"""
		Gets a power measurement in FSW's VSA mode
		It simply extracts the 'power' from getAllMeasurements

		Input:
			None

		Output:
			float power in dBm
		"""
		power=self.getAllMeasurements(avg=avg)["power"]
		logger.info("Got VSA Power: %.2f dBm" % power)
		return power

	def getMER(self, avg=100):
		"""
		Gets an MER measurement in FSW's VSA mode
		It simply extracts the 'mer' from getAllMeasurements

		Input:
			None

		Output:
			float MER in dB
		"""
		mer=self.getAllMeasurements(avg=avg)["mer"]
		logger.info("Got VSA MER: %.2f dB" % mer)
		return mer

	def getPhaseError(self, avg=100):
		"""
		Gets an Phase Error measurement in FSW's VSA mode
		It simply extracts the 'phaseerror' from getAllMeasurements

		Input:
			None

		Output:
			float phase error in degrees
		"""
		phase=self.getAllMeasurements(avg=avg)["phaseerror"]
		logger.info("Got VSA Power: %.2f degrees" % phase)
		return phase

	def getCarrierFrequencyError(self, avg=100):
		"""
		Gets an Carrier Frequency Error measurement in FSW's VSA mode
		It simply extracts the 'carrierfreqerror' from getAllMeasurements

		Input:
			None

		Output:
			float carrier frequency error in Hz
		"""
		freqerror=self.getAllMeasurements(avg=avg)["carrierfreqerror"]
		logger.info("Got VSA Power: %.2f MHz" % (freqerror/1e6))
		return freqerror

	def reset(self):
		self.comm.write("*RST")

	def setContinousSweep(self, state):
		if state==True:
			self.comm.write("INIT:CONT ON")
		if state==False:
			self.comm.write("INIT:CONT OFF")
			self.comm.write("INIT:IMM")

	def getSpectrumSNR(self):
		txp=self.getSpectrumChannelPower()
		symb = super().getSymbolRate()
		#self.comm.write("CALC:MARK:FUNC:POW:SEL CPOW")
		self.comm.write("SENS:POW:ACH:BWID:CHAN1 %.2f" % (symb))
		self.setContinousSweep(True)
		self.adjustSetting()
		self.setSweepTime()
		self.autoLevel()
		#time.sleep(self.sweeptime*2)
		self.setContinousSweep(False)
		noise = float(self.comm.query("CALC:MARK:FUNC:POW:RES? CPOW"))
		logger.info("Got Spectrum Noise Channel Power: %.2f dBm" % pwr)
		snr=txp-noise
		return snr

	def getSpectrumChannelPowerNoise_preamp(self, preamp=False):
		"""
		Gets Channel Power in FSW's Spectrum mode

		Input:
			None
		
		Output:
			float channel power in dBm
		"""
		self.selectWindow("Spectrum")
		symb = super().getSymbolRate()
		alpha=super().getAlpha()
		self.comm.write("CALC:MARK:FUNC:POW:SEL CPOW")
		self.comm.write("SENS:POW:ACH:BWID:CHAN1 %.2f" % (symb))
		self.setSpan(symb*3)
		self.setContinousSweep(True)
		self.setDetector("RMS")
		self.adjustSetting()
		self.setSweepTime()
		self.autoLevel()
		# to fix RF Overload bug, force the preamp off and turn on auto electronic attenuator
		# this must be done after Auto Level, because Auto Level will undo electronic attenuator settings
		self.setPreAmpState(preamp)
		self.setElectronicAttenuatorState(True)
		self.setElectronicAttenuatorAuto(True)
		self.setContinousSweep(False)
		pwr = float(self.comm.query("CALC:MARK:FUNC:POW:RES? CPOW"))
		logger.info("Got Spectrum Channel Power: %.2f dBm" % pwr)
		return pwr

	def getSpectrumChannelPowerNoise(self):
		power= self.getSpectrumChannelPowerNoise_preamp()
		if power<=-60:
			power=self.getSpectrumChannelPowerNoise_preamp(preamp=True)
		return power