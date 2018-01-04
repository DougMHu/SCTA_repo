# Testing the System Class
from .context import SCTA
from SCTA.DataLogging import LogManager, DataLogger
import json, csv, os
import logging, unittest

# Setup debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DataLogger_Test(object):

	FILENAME = 'DataLogger_Test'
	FORMATS = ['csv', 'CSV', 'json', 'JSON']
	CSV_HEADER = ['index', 'power']
	# Testing flexible use cases
	CSV_SAMPLE = [3, -50.6]
	JSON_SAMPLE = {'index': {'type': 'int', 'units': None, 'value': 3}, 'power': {'type': 'float', 'units': 'dBm', 'value': -50.6}}

	def setUp(self):
		pass

	def tearDown(self):
		filenames = [self.FILENAME + '.' + x for x in self.FORMATS]
		for filename in filenames:
			try:
				os.remove(filename)
			except OSError:
				pass

	def test_push(self):
		for format in self.FORMATS:
			yield self.check_push, self.FILENAME, format

	def check_push(self, filename, format):
		dataLogger = DataLogger(filename, format, self.CSV_HEADER)
		
		if format.lower() == 'csv':
			sample = self.CSV_SAMPLE
		if format.lower() == 'json':
			sample = self.JSON_SAMPLE
		dataLogger.push(sample)
		
		with open(filename + '.' + format, 'r+', encoding='utf-8') as f:
			if format.lower() == 'csv':
				reader = csv.DictReader(f, fieldnames=['timestamp'] + self.CSV_HEADER)
				for row in reader:
					print(row)
					comparison = [key==row[key] for key in row]
					print(comparison)
					same = True
					for value in comparison:
						same = same and value
					if same:
						continue
					for measurement in self.CSV_HEADER:
						print(measurement) 
						typecast = eval(self.JSON_SAMPLE[measurement]['type'])
						csv_measurement = typecast(row[measurement])
						actual_measurement = self.JSON_SAMPLE[measurement]['value']  
						assert (csv_measurement == actual_measurement)

			if format.lower() == 'json':
				json_measurement = json.load(f)
				#json_measurement[0].pop('timestamp', None)
				logger.debug(json_measurement[0])
				logger.debug(self.JSON_SAMPLE)
				assert (json_measurement[0] == self.JSON_SAMPLE)

class LogManager(object):
	pass


if __name__ == '__main__':
	unittest.main()