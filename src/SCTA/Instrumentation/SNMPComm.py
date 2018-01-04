# Comm class behaves differently under simulation
from .ResourceManagers import TelnetResourceManager, TelnetIOError
import logging, time
import sys, os, subprocess

logger = logging.getLogger(__name__)

class SNMPComm(object):

        def __init__(self, ip="192.168.10.1", port=23, community="private", type="int"):
                """Constructor.

                ~~~ Valid ranges ~~~
                ip: String IP address
                port: integer port number

                """
                self.ip = ip
                self.port = port
                self.community = community
                self.type=type
                logger.info("port is %r" % port)
                logger.info("Connected to instrument at ip %s, port %d" % (ip, port))
        
        def write(self, commands):
                shell_command = "C:\SnmpSet.exe -r:%s -v:2 -c:%s -o:%s -tp:int" % (self.ip, self.community, commands)
                proc=subprocess.Popen(shell_command, stdout=subprocess.PIPE, shell=True)
                (out, err)=proc.communicate()
                logger.info("command sent is: %r" % shell_command)
                logger.info("output is: %r" % out)
                #newCommand='"C:\Snmpset.exe -r:%s -o:%s -tp:%s' %(self.ip, commands, self.type)
                time.sleep (2)
                #print ("newcommand = %r" % newCommand)
                #logger.debug("command sent is: %r"% newCommand)
                #command = os.system('"C:\Snmpset.exe -r:%s -o:%s -tp:%s' %(self.ip, commands, self.type))
                #logger.info("Wrote %s" % repr(command))

       
        def query(self, commands):
                proc=subprocess.Popen("C:\SnmpGet.exe -r:%s -v:2 -o:%s" %(self.ip, commands), stdout=subprocess.PIPE, shell=True)
                (out, err)=proc.communicate()
                result={}
                logger.info(out.decode('utf-8'))
                for row in out.decode('utf-8').split("\n"):
                        if '=' in row:
                                key, value=row.split('=')
                                result[key]= value
                        # print (result)
                return result["Value"].strip('\r')
