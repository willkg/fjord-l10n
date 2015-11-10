======
README
======

This repository holds scripts and exporters for tracking l10n progress
for Input.

This generates data for `postatus <https://github.com/willkg/postatus/>`_.


Installation
============

1. Clone the repository locally::

      $ git clone https://github.com/willkg/fjord-l10n

2. Create a virtual environment and activate it::

      $ mkvirtualenv l10n

3. Install requirements::

      $ pip install -r requirements.txt


Usage
=====

l10n_completion
---------------

::

   $ workon l10n
   $ ./bin/run_svn_and_l10n_completion.sh OUTPUTFILE LOCALEDIR


That'll do an ``svn update`` in the LOCALEDIR and then figure out completion
status and put it in the OUTPUTFILE.
