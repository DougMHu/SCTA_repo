.. _equipment-classes-label:

Equipment Classes
*****************

Comm Class
----------

The comm class will obtain the protocol to communicate with the instruments (GPIB, IP, serial) and will also pass the resource manager which will be common to all instruments. 

Additional methods will be needed to write and read using this class. 

.. code-block:: python
	
	class Comm(object)

		def __init__(self, protocol, port, config={}, rm)
			"""Constructor.

			~~~ Valid ranges ~~~
			protocol: GPIB, serial, IP
			port: String of port of IP address

			"""
			self.protocol=protocol
			self.port=port

			if protocol=GPIB then
				port=GPIB::'+port+"::'INSTR'
			if protocol = IP then
				port="TCPIP0::"+port+"::INSTR"
			
			self.instrument=rm.open_resource(port, kwargs=config)
			

Usage

.. code-block:: python
	
	comm = Comm_Class("IP","192.0.0.0")
   	mod1 = Modulator(comm)
   	mod2 = Modulator(comm)
   	mod_list = [mod1, mod2]
   	btc = BTC(mod_list)


Modulator Class
---------------

.. code-block:: python

   class Modulator(Transponder):

       def __init__(self, id="mod"):
           """Constructor.
           
           ~~~ Valid ranges ~~~
           ip:		IP address
           power:	[-80, -10] dBm
           freq:	[250, 2150] MHz
           symrate:	[20, 45] MBaud
           pilots:	True, False

           """
           super(Modulator, self).__init__( id=id)
           self.power = -30


SFU Class
~~~~~~~~~

.. warning:: We have found that different SFUs use different commands for Broadcast Standard and Code Rate related functions. We have determined this to be caused by two different firmware versions: **fill in here** and have implemented a solution that works for both. We try our best to fix the bugs we find, but there may be more. If an SFU script is buggy, please contact us. If you are a developer, use the ``VISA Interactive Control`` to verify that the commands the script sends actually changes the settings correctly.

.. code-block:: python

   class SFU(Modulator):

       def __init__(self, id="SFU", type="GPIB", port="28", config={}):
           """Constructor.
           
           
           ~~~ Valid ranges ~~~
           type:	[GPIB, IP]
	   port:	[28 or 192.10.10.10]
	   cnr:		[0, 20] dB
	

           """
           super (SFU, self).__init__(id=id)
           self.comm = Comm(protocol=type, port=port, config=config)
           self.cnr=None


setTransponder(self, transponder)
	Description:
	This will set all the parameters of the transponder to the SFU.
	
	inputs:
	Transponder attributes

	outputs:
	none
	
setBroadcastStandard(self, bcstd)
	Description:
	Sets the desired broadcast standard

	Inputs:
	(bcstd): DVB-S2, DVBS 

	Outupts:
	None

getBroadcastStandard(self):
	Description:
	Queries the current broacast standard set on the SFU.

	Inputs:
	none

	ouputs:
	Returns the broadcast standard as: DVB-S2, DVBS 

setPower(self, double)
	Description:
	This function will set the SFU power level or it can also be set to the power level inherited.
	
	inputs:
	power[double]: power level value in dB.

	outputs:
	(none)

getPower(self)
	Description:
	This function will obtain the current power levelon the SFU.

	inputs:
	(none)

	outputs:
	SFU power

setFrequency(self, double)
	Description:
	This functions will set the SFU frequency in Hz.

	inputs:
	freq(double): Frequency in Hz.

	outputs:
	(none)

getFrequency(self)
	Description:
	This function will obtain the current frequency from the SFU.

	inputs:
	(none)

	outputs: 
	(freq in Hz)

setAlpha(self, double)
	Description:
	This function will set the SFU symbol rate in S/s.

	inputs: 
	symrate(double): Symbol Rate in kS/s.

	outputs:
	(none)

getAlpha(self)
	Description:
	This function will obtain the current symbol rate from the SFU.

	inputs:
	(none)
	outputs:
	(symbol Rate in S/s)

setNoiseLevel(self, double)
	Description: 
	This function will set the CNR level on the SFU, once set, the SFU automatically adjusts its noise level to obtained the input CNR desired. 

	Inputs: 
	noiseLeveldB[double]: value of CNR level in dB. Range 0 - 20 dB.
	
	Ouput: (none)

