import math
import sys
from scipy.stats import t
from numpy.random import uniform

def log10_for_0plus(x):
	if (x == 0) or ((x > 0) and (x < sys.float_info.min)):
		return math.log10(sys.float_info.min)
	else:
		return math.log10(x)

def sample_mean(samples, log=False):
	"""
	Computes the sample mean, either linear or logarithmic.
	Assumes logarithmic samples are in dB-equivalent units,
		i.e. 10*log10(linear unit of power)

	Input:
		list of samples
		Boolean log:
			if True: computes the logarithmic average
			if False: computes the linear average

	Output:
		float sample mean
	"""
	if len(samples) == 0:
		return float('nan')
	if log:
		linSamples = [10**(sample/10) for sample in samples]
		linMean = float(sum(linSamples))/len(linSamples)
		logMean = 10*log10_for_0plus(linMean)
		return logMean
	else:
		return float(sum(samples))/len(samples)

def sample_variance(samples, log=False):
	"""
	Computes the sample variance, either linear or logarithmic.
	Assumes logarithmic samples are in dB-equivalent units,
		i.e. 10*log10(linear unit of power)

	Input:
		list of samples
		Boolean log:
			if True: computes the logarithmic variance
			if False: computes the linear variance

	Output:
		float sample variance
	"""
	if len(samples) < 2:
		return float('nan')
	if log:
		linSamples = [10**(sample/10) for sample in samples]
		linMean = float(sum(linSamples))/len(linSamples)
		linVar = float(sum( [(sample - linMean)**2 for sample in linSamples] ))/(len(linSamples)-1)
		logVar = 10*log10_for_0plus(linVar)
		return logVar
	else:
		return float(sum( [(sample - sample_mean(samples))**2 for sample in samples] ))/(len(samples)-1)

def sample_stdev(samples, log=False):
	"""
	Computes the sample variance, either linear or logarithmic.
	Assumes logarithmic samples are in dB-equivalent units,
		i.e. 10*log10(linear unit of power)

	Input:
		list of samples
		Boolean log:
			if True: computes the logarithmic variance
			if False: computes the linear variance

	Output:
		float sample variance
	"""
	if len(samples) < 2:
		return float('nan')
	if log:
		linSamples = [10**(sample/10) for sample in samples]
		linMean = float(sum(linSamples))/len(linSamples)
		linVar = float(sum( [(sample - linMean)**2 for sample in linSamples] ))/(len(linSamples)-1)
		linStdDev = math.sqrt(linVar)
		logStdDev = 10*log10_for_0plus(linStdDev)
		return logStdDev
	else:
		return math.sqrt( float(sum( [(sample - sample_mean(samples))**2 for sample in samples] ))/(len(samples)-1) )

def MOE(samples, confidence=0.95, log=False):
	"""
	Computes the margin of error on each sample with specified level of confidence.
	Assumes unkown mean, unknown variance, Gaussian distribution.

	Input:
		list of samples
		float confidence (0 < confidence < 1)
		Boolean log:
			if True: computes the logarithmic margin of error
			if False: computes the linear margin of error

	Output:
		float 	
	"""
	if len(samples) < 2:
		return float('nan')
	m = sample_mean(samples, log=log)
	v = sample_variance(samples, log=log)
	if log:
		linMean = 10**(m/10)
		linVar = 10**(v/10)
		linStdDev = math.sqrt(linVar)
		s = linStdDev
		n = len(samples)
		df = n - 1
		one_sided = 1 - (1 - confidence)/2
		crit = t.ppf(one_sided, df)
		e = crit*df*s/math.sqrt(n)
		# report the error in dB, thus calculate the ratio between the average and the average +/- error
		E1 = 10*log10_for_0plus( (linMean + e) / linMean )
		if ((linMean - e) > 0):
			E2 = 10*log10_for_0plus( (linMean - e) / linMean )
			# this logarithmic error is asymmetric, so return the largest of the two sided error
			E = max(E1, E2)
		else:
			E = E1
		return E
	else:
		s = math.sqrt(v)
		n = len(samples)
		df = n - 1
		one_sided = 1 - (1 - confidence)/2
		crit = t.ppf(one_sided, df)
		return crit*df*s/math.sqrt(n)

def MOE_batch_means(samples, log=False):
	"""Assumes unkown mean, unknown variance, unknown distribution.
	Assumes 50 samples. Batches into 5 groups of 10 samples.
	Computes the 95 percent margin of error."""
	if len(samples) == 0:
		return float('nan')
	batchSize = 10
	batches = [samples[i:i+batchSize] for i in range(0, len(samples), batchSize)]
	batchMeans = [sample_mean(batch, log=log) for batch in batches]
	#print batchMeans
	return MOE(batchMeans, log=log)

if __name__ == "__main__":
	# Simulate samples from a Gaussian Distribution
	# x = list(range(10))
	from random import gauss
	mu = 0
	sigma = 0.1
	num = 100
	x = [gauss(mu,sigma) for i in list(range(num))]
	xlog = [10*log10_for_0plus( uniform(mu,sigma) ) for i in list(range(num))]

	# Take the linear mean
	print("\n===========================================================")
	print("Linear Statistics")
	print("===========================================================")
	linMean = sample_mean(x)
	print ("\nLinear Mean = %f" % linMean)

	# Find the linear variance
	linVar = sample_variance(x)
	print("\nLinear Variance = %f" % linVar)

	# Find the linear variance
	linStdDev = sample_stdev(x)
	print("\nLinear Standard Deviation = %f" % linStdDev)

	# Find the 95% confidence Margin of Error
	percent = 0.95
	linMOE = MOE(x, confidence=percent)
	print("\n%.1f%% Confidence Margin of Error = %f" % (percent*100, linMOE))

	# Take the logarithmic mean
	print("\n===========================================================")
	print("Logarithmic (Base 10) Statistics")
	print("===========================================================")
	logMean = sample_mean(xlog, log=True)
	print ("\nLogarithmic Mean = %f" % logMean)

	# Find the logarithmic variance
	logVar = sample_variance(xlog, log=True)
	print("\nLogarithmic Variance = %f" % logVar)

	# Find the logarithmic variance
	logStdDev = sample_stdev(xlog, log=True)
	print("\nLogarithmic Standard Deviation = %f" % logStdDev)

	# Find the 95% confidence Margin of Error
	logMOE = MOE(xlog, confidence=percent, log=True)
	print("\n%.1f%% Confidence Margin of Error = %f" % (percent*100, logMOE))