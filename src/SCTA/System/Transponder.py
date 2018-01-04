from . import Mode
import logging

logger = logging.getLogger(__name__)

class Transponder(object):

    def __init__(self, id='txp', mode=None, bcstd='DIRECTV', mod='QPSK', fec='3/4', freq=1074e6, symb=20e6, roll=20.0, scramb=0, pilots=True, pol=None, LO=None):
        """
        Creates a Transponder object with the input parameters below.
        If mode number is specified, the transponder broadcast standard, constellation, and code rate will be configured accordingly and input bcstd, mod, and fec will be ignored.
        With no inputs specified, it creates a MODCOD Mode 1 Transponder, 20MB, 20% roll-off, scrambling code 0, pilot symbols on @ 1074 MHz by default.

        Input:
            id: string
            mode: integer mode number
            bcstd: string broadcast standard
            mod: string constellation
            fec: string code rate
            freq: float center frequency
            symb: float symbol rate
            roll: float alpha
            scramb: integer scrambling code
            pilots: boolean pilots enabled
            pol: string polarity
            LO: string Local Oscillator

        Output:
            Transponder object

        ~~~~~ Valid Inputs ~~~~~
        mode:        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19,20, 21, 22, 23, 24
        freq:        float in Hz
        symb:        float in Baud
        roll:        [0, 100] %
        scramb:      [0, 2^18-1]
        pilot:       False, True (off, on)
        pol: "LHCP", "RHCP", "horizontal", "vertical"

        """
        self.id = id # human-readable identifier
        # If mode number is specified, initialize using mode number
        if type(mode) is int:
            num = mode
            self.mode = Mode.fromMODCOD(num)
        # otherwise, initialize individual inputs
        else:
            self.mode = Mode(bcstd, mod, fec)
        self.setFrequency(freq)     # Center frequency
        self.setSymbolRate(symb)    # Symbol rate
        self.setAlpha(roll)         # roll-off
        self.setScramblingCode(scramb)  # Scrambling code
        self.setPilots(pilots)      # Pilot symbols
        # self.setPolarity(pol)       # Antenna polarization
        # self.setLocalOscillator(LO) # Local Oscillator class instance
        logger.debug("Created Transponder object: %r" % self)

    ### Magic Methods used for creating unique sets
    def __repr__(self):
        """String representation of a Mode object is uniquely determined by the object's dictionary."""
        return type(self).__name__ + "(%s)" % (self.__dict__)
    
    def __eq__(self, other):
        """Compare equality between two Mode objects by comparing equality of each dictionary."""
        if isinstance(other, type(self)):
            return (self.__dict__ == other.__dict__)
        else:
            return False
    
    def __ne__(self, other):
        """Compare inequality between two Mode objects by comparing inequality of each dictionary."""
        return (not self.__eq__(other))
    
    def __hash__(self):
        """Mode objects that have different string representations are considered unique."""
        return hash(self.__repr__())

    def setTransponder(self, txpdr):
        """
        Sets this object's parameters to be the same as the input transponder's parameters

        Input:
            txpdr: a Transponder object

        Output:
            None
        """
        # get all parameters from the input transponder
        mode = txpdr.getMode()
        freq = txpdr.getFrequency()
        symb = txpdr.getSymbolRate()
        roll = txpdr.getAlpha()
        scramb = txpdr.getScramblingCode()
        pilots = txpdr.getPilots()
        # pol = txpdr.getPolarity()
        # LO = txpdr.getLocalOscillator()
        self.setMode(mode)
        # set this transponder's parameters to corresponding input parameters
        self.setFrequency(freq)
        self.setSymbolRate(symb)
        self.setAlpha(roll)
        self.setPilots(pilots)
        if self.getBroadcastStandard() == "DVB-S2":
            self.setScramblingCode(scramb)
        # self.setPolarity(pol)
        # self.setLocalOscillator(LO)

    def getMode(self):
        """
        Gets the current mode

        Input:
            None

        Output:
            Either an integer MODCOD Mode Number or a custom Mode Object
        """
        num = Mode.toMODCOD(self.mode)
        if num is None:
            return self.mode
        else:
            return num

        # # if MODCOD Mode Number is specified, return that
        # if type(self.index) is int:
        #     return self.index
        # # otherwise return a custom Mode Object
        # else:
        #     return Mode(bcstd=self.getBroadcastStandard(), mod=self.getConstellation(), fec=self.getCodeRate())

    def setMode(self, mode):
        """
        Sets the current mode

        Input:
            Either an integer MODCOD Mode Number or a custom Mode Object

        Output:
            None
        """
        # If MODCOD mode number is specified, get the corresponding mode object
        if type(mode) is int:
            num = mode
            mode = Mode.fromMODCOD(num)
        self.setBroadcastStandard(mode.getBroadcastStandard())
        self.setConstellation(mode.getConstellation())
        self.setCodeRate(mode.getCodeRate())

    def getConstellation(self):
        """
        Gets the constellation

        Input:
            None

        Output:
            string constellation
        """
        constellation = self.mode.getConstellation()
        logger.debug("Got constellation: %s" % constellation)
        return constellation

    def setConstellation(self, mod):
        """
        Sets the constellation

        Input:
            mod: string constellation

        Output:
            None
        """
        self.mode.setConstellation(mod)
        logger.debug("Set constellation: %s" % mod)

    def getBroadcastStandard(self):
        """
        Gets the broadcast standard

        Input:
            None

        Output:
            string broadcast standard
        """
        bcstd = self.mode.getBroadcastStandard()
        logger.debug("Got broadcast standard: %s" % bcstd)
        return bcstd

    def setBroadcastStandard(self, bcstd):
        """
        Sets the broadcast standard

        Input:
            bcstd: string broadcast standard

        Output:
            None
        """
        self.mode.setBroadcastStandard(bcstd)
        logger.debug("Set broadcast standard: %s" % bcstd)


    def getCodeRate(self):
        """
        Gets the code rate

        Input:
            None

        Output:
            string code rate
        """
        fec = self.mode.getCodeRate()
        logger.debug("Got code rate: %s" % fec)
        return fec

    def setCodeRate(self, fec):
        """
        Sets the code rate

        Input:
            fec: string code rate

        Output:
            None
        """
        self.mode.setCodeRate(fec)
        logger.debug("Set code rate: %s" % fec)

    def getFrequency(self):
        """
        Gets the center frequency

        Input:  
            None

        Output: 
            float center frequency
        """
        frequency = self.freq
        logger.debug("Got frequency: %f MHz" % (frequency/1e6))
        return frequency

    def setFrequency(self, freq):
        """
        Sets the center frequency

        Input:  
            freq: float center frequency

        Output: 
            None
        """
        self.freq = float(freq)
        logger.debug("Set frequency: %f MHz" % (self.freq/1e6))

    def getSymbolRate(self):
        """
        Gets the symbol rate

        Input:  
            None

        Output: 
            float symbol rate
        """
        symbol_rate = self.symb
        logger.debug("Got symbol rate: %f MBaud" % (symbol_rate/1e6))
        return symbol_rate

    def setSymbolRate(self, symb):
        """
        Sets the symbol rate

        Input:  
            symb: float symbol rate

        Output: 
            None
        """
        self.symb = float(symb)
        logger.debug("Set symbol rate: %f MBaud" % (self.symb/1e6))

    def getAlpha(self):
        """
        Gets the roll-off (in percent)

        Input:  
            None

        Output: 
            float roll-off (in percent)
        """
        alpha = self.roll
        logger.debug("Got roll-off factor: %f%%" % alpha)
        return alpha

    def setAlpha(self, roll):
        """
        Sets the roll-off (in percent)

        Input:  
            roll: float roll-off (in percent)

        Output: 
            None
        """
        self.roll = float(roll)
        logger.debug("Set roll-off factor: %f%%" % self.roll)

    def getScramblingCode(self):
        """
        Gets the scrambling code

        Input:  
            None

        Output: 
            integer scrambling code
        """
        scrambling_code = self.scramb
        logger.debug("Got scrambling code: %d" % scrambling_code)
        return scrambling_code

    def setScramblingCode(self, scramb):
        """
        Sets the scrambling code

        Input:  
            scramb: integer scrambling code

        Output: 
            None
        """
        self.scramb = int(scramb)
        logger.debug("Set scrambling code: %d" % self.scramb)

    def getPilots(self):
        """
        Gets the pilots-enabled state

        Input:  
            None

        Output: 
            True or False
        """
        pilots = self.pilots
        logger.debug("Got pilot symbols enabled: %r" % pilots)
        return pilots

    def setPilots(self, pilots):
        """
        Sets the pilots-enabled state

        Input:  
            pilots: True or False

        Output: 
            None
        """
        self.pilots = pilots
        logger.debug("Set pilot symbols enabled: %r" % self.pilots)

    # def getPolarity(self):
    #     """
    #     Gets the polarity at input to LNB

    #     Input:  
    #         None

    #     Output: 
    #         string polarity
    #     """
    #     return self.pol

    # def setPolarity(self, pol):
    #     """
    #     Sets the polarity at input to LNB

    #     Input:  
    #         pol: string polarity

    #     Output: 
    #         None
    #     """
    #     self.pol = str(pol)

    # def getLocalOscillator(self):
    #     """
    #     Gets the Local Oscillator object

    #     Input:  
    #         None

    #     Output: 
    #         Local Oscillator object
    #     """
    #     return self.LO

    # def setLocalOscillator(self, LO):
    #     """
    #     Sets the Local Oscillator object

    #     Input:  
    #         LO: Local Oscillator object

    #     Output: 
    #         None
    #     """
    #     self.LO = LO
