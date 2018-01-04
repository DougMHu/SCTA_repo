# Comm class behaves differently under simulation
from .ResourceManagers import PyvisaResourceManager, VisaIOError
import logging
logger = logging.getLogger(__name__)

class Comm(object):

        def __init__(self, protocol, port, rm=PyvisaResourceManager(), config={}):
                """Constructor.

                ~~~ Valid ranges ~~~
                protocol: GPIB, serial, IP
                port: String of port of IP address

                """
                self.protocol=protocol
                self.port=port

                # translate into pyvisa port notation
                if protocol == "GPIB":
                        port="GPIB::"+str(port)+"::INSTR"
                if protocol == "IP":
                        port="TCPIP0::"+port+"::INSTR"

                self.instrument=rm.open_resource(port)#, kwargs=config)
                logger.info("Connected to instrument at port %s" % str(port))
                #self.instrument.timeout=2000
        
        def write(self, command):
                self.instrument.write(command)
                logger.info("Wrote %s" % repr(command))
                if (self.protocol == "GPIB") or (self.protocol == "IP"):
                        self.scpiCompleteOperation()
                        logger.debug("Write operation complete")

        def query(self, command):
                result= self.instrument.query(command)
                logger.info("Queried %s" % repr(command))
                logger.debug("query result = %s" % result)
                result= result.replace("\n","")
                return result   

        def scpiCompleteOperation(self):
                """For SCPI commands only! Some commands will take the instrument a long time to run.
                Instead of setting an arbitrarily long timeout, poll the operation complete status until it returns true.
                Similar to the ESR query poll suggested in R&S SFU documentation except at a much higher level.
                Resorted to this instead because ESR poll did not work as documented..."""
                while True:
                        try:
                                opc = int(self.instrument.query("*OPC?"))
                        except VisaIOError as error:
                                if error.abbreviation == "VI_ERROR_TMO":
                                        logger.debug("pyvisa.errors.VisaIOError: %s" % error.description)
                                else:
                                        raise error
                        else:
                                if opc == 1:
                                        break

