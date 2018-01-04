
##############################################################
##################### CSV file parsing #######################
##############################################################
import csv

def csv2dict(lines):
	"""Creates a dictionary of keys from header and lists of values from input list of lines"""
	# initialize dictionary of empty lists
	dict_of_lists = {}
	reader = csv.DictReader(lines)
	for key in reader.fieldnames:
		dict_of_lists[key] = []

	# populate lists from row values
	for row in reader:
		for key in row:
			dict_of_lists[key].append(row[key])
	return dict_of_lists

def dict2csv(samples, fieldnames, filename):
	"""Creates a CSV file from the value lists in samples dictionary. The order of keys is provided in fieldnames."""
	
	# Create a copy of samples dictionary
	dictionary = samples.copy()

	# Create CSV file and write header
	with open(filename, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, lineterminator='\n', fieldnames=fieldnames)
		writer.writeheader()
		
		# for the total number of samples in the dictionary
		num_samples = len(dictionary[fieldnames[0]])

		for i in list(range(num_samples)):
			# write row values one at a time
			sample = {}
			for key in fieldnames:
				sample[key] = dictionary[key].pop(0)
			writer.writerow(sample)

def csv2modeDict(filename, typeLookup, label):
	"""Create a dictionary of spec values for each Mode #"""
	# Extract rows from csv into a dictionary
	adict = {}
	with open(filename) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			key = row.pop(label)
			typecast = typeLookup[label]
			adict[typecast(key)] = row
		return adict
	raise Exception

def filterEmptyValues(adict):
	"""Filter out empty spec values for each Mode #"""
	for mode in adict:
		emptyfields = []
		for field in adict[mode]:
			if not adict[mode][field]:
				emptyfields.append(field)
		for field in emptyfields:
			adict[mode].pop(field)

def typecastValues(adict, typeLookup):
	"""Typecast the string values to appropriate type"""
	for mode in adict:
		for field in adict[mode]:
			typecast = typeLookup[field]
			adict[mode][field] = typecast(adict[mode][field])

def importCSV(filename, typeLookup, label):
	"""Import AMC Spec file and return a AMC Spec Lookup Table"""
	# The AMC Spec Lookup Table is implemented as a dictionary
	
	adict = csv2modeDict(filename, typeLookup, label)
	filterEmptyValues(adict)
	typecastValues(adict, typeLookup)
	return adict