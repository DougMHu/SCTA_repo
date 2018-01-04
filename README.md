# Satellite Communications Test Automation (SCTA)

The Satellite Communications Test Automation (SCTA) libraries form a __general purpose Python API__ for controlling RF test equipment and automating common RF front-end tests. It can be used for receiver __testing__, __monitoring__ and __evaluation__.

Our goal is to build __reusable__, __modular__ code that makes any kind of testing or monitoring _simple to do_ in code that satellite communications engineers can _understand_.

The full documentation can be found [here](http://scta.readthedocs.io/en/latest/index.html).

## Getting Started

These instructions will get you a boiler-plate automation script simulated on your local machine for development and testing purposes. See RF Test Setup for notes on how to run automation scripts on a physical test setup.

### Prerequisites

We expect some familiarity with your computer’s command prompt/ terminal utility.

We recommend that you install Git version control software and the Anaconda package manager for Python 3.

You can install Git by going to their [downloads page](https://git-scm.com/downloads). We also provide a [step-by-step guide](http://scta.readthedocs.io/en/latest/Git.html) for Windows machines.

You can install Anaconda by going to their [downloads page](https://www.anaconda.com/download/). We also provide a [step-by-step guide](http://scta.readthedocs.io/en/latest/Anaconda.html) for Windows machines.

### Installing

Unfortunately, we don't have this library packaged and registered with PyPA yet, so you'll have to download and install our development environment manually. The following steps will guide you through the process, but a more detailed tutorial can be found in our [installation documentation](http://scta.readthedocs.io/en/latest/Anaconda.html#the-easy-way-cloning-our-scta-environment).

First, download the SCTA repository either by downloading it as a ``zip`` file off of the GitHub page, or by cloning the repository.

```
$ cd ~
$ git clone https://github.com/DougMHu/SCTA_repo.git
```

Next, clone our development environment.

```
$ cd SCTA_repo/install/Anaconda3/envs
$ conda env create -f SCTA-dev-environment.yml
```

If you want ``import SCTA`` to work in all your Python scripts, you will need to modify your PYTHONPATH environment variable. One way to do this is to configure Anaconda to modify PYTHONPATH for you every time you activate the environment. To do this, you need to add special batch files to your Anaconda environment directory. A full explanation behind the reasoning can be found [here](https://conda.io/docs/user-guide/tasks/manage-environments.html#saving-environment-variables).

Copy the batch files ``SCTA_repo/install/Anaconda3/etc/conda/activate.d/env_vars`` and ``SCTA_repo/install/Anaconda3/etc/conda/deactivate.d/env_vars`` into Anaconda's SCTA environment directory, e.g. ``~/Anaconda3/envs/SCTA-dev/``. Modify the batch file to use the SCTA source directory, e.g. ``~/SCTA_repo/src/``.

Congratulations! You made it through the most difficult part of installation.

Now try activating the environment and running a demo automation script.

```
$ source activate SCTA-dev
$ cd ~/SCTA_repo/src/examples
$ python NetAnDemo.py
```

### Tutorials

I recommend running the interactive Jupyter Notebook tutorials:

```
$ cd ~/SCTA_repo/src/tutorials
$ jupyter notebook
```

If you are new to scripting in Python, walk through the ``Python-Basics.ipynb`` to get a quick intro to concepts important for using the SCTA libraries.

Walk through the ``SCTA-Basics.ipynb`` to help you start writing a simple automation script.

More information on tutorials can be found [here](http://scta.readthedocs.io/en/latest/Tutorial.html).

## Unit Tests

Yes, this section is about _testing_ the _test_ automation libraries, and how to _automate_ those tests. These test whether set commands sent to the equipment change the equipment settings as expected. This helps us check whether the equipment automation was implemented correctly. This also helps future developers debug equipment libraries as existing equipment is updated or new equipment is developed. The most current test logs for all equipment libraries are stored under ``SCTA_repo/src/unittests/test-progress/``.

### Equipment Unit Tests

Each RF test equipment has its own unit tests to run. A typical unit test runs through hundreds of test cases, exhausting all possible inputs to equipment class methods. Some cases test impossible inputs to check that the method will report failure to execute and raise an exception. It is __important__ to run equipment unit tests as diagnostics when automation seems buggy, __especially after equipment firmware/ software updates__.

For example, try running the SFU unit test.

```
$ cd ~/SCTA_repo/src/unittests
$ make SFU_Test
```

More information about how to modify or create unit tests can be found [here](http://scta.readthedocs.io/en/latest/Unittest.html).

## RF Test Setup

To get more than just a simulation running, you need to setup the necessary VISA drivers and network configurations. Please refer to this [tutorial](http://scta.readthedocs.io/en/latest/Installation.html) to determine whether you have the necessary setup.

### Example Automation Script

Imagine you want to measure the signal-to-noise ratio (SNR) of a satellite transponder generated by a Rhode & Schwarz RF modulator (BTC) across all operating frequencies of a coaxial cable (L-band). Perhaps your lab setup might look like this.

![RF front-end test block diagram](docs/_static/img/sensitivity-setup.png)

Here is an example of an automation script that is very easy to read, understand, and modify for your own custom tests.

```python
# Initialize equipment and output file
mod = BTC()
dut = VTR()
csv = DataLogger("measurements.csv")

# Test DUT on a DVB-S2 MODCOD 13 transponder, i.e. 8PSK 2/3
txpdr = Transponder(mode=13)
mod.setTransponder(txpdr)
dut.setTransponder(txpdr)

# Test performance across L-band frequencies, i.e. 250 - 2150 MHz
Lband = list(range(250e6, 2150e6, 10e6))

# Take SNR measurement at each frequency
for freq in Lband:
   mod.setFrequency(freq)
   dut.setFrequency(freq)
   snr = dut.getSNR()
   csv.push(snr)
```

## Built With

* [sphinx](http://www.sphinx-doc.org/en/stable/) - Used to build the most important part of a project: Documentation
* [PyVISA](https://pyvisa.readthedocs.io/en/stable/index.html) - Equipment Resource Manager, the glue that holds it all together
* [nose](http://nose.readthedocs.io/en/latest/index.html) - Unit Test Automation
* [jupyter](https://jupyter-notebook.readthedocs.io/en/stable/) - Used to create beautiful, interactive tutorials and data visualizations

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Douglas Hu** - *Initial work* - [DougMHu](https://github.com/DougMHu)
* **Jose Luis Perez** - *Initial work* - [joselperez](https://github.com/joselperez)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Jose Luis Perez, RF test automation guru
* Charles Palaganas, for providing the vision and software architecture
* Sarah Trisorus, for her patient guidance in software development
