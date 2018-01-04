import logging
logging.SIM = 15
logging.addLevelName(logging.SIM, 'SIM')
logging.basicConfig(level=logging.SIM)