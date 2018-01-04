# Comm class behaves differently under simulation
from .ResourceManagers import TelnetResourceManager, TelnetIOError
import logging
logger = logging.getLogger(__name__)

class TelnetComm(object):

        def __init__(self, ip, port=23, commands='SCPI', rm=TelnetResourceManager()):
                """Constructor.

                ~~~ Valid ranges ~~~
                ip: String IP address
                port: integer port number

                """
                self.ip = ip
                self.port = port
                self.commands = commands
                self.connection = rm.open_resource(ip, port)
                logger.info("Connected to instrument at ip %s, port %d" % (ip, port))
        
        def write(self, command):
                command = (command + '\n').encode('ascii')
                self.connection.write(command)
                logger.info("Wrote %s" % repr(command))
                if self.commands == "SCPI":
                        self.scpiCompleteOperation()
                        logger.debug("Write operation complete")

        def read(self):
                output = self.connection.read_until(b'\n', timeout=1).decode('ascii')
                output = output.replace('\n', '')
                return output

        def query(self, command):
                command = (command + '\n').encode('ascii')
                self.connection.write(command)
                result = self.read()
                logger.info("Queried %s" % repr(command))
                logger.debug("query result = %s" % result)
                return result

        def scpiCompleteOperation(self):
                """For SCPI commands only! Some commands will take the instrument a long time to run.
                Instead of setting an arbitrarily long timeout, poll the operation complete status until it returns true.
                Similar to the ESR query poll suggested in R&S SFU documentation except at a much higher level.
                Resorted to this instead because ESR poll did not work as documented..."""
                command = '*OPC?'
                command = (command + '\n').encode('ascii')
                self.connection.write(command)
                while True:
                        try:
                                opc = self.read()
                                if opc == '':
                                        logger.debug("OPC timed out. Continue to wait")
                                        continue
                                else:
                                        opc = int(opc)
                        except TelnetIOError as error:
                                logger.debug("Telnet OPC query timed out")
                        else:
                                if opc == 1:
                                        logger.debug("OPC returned 1. Operation Complete")
                                        break
                                else:
                                        logger.debug("OPC returned %d. Operation not complete" % opc)


