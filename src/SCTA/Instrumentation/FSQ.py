class FSQ(Demodulator):

	def __init__(self, id="FSQ", type="GPIB", port="25", rm=None, config={}):
        """Constructor.

        ~~~ Valid ranges ~~~
        type:        [GPIB, IP]
        port:        [28 or 192.10.10.10]
        freq:		 [20 Hz, 26.5 GHz]
        """

        super ().__init__(id=id)
        self.comm = Comm(protocol=type, port=port, rm=rm, config=config)
        self.config()
    
    def __del__(self):
        self.close()

    def close(self):
        """
        Closes the connection with the FSQ
        NOTE: YOU MUST CALL THIS AFTER YOU ARE FINISHED WITH THE FSQ

        Input:
            None

        Output:
            None
        """
        self.comm.instrument.close()

    def config(self, type):
        if type=="Spectrum":
            self.reset()
            self.setFrequency(freq)
            self.write("CALC:MARK:FUNC:POW:SEL CPOW")
            self.write("SENS:POW:ACH:BWID:CHAN1 $d" % ((symb*1.2)+symb))
            self.setSpan(symb)
            self.AdjustSetting()
            self.setSweepTime()
            self.AutoLevel()
    	if type=="VSA":
            self.reset()
            self.comm.write("INST:SEL DDEM")
            self.setSymbolRate(rate)
            self.setModulation(mod)
            self.setAlpha(roll)
            self.setSweepTime(1000)
            self.setContinousSweep(True)
        return 0

    def setConstellation(self, mod):
        if mod=="QPSK":
            self.comm.write("SENS:DDEM:FORM QPSK")
            self.comm.write("SENS:DDEM:MAPP 'DVB_S2'")
        if mod=="8PSK":
            self.comm.write("SENS:DDEM:FORM PSK")
            self.comm.write("SENS:DDEM:PSK:NST 8")
            self.comm.write("SENS:DDEM:MAPP 'DVB_S2'")

    def getConstellation(self):
        constellation=self.comm.query("SENS:DDEM:FORM?")
        if constellation="PSK":
            return "8PSK"
        return constellation

    def setSymbolRate(self, rate):
        if self.rate != rate:
            self.comm.write("SENS:DDEM:SRAT %d" % rate)
            super().setSymbolRate(rate)
            return 0

    def getSymbolRate(self):
        rate=float(self.comm.query("SENS:DDEM:SRAT?"))
        return rate

    def setAlpha(self, alpha):
        if self.getAlpha != alpha
        self.comm.write("SENS:DDEM:TFIL:ALPH %d" % (alpha/100))
        return 0


    def getAlpha(self):
        alpha=float(self.comm.write("SENS:DDEM:TFIL:ALPH?"))
        return (alpha*100)

    def setFrequency(self, freq): 
        if self.freq!=freq:
            self.comm.write("SENS:FREQ:CENT %d" % freq)
        return 0

    def setSpan(self, symb, scale=3):
        if self. != 
        self.comm.write("SENS:FREQ:SPAN %d" % (symb*scale))
        return 0

    def getSpan(self):
        span=self.comm.query("SENS:FREQ:SPAN?")
        return span

    def getSpectrumChannelPower(self, freq, symb):
        self.setFrequency(freq)
        self.write("CALC:MARK:FUNC:POW:SEL CPOW")
        self.write("SENS:POW:ACH:BWID:CHAN1 $d" % ((symb*1.2)+symb))
        self.setSpan(symb)
        self.AdjustSetting()
        self.setSweepTime()
        self.AutoLevel()
        

    def setSweepTime(self, time=1):
        self.comm.write("SENS:SWE:TIME %time")
        return 0

    def setAutoLevel(self):
        self.comm.write("SENS:POW:ACH:PRES:RLEV")
        return 0

    def AdjustSetting(self):
        self.comm.write("SENSe:POWer:ACHannel:PRESet CPOW")
        return 0

    def CreateNewWindow(self, type, name):
        if type=="VSA":
            name="VSA"
            self.comm.write("INST:CRE DDEM, '%s'" % name)
        if type=="Spectrum":
            self.comm.write("INST:CRE SANANLYZER, '%s'" % name)
        return 0

    def sweepAverage(self, count):
        self.comm.write("SENS:SWE:COUN:VAL %d" % count)
        return 0

    def getAllMeasurements(self, freq, symb):
        self.setFrequency(freq)
        self.config(VSA)
        self.setContinousSweep(False)
        self.AutoLevel()
        mer=self.comm.query("CALC2:MARK:FUNC:DDEM:STAT:SNR? AVG")
        pwr=self.comm.query("CALC2:MARK:FUNC:DDEM:STAT:MPOWER? AVG")
        phaseerror=self.comm.query("CALC2:MARK:FUNC:DDEM:STAT:PERR? AVG")
        carrierfreqerror=self.com.query("CALC2:MARK:FUNC:DDEM:STAT:CFER? AVG")
        return {
            'mer'=mer
            'power'=pwr
            'phaseerror'=phaseerror
            'carrierfreqerror'=carrierfreqerror
        }

    def getVSAChannelPower(self, freq, symb):
        self.comm.query("INST:SEL DDEM")
        getallMeasurements(freq, symb)
        return getAllMeasurements(power)

    def getMER(self, freq, symb):
        self.comm.query("INST:SEL DDEM")
        getAllMeasurements(freq,symb)
        return getAllMeasurements(mer)

    def getPhaseError(self, freq, symb):
        self.comm.query("INST:SEL DDEM")
        getAllMeasurements(freq,symb)
        return getAllMeasurements(phaseerror)

    def getCarrierFrequencyError(self, freq, symb):
        self.comm.query("INST:SEL DDEM")
        getAllMeasurements(freq, symb)
        return getAllMeasurements(carrierfreqerror)

    def reset():
        self.comm.write("*RST")
        return 0

    def setContinousSweep(self, state):
        if state==True:
            self.comm.write("INIT:CONT ON")
        if state==False:
            self.comm.write("INIT:CONT OFF")
        return 0 




    










