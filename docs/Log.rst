Logging Measurements & Debug Messages
*************************************
This page contains all you need to know about how to log measurements and debug messages in your scripts. It follows the life of a measurement from when you first take it using the `equipment get methods`__ to when you store it in your log file.

.. note:: Typically, logging debug messages is unnecessary unless you are developing low-level functions or need low-level information about equipment state.

.. hint:: For an example of typical measurement logging, jump to `Log Class`_.

Measurement Object
------------------
The output of an equipment get measurement method should always be a Python ``dictionary``. The measurement object stores the measurement value itself along with context about how the measurement was taken.

Attributes:
  - Equipment ID
  - Transponder tuning parameters
  - Measurement ID, e.g. ``snr``, ``pwr``, etc.
  - Measurement value

Here is an example measurement object::

   {
       "timestamp": "2016-09-26T14:30:04",
       "equip_id": "fsw-1",
       "txpdr": {
           "id": "txpdr-1",
           "mode": {
               "bcstd": "DVB-S2",
               "mod": "8psk",
               "fec": "6/7"
           },
           "freq": 974,
           "symb": 20000,
           "roll": 20,
           "scramb": 1000,
           "pilot": "True",
           "pol": "None",
           "LO": "None"
       },
       "meas_id": "snr",
       "meas_val": 9.5
   }

Log Class
---------
The Log Class is an object used to configure what data to store and how to format the output.

Here is an example of typical configuration and use of the Log Class.

.. code-block:: python

   snr_log = Log(filename='FSW_SNR', format='csv')
   measurement = fsw.getMeas()
   snr_meas = measurement['snr']
   snr_log.push(snr_meas)

.. hint:: 

  Try creating a ``Log`` object specific to each equipment, and push measurements of that equipment to its individual ``Log``. That way, you can save different equipment measurements to different files.

There are 2 possible formats for the output log file: CSV and JSON. If ``csv`` is selected, then a list of measurement values and time stamps are stored and written to separate column in a CSV file. If ``json`` is selected, then a list of `Measurement Object`_ s with time stamps are stored in the JSON file format.

.. note:: 

  JSON_ stands for JavaScript Object Notation. It uses JavaScript syntax, but the format is text only. So, it can be read and used as a data format by any programming language. Python ``dictionaries`` lend themselves to JSON formatting due to structure similarities.

Attributes
~~~~~~~~~~
Each Log includes a timestamp for each measurement object.

- List of time stamp
- List of corresponding measurement objects

Methods
~~~~~~~
Constructor
  Description: Configures where the measurements will be written to and what format. If no filename is specified, samples are not written to a file. If a filename is specified and the format is ``csv``, then only the measurement value and timestamp will be written to a CSV file. If a filename is specified and the format is ``json``, then the timestamp will be included in the `Measurement Object`_ and written to a JSON file.

  Inputs: filename and format

  Outputs: instance of the Log Class

Push(sample)
  Description: pushes measurement to the list of samples and writes sample to output file

  Inputs: instance of `Measurement Object`_

  Outputs: Success/ Failure


Class Definition
~~~~~~~~~~~~~~~~

.. code-block:: python

   class Log(object):

       def __init__(self, filename=None, format=None):
           """Constructor.

           ~~~~~ Possibilities ~~~~~
           filename: string with no '.'
           format: 'csv', 'json'

           """
           self.filename = filename
           self.format = format
           self.sample = []
           self.time_stamp = []

Debug Messages
--------------
Error Codes

Debug Class (Parent of all classes to set debug flag and print debug messages)

.. _JSON: http://www.json.org/
.. _getmethods: Equipment.html#demodulator-class
__ getmethods_