getNoiseLevel(self)
	Description:
	Queries the current noise level set on the SFU. 

	Inputs:
	none

	outputs:
	returns the noise level in dB.

enableNoise(self, boolean)
	Description:
	This function will enable or disable noise output.

	Inputs:
	Boolean

	Outputs: none


Test code:

>>> import SFU from Equipment_Lib 
>>> sfu = SFU(ip=10.23.121.1)
>>> sfu.setNoise(20)
(0/2) setNoise: method called
(1/2) setNoise: turned on bandwidth coupling
(2/2) setNoise: set CNR level

getNoise(self)
	Description: 
	This function will get the current CNR level on the SFU

	Inputs: 
	(none)
	
	Ouput:
	returns SFU SNR level (double)

setPilots(self, boolean)
	Description:
	Sets the Pilots on when True, pilots off when false.
	inputs:
	(boolean)

	outputs:
	(none)

getPilots(self)
	Description:
	Queries the pilots status
	
	inputs: 
	none

	outputs:
	(boolean) ON:true; OFF;false

setCW(self, boolean)
	Description:
	Enables, disables CW, based on boolean:

	inputs:
	(boolean) True: Modulation off, False, Modulation ON

	outputs:
	None

getCW(self)
	Description:
	Queries instrument whether CW is enabled or disabled

	inputs none

	outputs:
	True; CW enabled, False; CW disabled

setAlpha(self, alpha)
	Description:
	Sets roll off for the modulated signal.

	inputs:
	(int) roll off 20, 30, 35

	outputs:
	none

setPhaseNoise(self, boolean)
	Description:
	Sets Phase noise for Phase Noise Shape 1, magnitude 13

	inputs
	(boolean): Enables or disables phase noise

	outputs:
	none

getPhaseNoise(self)
	Description:
	Determines if Phase Noise is enabled or disabled:

	inputs
	None

	outputs:

setModulation(self, modulation)
	Description:
	Sets the Modulation type on the SFU for the desired tranponder

	inputs
	DVB-S2, DVBS

	outputs:
	none

getModulation(self)
	Description:
	Obtains the current modulation set on the SFU. 

	inputs:
	none

	outputs:
	current modulation set on SFU.

setCodeRate(self, coderate)
	Description:
	Sets the desired code rate on the SFU

	inputs:
	code rate, 2/3, 3/5, 6/7, 1/2, etc..

	outputs:
	none


setScramblingCode(self, scramb)
	Description:
	Sets the scrambling code on the SFU.

	input:
	(int): scrambling code ID

	output:
	none

getScramblingCode(self)
	Description:
	Gets the scrambling code ID from the SFU.

	inputs
	none

	outputs:
	Scrambling code ID

BTC Class
~~~~~~~~~

