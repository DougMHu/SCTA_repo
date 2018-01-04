# # What is SCTA?

# __SCTA__ stands for:
# 
# __S__atellite, and
# 
# __C__ommunications 
# 
# __T__est 
# 
# __A__utomation.
# 
# It is a Python library for controlling the RF lab equipment and collecting measurements for later analysis. You can use these libraries to write your very own test automation script! Or you can use them to control the equipment real-time, as we will demo in this Jupyter Notebook.

# # Installing the SCTA libraries

# The full installation instructions can be found [here](file://10.23.121.10/amclab_share/SCTA/SCTA_repo/docs/_build/html/Installation.html).
# 
# However, this Jupyter notebook should be running remotely on a computer that already has the SCTA libraries installed. So you can just focus on the fun part :)

# # Importing SCTA libraries

# Import the SCTA libraries the same way you import any other Python library. If you just want to simulate an automation script, simply uncomment the ``import RunAsSimulation`` statement below.
# (For example, if you are not currently connected to any RF test equipment, or if you have not installed PyVISA.)

import SCTA
from SCTA.Simulation import RunAsSimulation


# View the available classes you can import. In this tutorial, we will focus on __``Transponder``__, __``SFU``__, __``FSW``__, and __``DataLogger``__.

import pkgutil
package = SCTA
for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                      prefix=package.__name__+'.',
                                                      onerror=lambda x: None):
    print(modname)


# # Trasponders

# Let's create a new variable of type ``Transponder``:

txp = SCTA.System.Transponder(mode=1)
txp


# As you see above, a ``Transponder`` object stores parameters that are important for tuning to a DirecTV satellite transponder.
# 
# You can change the object's parameters by calling its __set methods__. You can read the object's parameters by calling its __get methods__.


# For example, let's change the transponder frequency (Hz) using the __``setFrequency``__ method:

txp.setFrequency(974e6)


# Then we can read the frequency value using the __``getFrequency``__ method:

txp.getFrequency()


# You can do the same with broadcast standard, constellation, and code rate individually.
# 
# But if you know what AMC Mode number you want, use __``setMode``__ instead:

txp.setMode(12)
print(txp.getBroadcastStandard())
print(txp.getConstellation())
print(txp.getCodeRate())


# # Equipment

# In this tutorial, we will focus on two pieces of lab equipment. Let's create two objects of type __``SFU``__ and __``FSW``__.
# 
# To initialize the SFU and FSW, we specify the ``type`` of connection and the ``port`` number. In this case, the SFU and FSW are connected to our computer via Ethernet with the following IP addresses:

sfu = SCTA.Instrumentation.SFU(type="IP", port="192.168.88.246")
fsw = SCTA.Instrumentation.FSW(type="IP", port="192.168.88.248")


# The SFU and FSW have all of the same set/get methods of Transponder. They even have a __``setTransponder``__ method that configures all the parameters for you in one line!

sfu.setTransponder(txp)
fsw.setTransponder(txp)


# After configuring the SFU transponder parameters, you can use other methods to control the signal generation.
# 
# For example, an SFU object lets you set the output power (dBm) and CNR (dB). If you want to set the CNR, make sure to enable the AWGN beforehand:

sfu.setPower(-45)
sfu.setNoiseState(True)
sfu.setNoiseLevel(10)


# An FSW object lets you measure power (dBm) and MER (dB). It can also measure channel power and CNR through its Spectrum Analyzer mode, but here we show it reading power and MER through its Vector Signal Analyzer mode:

print(fsw.getVSAChannelPower())
print(fsw.getMER())


# Hopefully, the FSW measured power and MER matched the SFU output power and CNR!


# # Logging Data

# To log measurements to a CSV file, we specify the __``filename``__ and __``csv_header``__ that we want to see in the first line:

filename = "tutorial"
csv_header = ['Frequency (Hz)', 'SFU Power (dBm)', 'FSW Power (dBm)']


# We pass these as input to a __``DataLogger``__ object. 
# 
# By creating a DataLogger, it will create a file "tutorial.csv" and write the header in the first line. You can check this by opening the file via the Jupyter file browser.

logger = SCTA.DataLogging.DataLogger(filename=filename, format='csv', csv_header=csv_header)


# Use the __``push``__ method to write new lines to the CSV file for each new sample measurement.
# 
# Every sample should be a list of measurements that correspond to the header you created earlier. For example:

# Measure channel power
freq = fsw.getFrequency()
sfu_pwr = sfu.getPower()
fsw_pwr = fsw.getVSAChannelPower()

# Write list of measurements to CSV file
sample = [freq, sfu_pwr, fsw_pwr]
logger.push(sample)


# You can check that the CSV file should now have a second line containing the measurements we pushed. A timestamp is added automatically.

# # Automating a Test

# Here's a simply __for loop__ that takes power measurements across several frequencies. This forms the foundation of all our autmoation scripts!

low_freq = int(270e6) # start at 270 MHz
hi_freq = int(2130e6) # end at 2130 MHz
step_freq = int(20e6) # in 20 MHz intervals
freqs = list(range(low_freq, hi_freq+1, step_freq)) # create the list of frequencies to sweep

for freq in freqs:
    sfu.setFrequency(freq) # change the SFU center frequency
    fsw.setFrequency(freq) # tune FSW to new center frequency
    fsw_pwr = fsw.getVSAChannelPower() # measure FSW power
    sample = [freq, sfu_pwr, fsw_pwr] # create a list of measurements
    logger.push(sample) # push the sample to CSV file


# Check the CSV file to see if the measurements make sense!

# # Congratulations!
# 
# You are on your way to automating lots of RF tests for us :)
