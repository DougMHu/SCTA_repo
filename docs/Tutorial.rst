Getting Started
***************

Prerequisites
  Basic knowledge of how to run python scripts through commandline

I recommend running the interactive Jupyter Notebook tutorials::

   cd SCTA_repo\src\tutorials
   jupyter notebook

.. note:: You need to install ``jupyter`` in your SCTA environment to run the interactive tutorials.

If you are new to scripting in Python, walk through the ``Python-Basics.ipynb`` to get a quick intro to concepts important for using the SCTA libraries.

Walk through the ``SCTA-Basics.ipynb`` to help you start writing a simple automation script.

If you do not have ``jupyter`` installed or do not want an interactive tutorial, there are equivalent tutorials as python scripts in ``SCTA_repo\src\tutorials\``. The ``Python-Basics.py`` script introduces Python programming and ``SCTA-Basics.py`` script introduces the SCTA libraries. You can run the scripts to see the output::

   cd SCTA_repo\src\tutorials
   python SCTA-Basics.py

After walking through the tutorials, browse ``SCTA_repo\src\examples\`` for real examples of automation scripts. You can use these as templates for your own scripts. For example, check out ``NetAnDemo.py`` for a common frequency sweep test.
