# Check if user is running a simulation
import logging
logger = logging.getLogger(__name__)
simLevel = logger.getEffectiveLevel()
levelName = logging.getLevelName(simLevel)
if levelName is not 'SIM':
        simLevel = logging.NOTSET
        isSimulation = False
else:
        isSimulation = True