.. code-block:: python

   class BTC(object):

       def __init__(self, id="BTC", type=GPIB, port=port, numMods=2):
           """Constructor.
           
           
           ~~~ Valid ranges ~~~
           cnr:		[0, 20] dB
           pilots:	True, False

           """
           self.modulator_list = []
           self.id=id
	   self.cnr = 20
           for i in range(numMods):
           		mod=Modulator(id=id+"-output-"+str(i+1)
           		self.modulator_list.append(mod)


getCodeRate(self)
	Description:
	Sets the FEC code rate on the SFU.

	Inputs:
	code rate 1/2, 2/3, 6/7, etc...

	outputs:
	none

setPower(self, pwr, modNumber)
	Description:
	This function will set the BTC power level on the corresponding output.
	inputs:
	pwr (double): power level value in dB.
	modNumber (int): corresponding output port
	outputs:
	(none)

getPower(self, modNumber)
	Description:
	This function will obtain the current power level on the BTC from the output indicated.

	inputs:
	modNumber (int)- corresponding output port

	outputs:
	BTC power from specified port

setFrequency(self, freq, modNumber)
	Description:
	This functions will set the BTC frequency in Hz in the appropriate output port.

	inputs:
	freq (double): Frequency in Hz.
	modNumber (int): specified output port

	outputs:
	(none)

getFrequency(self, modNumber)
	Description:
	This function will obtain the current frequency from the BTC.

	inputs:
	modNumber (int): specified output port 

	outputs: 
	frequency in Hz

setAlpha(self, symb, modNumber)
	Description:
	This function will set the BTC symbol rate in MS/s.

	inputs: 
	symb(double): Symbol Rate in MS/s.
	modNumber (int): specified output port

	outputs:
	(none)

getAlpha(self, modNumber)
	Description:
	This function will obtain the current symbol rate from the BTC on the specified port. 

	inputs:
	modNumber (int): specified output port

	outputs:
	symbol Rate in MS/s from the specified port

setNoise(self, cnr, modNumber)
	Description: 
	This function will set the CNR level on the BTC, once set, the BTC automatically adjusts its noise level to obtained the input CNR desired. 
	Note: this need to set the bandwidth coupling ON to obtain an accurate measurement.

	Inputs: 
	cnr (double): value of CNR level in dB. Range 0 - 25 dB.
	modNumber (int): specified output port

	Ouput: (none)

Test code:

>>> import BTC from Equipment_Lib 
>>> btc = BTC(ip=10.23.121.1)
>>> btc.setNoise(20)
(0/2) setNoise: method called
(1/2) setNoise: turned on bandwidth coupling
(2/2) setNoise: set CNR level

getNoise(self, modNumber)
	Description: 
	This function will get the current CNR level on the BTC

	Inputs: 
	modNumber (int): specifies output port to get noise from. 
	
	Ouput:
	returns BTC SNR level (double)

setPilots(self, boolean, modNumber)
	Description:
	Sets the Pilots on when True, pilots off when false.

	inputs:
	(boolean): True; pilots ON, False; Pilots OFF
	modNumber (int):specifies output port to set pilots status.

	outputs:
	(none)

getPilots(self, modNumber)
	Description:
	Queries the pilots status from the specified port.
	
	inputs: 
	modNumber (int): specifies output port to get pilots status.

	outputs:
	(boolean) ON:true; OFF;false


SLG Class
~~~~~~~~~

.. code-block:: python
	
	class SLG(object):
		def __init__(self, id="SLG", type="IP", port=port, numMods=32)
			"""Constructor.
			
			~~~ Valid ranges ~~~

           

           		"""
           		self.modulator_list = []
           		self.id=id
           		for i in range(numMods):
           			mod=Modulator(id=id+"-output-"+str(i+1)
           			self.modulator_list.append(mod)
            

loadScenario(self, Scen)
	Description:
	Loads the scenario specified
	
	inputs:
	Scen[string]: Scenario name which needs to be available in the SLG

	outputs:
	(none)

setPower(self, power, modNumber)
	Description:
	Description:
	This function will set the SFU power level. 
	inputs:
	power[double]: power level value in dB.

	outputs:
	(none)

getPower(self, modNumber)
	Description:
	This function will obtain the current power levelon the SFU.

	inputs:
	(none)

	outputs:
	SFU power

setFrequency(self, freq, modNumber)
	Description:
	This functions will set the SFU frequency in Hz.

	inputs:
	freq(double): Frequency in Hz
	modNumber (int): specific output port

	outputs:
	(none)

getFrequency(self, modNumber)
	Description:
	This function will obtain the current frequency from the SFU.

	inputs:
	modNumber (int): specific output port

	outputs: 
	(freq in Hz)

setAlpha(self, symb, modNumber)
	Description:
	This function will set the SFU symbol rate in MS/s.

	inputs: 
	symb (double): Symbol Rate in MS/s.
	modNumber (int): specific output port

	outputs:
	(none)

getAlpha(self, modNumber)
	Description:
	This function will obtain the current symbol rate from the SFU.

	inputs:
	modNumber(int): specific output port

	outputs:
	(symbol Rate in S/s)

setPilots(self, boolean, modNumber)
	Description:
	Sets the Pilots on when True, pilots off when false.
	inputs:
	(boolean)
	modNumber (int): specific output port

	outputs:
	(none)

getPilots(self, modNumber)
	Description:
	Queries the pilots status
	
	inputs: 
	modNumber (int): specific output port

	outputs:
	(boolean) ON:true; OFF;false

setAlpha(self, roll, modNumber):
	Description:
	Sets the roll-off value on the specified SLG modulator 

	inputs:
	roll: roll-off value as integer
	modNumber: SLG modulator number to set

	outputs:
	none

getAlpha(self, modNumber):
	Description:
	Obtains thed current modulator roll-off/Alpha value:

	Inputs:
	modNumber: SLG modulator number to query roll-off value set

	outputs:
	returns roll off value on specified modulator output


setScramblingCode(self, scramb, modNumber)
	Description:
	Sets the scrambling code on the device.

	inputs:
	scramb (int): Scrambing code number to set
	modNumber (int): specific output port 

	outputs:
	(none)

getScramblingCode(self, modNumber)
	Description:
	Queries the current scrambling code set on device on the indicated output modulator

	inputs:
	modNumber (int): specific output port


	outputs
	(int) returns the current scrambling code 

setModulatorState(self, boolean, modNumber)
	Description:
	Enables or disables the desired modulator output

	inputs:
	(boolean): True; enable output. False; disable output
	(modNumber): which modulator to turn on/off on the current SLG. 

	outputs:
	none

getModulatorState(self, modNumber)
	Description:
	Queries modulator status on SLG.

	inputs:
	(modNumber) Modulator output to check 

	outputs:
	(boolean): True; modulator is on. False; modulator is off.

selectBand(self, band):
	Description:
	Selects band range based on the following 


Demodulator Class
-----------------

.. code-block:: python

   class Demodulator(Transponder):

       def __init__(self, id):
           """Constructor.
           
           ~~~ Valid ranges ~~~
           id: string

           """
	   super(Demodulator, self).__init__(id=id)


FSW Class
~~~~~~~~~

.. code-block:: python
	
	class FSW(Demodulator)

		def __init__(self, id, protocol, port, config)
			"""Constructor.

			~~~ Valid Ranges ~~~
			protocol: GPIB, ethernet, serial
			freq: [20, 26.5] GHz

			"""
			super (FSW, self).__init__(id=id)
           		self.comm = Comm(protocol=type, port=port, config=config)

config(self, Transponder)
	Description:
	Configures the FSW to measure either Channel Power or MER and power using the Transponder objects.
	
	Inputs:
	(Transponder): Uses the tranponder objects to configure the FSW

	Outputs:
	none

getAllMeasurements(self)
	Description:
	Obtains all measurements from the VSA window. 
	
	inputs:
	(none)

	outputs
	Returns MER, power, phase error, carrier frequency error from VSA. 

getSpectrumChannelPower(self, freq, symrate)
	Description:
	Measures channel power and returns measurement

	inputs:
	(double) frequency
	(double) symrate

	outputs:
	(double) channel power measurement

.. code-block:: python

	FSW.getchpwr(Demodulator)

		setfreq(freq)
		bw=symrate*1.2
		setsymrate(bw)

		#set RBW and VBW
		#set sweep time
		#getmeasurement

		return chpwr


setFrequency(self, freq)
	Description:
	Sets the input frequency in Hz

	inputs:
	(double) frequency

	outputs:
	(none)

getFrequency(self, freq)
	Description:
	obtains the frequency setting for the specified tuner.

	inputs:
	(int): Tuner index

	outputs:
	(double): frequency setting on current tuner


setBroadcastStandard(self)
	Description:
	Obtains the modulation and code rate for the tuner indicated.

	inputs:
	(int): TunerIndex

	outputs:
	(string): tuner modulcation and code rate

setAlpha(self, double)
	Description:
	This function will set the VTR symbol rate in MS/s.

	inputs: 
	(double): Symbol Rate in MS/s.

	outputs:
	(none)

getAlpha(self)
	Description:
	This function will obtain the current symbol rate from the VTR.

	inputs:
	(none)
	outputs:
	(symbol Rate in MS/s)


VTR Class
~~~~~~~~~

.. code-block:: python

   class VTR(Demodulator):

       def __init__(self, comm, power, freq, symrate, pilots):
           """Constructor.
           
           ~~~ Valid ranges ~~~
           comm:	GPIB, ethernet, serial...
           numTuners: number of tuners available
           power:	[-80, -10] dBm
           freq:	[250, 2150] MHz
           symrate:	[20, 45] MBaud
           pilots:	True, False

           """

	   super (VTR, self).__init__(id=id)
           self.comm = Comm(protocol=type, port=port, config=config)


setFrequency(freq, TunerIndex)
	Description:
	Sets the input frequency

	inputs:
	(double) frequency
	(int): Tuner index

	outputs:
	(none)

getFrequency(TunerIndex)
	Description:
	obtains the frequency setting for the specified tuner.

	inputs:
	(int): Tuner index

	outputs:
	(double): frequency setting on current tuner

setPower(pwr, TunerIndex)
	Description:
	Sets the power level on the appropriate tuner.

	inputs:
	(double): frequency
	(int): tuner

getPower(TunerIndex)
	Description:
	Obtains the power level for the appropriate tuner.

	inputs:
	(int): tuner number

getMode(TunerIndex)
	Description:
	Obtains the modulation and code rate for the tuner indicated.

	inputs:
	(int): TunerIndex

	outputs:
	(string): tuner modulcation and code rate

setAlpha(double)
	Description:
	This function will set the VTR symbol rate in MS/s.

	inputs: 
	(double): Symbol Rate in MS/s.

	outputs:
	(none)

getAlpha()
	Description:
	This function will obtain the current symbol rate from the VTR.

	inputs:
	(none)
	outputs:
	(symbol Rate in MS/s)

setPilots(boolean)
	Description:
	Sets the Pilots on when True, pilots off when false.
	inputs:
	(boolean)

	outputs:
	(none)

getPilots()
	Description:
	Queries the pilots status
	
	inputs: 
	none

	outputs:
	(boolean) ON:true; OFF;false

setScramblingCode(int, TunerIndex)
	Description:
	Sets the scrambling code on the device on the desired tuner.

	inputs:
	(int): Scrambing code number to set

	outputs:
	(none)

getScramblingCode(TunerIndex)
	Description:
	Queries the current scrambling code set on device.

	inputs:
	(none)

	outputs
	(int) returns the current scrambling code 	


DM240XR Class
~~~~~~~~~~~~~

.. warning:: This class is not being updated right now!!!

.. code-block:: python

   class DM240(Modulator):

       def __init__(self, ip, power):
           """Constructor.
           
           ~~~ Valid ranges ~~~
           ip:		IP address
           power:	[-80, -10] dBm
           freq:	[250, 2150] MHz
           symrate:	[20, 45] MBaud
           pilots:	True, False

           """
           Modulator.__init__(self, ip, power, freq, symb, pilots)
	   self.power=power

setPower(power)
	Description:
	This function will set the DM240 power level. 
	inputs:
	power[double]: power level value in dB. [0dBm to -20 dBm] 

	outputs:
	(none)

getPower()
	Description:
	This function will obtain the current power level on the DM240.

	inputs:
	(none)

	outputs:
	DM240 power

setFrequency(double)
	Description:
	This functions will set the DM240 frequency in Hz.

	inputs:
	freq(double): Frequency in Hz. [950e6 Hz to 2050e6 Hz]

	outputs:
	(none)

getFrequency()
	Description:
	This function will obtain the current frequency from the DM240.

	inputs:
	(none)

	outputs: 
	(freq in Hz)

setAlpha(double)
	Description:
	This function will set the DM240 symbol rate in S/s.

	inputs: 
	symrate(double): Symbol Rate in S/s.

	outputs:
	(none)

getAlpha()
	Description:
	This function will obtain the current symbol rate from the DM240.

	inputs:
	(none)
	outputs:
	(symbol Rate in MS/s)

setPilots(boolean)
	Description:
	Sets the Pilots on when True, pilots off when false.
	inputs:
	(boolean)

	outputs:
	(none)

getPilots()
	Description:
	Queries the pilots status
	
	inputs: 
	none

	outputs:
	(boolean) ON:true; OFF;false

setScramblingCode(int)
	Description:
	Sets the scrambling code on the device.

	inputs:
	(int): Scrambing code number to set

	outputs:
	(none)

getScramblingCode()
	Description:
	Queries the current scrambling code set on device.

	inputs:
	(none)

	outputs
	(int) returns the current scrambling code 