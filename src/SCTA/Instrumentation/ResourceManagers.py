from ..Simulation.Parameters import simLevel, isSimulation
from ..utils.misc import singleton
from telnetlib import Telnet
import paramiko
import logging
logger = logging.getLogger(__name__)

# If it is a simulation, do not import pyvisa
try:
	import pyvisa
except ImportError:
	if isSimulation:
		logger.log(simLevel, "In simulation mode, so no need to import pyvisa")
		logger.warning("In simulation mode, equipment will return fake values!")
	else:
		logger.error("PyVISA is not installed. Equipment classes will not work!")
		raise

class RealTelnetResourceManager(object):
	Error = TimeoutError

	def __init__(self):
		self.connections = {}

	def __del__(self):
		for resource in self.connections:
			self.connections[resource].close()

	def open_resource(self, ip, port=23):
		if (ip, port) in self.connections:
			return self.connections[(ip, port)]
		else:
			self.connections[(ip, port)] = Telnet(ip, port=port)
			return self.connections[(ip, port)]

class RealSSHResourceManager(object):
	Error = TimeoutError

	def __init__(self):
		self.connections = {}

	def __del__(self):
		for resource in self.connections:
			self.connections[resource].close()

	def open_resource(self, ip, username, password):
		if ip in self.connections:
			return self.connections[(ip, username, password)]
		else:
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			client.connect(ip, username=username, password=password)
			self.connections[(ip, username, password)] = client
			return self.connections[(ip, username, password)]

class SimulatedTelnetResourceManager:
	Error = IOError
	def open_resource(self, ip, port=23):
		logger.log(simLevel, "Simulating an instrument at ip %s, port %d" % (ip, port))
		return logger

class SimulatedSSHResourceManager:
	Error = IOError
	def open_resource(self, ip, username, password):
		logger.log(simLevel, "Simulating an instrument at %s@%s" % (username,ip))
		return logger

class SimulatedPyvisaResourceManager:
	Error = IOError
	def open_resource(self, port):
		logger.log(simLevel, "Simulating an instrument at port %s" % str(port))
		return logger

# If it is a simulation, return dummy resource managers
if isSimulation:

	# override the pyvisa instrument write and query functions
	def simulate_write(command):
		logger.log(simLevel, "Writing %s" % repr(command))
	def simulate_query(command):
		logger.log(simLevel, "Querying %s" % repr(command))
		return "1"
	def simulate_read():
		logger.log(simLevel, "Read 1")
		return "root@jester:/# 1"
	def simulate_close():
		logger.log(simLevel, "Closing simulated instrument")
	logger.write = simulate_write
	logger.query = simulate_query
	logger.read = simulate_read
	logger.close = simulate_close

	# create our fake pyvisa resource manager and VisaIOError
	PyvisaResourceManager = SimulatedPyvisaResourceManager
	VisaIOError = SimulatedPyvisaResourceManager.Error

	# create our fake telnet resource manager
	TelnetResourceManager = SimulatedTelnetResourceManager
	TelnetIOError = SimulatedTelnetResourceManager.Error

	# create our fake SSH resource manager
	SSHResourceManager = SimulatedSSHResourceManager
	SSHIOError = SimulatedSSHResourceManager.Error
	
else:

	# singleton ensures that there only exists one reference to a resource manager
	PyvisaResourceManager = singleton(pyvisa.ResourceManager)
	VisaIOError = pyvisa.errors.VisaIOError

	# only one reference to Telnet Resource Manager
	TelnetResourceManager = singleton(RealTelnetResourceManager)
	TelnetIOError = RealTelnetResourceManager.Error

	# only one reference to SSH Resource Manager
	SSHResourceManager = singleton(RealSSHResourceManager)
	SSHIOError = RealSSHResourceManager.Error