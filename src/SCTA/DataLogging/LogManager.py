from .DataLogger import DataLogger
import atexit, os, json, csv
import logging

debugLogger = logging.getLogger(__name__)

class LogManager(object):

	# dictionary of all DataLoggers
	dataLoggers = {}

	@classmethod
	def getLogger(cls, filename, format, csv_header=['timestamp', 'sample']):
		"""If a logger with the given filepath already exists, return the corresponding DataLogger
		Else, creates and returns the new DataLogger."""
		key = filename + '.' + format
		
		if key in cls.dataLoggers:
			return cls.dataLoggers[key]
		
		else:
			dataLogger = DataLogger(filename, format, csv_header)
			cls.dataLoggers[key] = dataLogger
			return dataLogger

	@classmethod
	def getLoggers(cls):
		return cls.dataLoggers

	@classmethod
	def getJSONloggers(cls):
		JSONloggers = []
		for dataLogger in cls.dataLoggers.values():
			if dataLogger.getFileFormat().lower() == 'json':
				JSONloggers.append(dataLogger)
		return JSONloggers