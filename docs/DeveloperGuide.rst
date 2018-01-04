Developer's Guide to Maintaining/ Extending SCTA
************************************************

Prerequisites
  We recommend a development environment that includes package control and version control:

    - git_
    - anaconda_
    - You should clone the ``SCTA-dev`` Anaconda environment. Follow :ref:`anaconda-clone-environment-label` tutorial, but use the ``SCTA-dev-environment.yml`` file instead.

  To contribute to the source code, you need a basic understanding of Python packages, debug tools, and test frameworks:

    - import_
    - logging_
    - unittest_
    - nosetests_

  Most importantly, you need **VERY GOOD** documentation practices and naming conventions:

    - docstrings_
    - naming_

Contents
  .. toctree::
     :maxdepth: 2  

     Unittest
     Simulation
     Documentation
     Advice

.. _unittest: https://docs.python.org/3/library/unittest.html#basic-example

.. _nosetests: http://nose.readthedocs.io/en/latest/writing_tests.html#test-generators

.. _import: https://docs.python.org/3/tutorial/modules.html#packages

.. _logging: https://docs.python.org/3.5/howto/logging.html#advanced-logging-tutorial

.. _naming: https://google.github.io/styleguide/pyguide.html?showone=Naming#Naming

.. _docstrings: https://google.github.io/styleguide/pyguide.html?showone=Comments#Comments

.. _git: https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository#Cloning-an-Existing-Repository

.. _anaconda: http://conda.pydata.org/docs/using/using.html