from ..Specs import MODCOD_Spec
import logging

logger = logging.getLogger(__name__)

class Mode(object):

    def __init__(self, bcstd='DIRECTV', mod='QPSK', fec='6/7'):
        """
        Creates a Mode object with the input parameters below.
        With no inputs specified, it creates a MODCOD Mode 1 by default.
        
        Input:
            bcstd: string broadcast standard
            mod: string constellation
            fec: string code rate

        Output:
            Mode object

        ~~~~~ Valid Inputs ~~~~~
        bcstd:  "DIRECTV", "DVBS", "DVB-S2"
        mod:    "QPSK", "8PSK"
        fec:    "1/2", "3/5", "2/3", "3/4", "4/5", "5/6", "6/7", "7/8", "8/9", "9/10"
        """
        self.setBroadcastStandard(bcstd)
        self.setConstellation(mod)
        self.setCodeRate(fec)
        logger.debug("Created Mode object: %r" % self)

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

    @classmethod
    def fromMODCOD(cls, index):
        """
        Creates a Mode object corresponding to a MODCOD Mode number

        Input:
            index: integer MODCOD Mode number

        Output:
            Mode object
        """
        bcstd = MODCOD_Spec.getBroadcastStandard(index)
        mod = MODCOD_Spec.getConstellation(index)
        fec = MODCOD_Spec.getCodeRate(index)
        return Mode(bcstd=bcstd, mod=mod, fec=fec)

    @classmethod
    def toMODCOD(cls, inputMode):
        """
        Returns the MODCOD Mode number corresponding to an input Mode object

        Input:
            inputMode: a Mode object

        Output:
            integer MODCOD Mode number, or None if not found
        """
        mode2MODCOD = Mode.buildMode2MODCOD()
        if inputMode in mode2MODCOD:
            return mode2MODCOD[inputMode]
        else:
            return None

    @classmethod
    def buildMode2MODCOD(cls):
        """
        Creates a Lookup table that translates a Mode object to the MODCOD Mode number

        Input:
            None

        Output:
            a dictionary
        """
        mode2MODCOD = {}
        for num in MODCOD_Spec.mode_numbers:
            mode = Mode.fromMODCOD(num)
            mode2MODCOD[mode] = num
        return mode2MODCOD

    def setMode(self, inputMode):
        """
        Sets the parameters to be the same as the input mode's parameters

        Input:
            inputMode: a Mode object

        Output:
            None
        """
        bcstd = inputMode.getBroadcastStandard()
        mod = inputMode.getConstellation()
        fec = inputMode.getCodeRate()
        self.setBroadcastStandard(bcstd)
        self.setConstellation(mod)
        self.setCodeRate(fec)

    def setModeFromMODCOD(self, index):
        """
        Sets the parameters according to a MODCOD Mode number

        Input:
            index: integer MODCOD Mode number

        Output:
            None
        """
        self.setMode(self.fromMODCOD(index))

    def getConstellation(self):
        """
        Gets the constellation

        Input:
            None

        Output:
            string constellation
        """
        constellation = self.mod
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
        self.mod = mod
        logger.debug("Set constellation: %s" % mod)

    def getBroadcastStandard(self):
        """
        Gets the broadcast standard

        Input:
            None

        Output:
            string broadcast standard
        """
        bcstd = self.bcstd
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
        self.bcstd = bcstd
        logger.debug("Set broadcast standard: %s" % bcstd)


    def getCodeRate(self):
        """
        Gets the code rate

        Input:
            None

        Output:
            string code rate
        """
        fec = self.fec
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
        self.fec = fec
        logger.debug("Set code rate: %s" % fec)
