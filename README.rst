Holodeck
========

Django based simple dashboard system.

Demo Screenshot
---------------

.. image:: https://github.com/downloads/shaunsephton/holodeck/screenie.0.1.0.png

Getting Started
---------------

Environment Setup
~~~~~~~~~~~~~~~~~
Before installing Holodeck it is strongly recommended that you create a sandboxed environment using ``virtualenv`` or the like. To do so go to a path in which you want to create a Holodeck instance and issue the following command::

    $ virtualenv ve

Then activate your virtualenv::

    $ . ve/bin/activate

Now install Holodeck using pip::

    $ pip install holodeck
    
Once installed you should be able to execute the Holodeck CLI using ``holodeck``, i.e::

    $ holodeck
    usage: holodeck [--config=/path/to/settings.py] [command] [options]

By default the CLI looks for a configuration file in the current working path called ``holodeck.conf.py``.

Configuration Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Holodeck allows you to specify settings to tweak it's behaviour for your particular use case. To generate a default settings file use the ``init`` command. ``init`` allows you to specify an alternative path (otherwise it defaults to the current working path)::

    $ holodeck init
    Configuration file created at '/home/bill/holodeck/holodeck.conf.py'

    # or with custom path

    $ holodeck init /etc/holodeck.conf.py
    Configuration file created at '/etc/holodeck.conf.py'

Then you can customize Holodeck and Django settings within the generated file (defaults to ``holodeck.conf.py``), for instance which database engine you want to use.

Creating Database Tables
~~~~~~~~~~~~~~~~~~~~~~~~
Once you are happy with your configration you have to create the various database tables required by Holodeck. Do this using the ``upgrade`` command::

    $ holodeck upgrade

Remember to ensure that the configured database exists as specified in your configuration in case you are not using the default SQLite database.

Running Local Instance 
~~~~~~~~~~~~~~~~~~~~~~
With Holodeck installed and configured you can now fire up a local Holodeck instance using the ``runserver`` command::

    $ holodeck runserver

Then access the instance on `http://localhost:8000 <http://localhost:8000>`_.

Pushing Data
~~~~~~~~~~~~
Python users can use `Photon <http://pypi.python.org/pypi/photon>`_ to push data to Holodeck. Photon includes `examples <https://github.com/shaunsephton/photon/tree/master/photon/examples>`_ you can use as a starting point. 

