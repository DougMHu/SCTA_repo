from .ResourceManagers import SSHResourceManager, SSHIOError
import logging
logger = logging.getLogger(__name__)

class SSHComm(object):

        def __init__(self, ip, username, password, rm=SSHResourceManager()):
                """Constructor.

                ~~~ Valid ranges ~~~
                protocol: GPIB, serial, IP
                port: String of port of IP address

                """
                self.ip=ip
                self.username=username
                self.password=password
                self.instrument=rm.open_resource(ip, username, password)
                logger.info("Connected to instrument at %s@%s" % (username,ip))
                #self.instrument.timeout=2000
        
        def write(self, command, timeout=None):
                self.instrument.exec_command(command, timeout=timeout)
                logger.info("Wrote %s" % repr(command))

        def query(self, command, timeout=None, stream="stdout"):
                result = ""
                while not result:
                        stdin, stdout, stderr = self.instrument.exec_command(command, timeout=timeout)
                        stdout.channel.recv_exit_status()
                        logger.info("Queried %s" % repr(command))
                        
                        if stream == "stdout":
                                outstream = stdout
                        else:
                                outstream = stderr
                        for line in outstream:
                                result += line
                        result = result[:-1]    # remove the newline character
                        #result= result.replace("\n","")
                        logger.info("query result = %r" % result)
                
                return result