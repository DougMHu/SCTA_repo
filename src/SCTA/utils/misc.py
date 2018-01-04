import inspect

def dict_float2str(d):
	"""Input: (nested) dictionary with values that are floats
	Output: dictionary where all float values are replaced by strings"""
	adict = {}
	for key, value in d.items():
			if inspect.isclass(value):
					value = str(value)
			if type(value) == dict:
					value = dict_float2str(value)
			adict[key] = value
	return adict

# singleton ensures that there only exists one reference to a class object
def singleton(cls):
	instances = {}
	def getinstance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return getinstance

def ceildiv(a, b):
	"""Performs integer division of a/b, then rounds up"""
	return -(-a // b)

def find_nearest(df, value, value_col="Insertion Loss (dB)", index_col="Frequency (Hz)"):
	"""Given a pandas dataframe, find value corresponding to nearest index"""
	index = (np.abs(df[index_col]-value)).argmin()
	return df[value_col][index]