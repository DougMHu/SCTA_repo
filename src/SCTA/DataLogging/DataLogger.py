from ..utils import misc as helper
from datetime import datetime
import json, csv, os
import logging

progressLogger = logging.getLogger(__name__)

class DataLogger(object):
	def __init__(self, filename, format, csv_header=['timestamp', 'sample']):
		"""Creates an output file which you can write samples to.

		Input:
			filename: string filename that can also include a path, e.g. 'data\fsw_log'
			format: string 'csv' or 'json'
			csv_header: list of strings, e.g. ['Frequency (MHz)', 'Power (dBm)']
						csv_header is ignored for JSON formatted files

		Output:
			DataLogger object which you can push samples to

		NOTE: The DataLogger only stores the last sample. All other samples are saved on disk.
		"""
		self.filename = filename
		self.format = format
		self.filepath = filename + '.' + format
		self.csv_header = csv_header[:]
		self.csv_header.insert(0, 'timestamp')
		self.timestamp = None
		self.sample = None
		self.initFile()

	def push(self, sample):
		"""Appends sample to the output file.

		Input:
			sample:
				For CSV files: 	a list of samples, e.g. [974e6, -50.0]
								list length must be equal to the CSV header
				For JSON files: a dictionary, e.g.	{
													'freq': 974e6,
													'pwr': -50.0	
													}

		Output:
			None

		For a csv format, the sample can only be a single measurement.
		For a json format, the sample can be a measurement dictionary.
		"""

		# Timestamp the sample
		timestamp = datetime.now().isoformat()

		# Write the sample to disk
		with open(self.filepath, 'a', newline="\n", encoding="utf-8") as f:

			# if json file, sample should be a dictionary
			if self.format.lower() == 'json':
				sample['timestamp'] = timestamp
				self.writeJSON(f, sample)
			
			# if csv file, sample should be an ordered tuple or list
			if self.format.lower() == 'csv':
				entry = {"timestamp":timestamp}
				self.writeCSV(f, sample, entry)

			# Only update the data structure if successfully wrote to disk
			self.timestamp = timestamp
			self.sample = sample

	def getLastSample(self):
		return self.sample

	def getFilePath(self):
		return self.filepath

	def getFileFormat(self):
		return self.format

	def writeJSON(self, fp, sample):

		# Given the output file pointer, move cursor behind the close bracket (see LogManager)
		fp.seek(0, os.SEEK_END)
		pos = fp.tell() - 1
		if pos > 0:
			fp.seek(pos, os.SEEK_SET)
			fp.truncate()

		# If first sample in the file, format without a comma
		if self.sample is None:
			fp.write('{}]'.format(json.dumps(sample, indent=2)))

		# Else, prepend a comma to format a JSON list
		else:
			fp.write(',\n{}]'.format(json.dumps(sample, indent=2)))

	def writeCSV(self, fp, sample, entry):
		# if there is more than one sample in the list
		if hasattr(sample, '__iter__'):
			for key, value in zip(self.csv_header[1:], sample):
				entry[key] = value

		# otherwise there is only one value to write
		else:
			entry[self.csv_header[-1]] = sample

		writer = csv.DictWriter(fp, fieldnames=self.csv_header)
		writer.writerow(entry)

	def initFile(self):
		"""Instantiates and returns a new DataLogger with the specified filepath, filename, and format"""
		# Preformat the output file for appending json objects
		if self.format.lower() == 'json':
			progressLogger.debug("Recognized json format")
			self.initJSON()

		# Write headers for csv file
		if self.format.lower() == 'csv':
			self.initCSV()

	def initJSON(self):
		with open(self.getFilePath(), 'w') as f:
			progressLogger.debug("Successfully openned file")
			f.write('[]')

	def initCSV(self):
		with open(self.getFilePath(), 'w', newline="\n", encoding="utf-8") as f:
				writer = csv.DictWriter(f, fieldnames=self.csv_header)
				writer.writeheader()