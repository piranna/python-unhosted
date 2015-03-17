This is a Python library for Unhosted project (http://unhosted.org).
It provides a class implementing Unhosted JSON protocol
and support for Twisted Web (http://twistedmatrix.com).

Python-Unhosted is licensed under GNU LGPL license.

Release:
  * Release planning for 0.2.0: http://code.google.com/p/python-unhosted/wiki/Release020
  * Opened issues for 0.2.0: http://code.google.com/p/python-unhosted/issues/list?q=Milestone:0.2.0

Installation:
  * Clone our main development branch: hg clone https://python-unhosted.googlecode.com/hg/ python-unhosted
  * Be sure to have Python >= 2.4 and optionally Twisted Web
  * Install into system-wide location: python setup.py install
  * ... or into home directory: python setup.py install --home
  * ... or create RPM: python setup.py bdist\_rpm
  * ... or view distutils-provided help: python setup.py --help

Library features the following classes:
  * unhosted.IAccount - interface for storage-specific account implementations.
  * unhosted.IStorage - interface for any kind of storages. Stores (value, signature) tuples. Contains get(), put() and has() methods. Value can be looked up by account and key.
  * unhosted.Unhosted - main class, provides processRequest().
  * unhosted.databasestorage.DatabaseStorage - wrapper around any DB-API 2.0 compatible connection.
  * unhosted.dictstorage.DictStorage - wrapper around any dict-like object.
  * unhosted.mailchecker.MailChecker - Account checker via email.
  * unhosted.tx.UnhostedResource - Twisted Web resource for Unhosted.