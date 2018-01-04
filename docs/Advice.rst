Advice from Previous Developers
*******************************

Tips
----

- Update your ``__init__.py`` files whenever you add a new module
- Watch out for those Indent Errors
- Always check your import statements
- Be careful about querying instruments *too quickly*. Remember to always wait for operations to complete (OPC)
- If you see a ``pyvisa`` error about an "invalid resource handle" or "accessing a resource after it is closed", make sure you've implemented the ``__del__()`` function in your instrument class to ``close`` the ``pyvisa`` resource.
- If some data isn't being pushed properly to the DataLogger, check if your csv header and sample are equal length... Don't forget any commas between list entries...
- Be careful when operating on input lists by reference... Sometimes you only need a copy_ of it
- To enable Jupyter Notebook hide_cell extension, see https://github.com/kirbs-/hide_code/issues/23

Wishlist
--------

- Please fix our import statements DDDD:
- Please figure out how to close our pyvisa resources gracefully during our unittests
  - Perhaps create another Manager with a ``__del__`` that closes all of pyvisa ResourceManager's resources


.. _copy: http://stackoverflow.com/questions/8744113/python-list-by-value-not-by-reference