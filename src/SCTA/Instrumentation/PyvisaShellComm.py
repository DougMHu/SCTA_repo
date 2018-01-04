# Comm class behaves differently under simulation
from .ResourceManagers import PyvisaResourceManager, VisaIOError, TelnetResourceManager, TelnetIOError
from ..utils.misc import ceildiv
import logging
logger = logging.getLogger(__name__)

class PyvisaShellComm(object):

        def __init__(self, protocol, port, config={}, prompt="root@jester", cwd="~"):
                """Constructor.

                ~~~ Valid ranges ~~~
                protocol: GPIB, serial, IP
                port: String of port of IP address

                """
                self.protocol=protocol
                self.port=port
                self.prompt = prompt
                self.cwd_prompt = prompt + ":" + cwd + "# "

                # translate into pyvisa port notation
                baud_rate = None
                if protocol == "GPIB":
                        rm=PyvisaResourceManager()
                        port="GPIB::"+str(port)+"::INSTR"
                if protocol == "IP":
                        rm=TelnetResourceManager()
                        port="TCPIP0::"+port+"::INSTR"
                if protocol == "Serial":
                        rm=PyvisaResourceManager()
                        port="ASRL"+str(port)+"::INSTR"
                        if config:
                                baud_rate = config["baud"]

                self.instrument=rm.open_resource(port)#, kwargs=config)
                if baud_rate:
                        self.instrument.baud_rate = baud_rate
                logger.info("Connected to instrument at port %s" % str(port))
                self.instrument.timeout=5000
        
        def query(self, command):
                # write command
                self.instrument.write(command)
                logger.info("Wrote %s" % repr(command))
                # check echo is consistent
                char_width = 80 # default shell width
                # logger.debug("cwd_prompt: %r" % self.cwd_prompt)
                command_length = len(self.cwd_prompt + command)
                num_lines = ceildiv(command_length, char_width) # handles when command length fills the shell width exactly
                # logger.debug("num_lines = %d" % num_lines)
                echo = ""
                while not echo:
                        for i in list(range(num_lines)):
                                echo += self.read_line()
                        if self.prompt in echo:
                                echo = echo.split("# ")[1]
                                # logger.debug("stripped echo: %r" % echo)
                                echo = echo.replace("\r","")
                                echo = echo.replace("\n","")
                command = command.replace("\r","")
                command = command.replace("\n","")
                echo = echo.replace("\r","")
                echo = echo.replace("\n","")
                # logger.debug("command:\n%r" % command)
                # logger.debug("echo:\n%r" % echo)
                assert echo == command
                # read and return the output
                try:
                        logger.info("timeout set to: %f sec" % (float(self.instrument.timeout)/1000))
                        output = self.read_until(self.prompt)
                        # output = output.replace("\r","")
                        # for most one-liner outputs, remove the \n
                        if output:
                                if output[-1] == '\n':
                                        output = output[:-1]
                except VisaIOError as error:
                        output = None
                return output

        def write(self, command):
                # write command must also read output to flush stdout - to do this use self.query
                self.query(command)
                return None

        def write_raw(self, command):
                self.instrument.write(command)

        def read_line(self):
                result = self.instrument.read()
                logger.info("Read %s" % repr(result))
                result = result.replace("\n", "")
                result = result.replace("\r", "")
                return result

        def read_until(self, prompt):
                """For shell commands only. Reads and appends each line to the output until it reaches
                the prompt for next command. Returns the appended output. Raises a timeout error if it
                fails to parse the prompt for next command."""
                output = ""
                command_complete = False
                while not command_complete:
                        try:
                                line = self.read_line()
                        except VisaIOError as error:
                                if error.abbreviation == "VI_ERROR_TMO":
                                        logger.error("Parsing for shell command prompt failed!\noutput = %s" % repr(output))
                                        logger.error("pyvisa.errors.VisaIOError: %s" % error.description)
                                raise error
                        else:
                                if prompt in line:
                                        command_complete = True
                                        logger.debug("Shell command complete")
                                        self.cwd_prompt = line
                                        # logger.debug("cwd_prompt is %r" % line)
                                else:
                                        output += line
                                        output += "\n"
                return output

        def read_all(self):
                while True:
                        try:
                                line = self.read_line()
                        except VisaIOError as error:
                                if error.abbreviation == "VI_ERROR_TMO":
                                        logger.info("pyvisa.errors.VisaIOError: %s" % error.description)
                                        logger.info("finished reading all")
                                        print("finished reading all")
                                        break
                                if error.abbreviation == "VI_ERROR_ASRL_OVERRUN":
                                        logger.info("pyvisa.errors.VisaIOError: %s" % error.description)
                                        logger.info("continue reading until timeout error")
                                        print("overrun: continue reading until timeout error")
                                if error.abbreviation == "VI_ERROR_ASRL_FRAMING":
                                        logger.info("pyvisa.errors.VisaIOError: %s" % error.description)
                                        logger.info("continue reading until timeout error")
                                        print("framing: continue reading until timeout error")
                                else:
                                        raise
                        else:
                                print(line)



