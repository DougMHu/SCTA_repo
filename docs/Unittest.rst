Unit Testing
************

Makefile
--------

For Windows developers, make commands are stored in ``make.bat``. For Linux developers, make commands are stored in ``Makefile``.

To see available commands run::

   cd SCTA_repo\src
   make help

For example::

   make SFU_Test

will run the SFU unit tests and output debug statements to the prompt, while::

   make SFU_Progress

will output SFU unit test results to a ``SFU_Test-log.txt`` without any debug statements.
