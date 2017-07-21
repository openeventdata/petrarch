[![Build Status](https://travis-ci.org/openeventdata/petrarch.svg?branch=master)](https://travis-ci.org/openeventdata/petrarch)

PETRARCH
========

[![Join the chat at https://gitter.im/openeventdata/petrarch](https://badges.gitter.im/openeventdata/petrarch.svg)](https://gitter.im/openeventdata/petrarch?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Code for the new Python Engine for Text Resolution And Related Coding Hierarchy (PETRARCH) 
event data coder. The coder now has all of the functions from the older TABARI coder 
and the new CAMEO.verbpatterns.140609.txt dictionary incorporates both parser-based matching 
and extensive synonym sets. The program coded 60,000 AFP sentences from the GigaWord corpus 
without crashing, using the included dictionaries.

For more information, please visit the (work-in-progress)
[documentation](http://petrarch.readthedocs.org/en/latest/#).

**Note <PAS 21-July-2017>:** The most recent version here went through quite a few modifications -- for example eliminating most of the debugging and all of the unit-test/validation code -- prior to eventually being transitioned to the essentially entirely new program PETRARCH-2. Consequently if for some reason you wish to return to "PETRARCH-Classic", you might want to either go back to circa version 76ccdbffddbcb10bfa5bf4491bcdee2301f3e24e, or just get the stable version at https://github.com/philip-schrodt/petrarch, which does include a 284-record validation suite. Most of our development, however, has shifted to https://github.com/openeventdata/UniversalPetrarch, which uses a universal dependency parse rather than a constituency parse, and that code is likely a more useful base than the PETRARCH code.

##Installing

Installing the program is as simple as:

`pip install git+https://github.com/openeventdata/petrarch.git`

This will install the program with a command-line hook. You can now run the program using:

``petrarch <COMMAND NAME> [OPTIONS]``

You can get more information using:

``petrarch -h``

##Running

###But first, a note.

It is possible to run PETRARCH as a stand-alone program. Most of our
development work has gone into incorporating PETRARCH into a full pipeline of
utilities, though, e.g., the [Phoenix pipeline](https://github.com/openeventdata/phoenix_pipeline).
There's also a RESTful wrapper around PETRARCH and CoreNLP named
[hypnos](https://github.com/caerusassociates/hypnos). It's probably worthwhile
to explore those options before trying to use PETRARCH as a stand-alone.

###With that out of the way...

Currently, you can run PETRARCH using the following command if installed:

``petrarch batch -i <INPUT FILE> ``

If not installed:

``python petrarch.py batch -i data/text/GigaWord.sample.PETR.xml``

There's also the option to specify a configuration file using the ``-c <CONFIG
FILE>`` flag, but the program will default to using ``PETR_config.ini``.

When you run the program, a ``PETRARCH.log`` file will be opened in the current
working directory. This file will contain general information, e.g., which
files are being opened, and error messages.

##Unit tests

Commits should always successfully complete

``petrarch validate``

This command defaults to the ``PETR.UnitTest.records.txt`` file included with the
program. Alternative files can be indicated using the ``-i`` option. For example
(this is equivalent to the default command):

``petrarch validate -i data/text/PETR.UnitTest.records.xml``

The final record should read

    Sentence: FINAL-RECORD [ DEMO ]
    ALL OF THE UNIT TESTS WERE CODED CORRECTLY. 
    No events should be coded
    No events were coded
    Events correctly coded in FINAL-RECORD
    Exiting: <Stop> record 

There's also a check of the basic functionalities of PETRARCH available using
`pytest`. If you have `pytest` installed simply run `py.test` in the top-level
directory.

##Compatibilities with TABARI dictionaries

PETRARCH has a much richer dictionary syntax than TABARI, and because PETRARCH uses 
parsed input, many dictionary entries used by TABARI for noun-verb disambiguation are 
no longer needed. While the initial versions of the program could use existing TABARI 
dictionaries, PETRARCH-formatted dictionaries are now required: these are available in 
this repository and in https://github.com/openeventdata/Dictionaries.
