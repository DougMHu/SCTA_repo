Simulating Instruments
**********************

.. warning:: This will not mimic real instrument output by any means. All instrument output will be the ``string`` "1".

Import Simulation Configuration
-------------------------------

Simply add this import statement at the beginning of your automation script.

.. code-block:: python

   from SCTA.Simulation import RunAsSimulation

Run your script. You should notice that each instrument module will print ``logging.INFO`` statements simulating each command sent to the instrument, and each simulated query output received by the instrument.