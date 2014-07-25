.. image:: http://cpe.mitre.org/images/cpe_logo.gif
   :alt: CPE Logo

Common Platform Enumeration (CPE) dictionary for Django
-------------------------------------------------------

*Django-CPE* (this code) is a LGPL licensed Python package, implementing the
CPE dictionary specification to store CPE names and metadata,
as well as importing and exporting them in XML format.


About the CPE dictionary standard
---------------------------------

Common Platform Enumeration (CPE) is a standardized method of describing
and identifying classes of applications, operating systems, and hardware
devices present among an enterprise's computing assets.

The CPE Dictionary specification defines a standardized method for
creating and managing CPE dictionaries. A dictionary is a repository
of CPE names and metadata associated with the names.

For more information, please visit the official website of CPE,
developed by `MITRE`_ and maintained by `NIST`_.

TODO: Put links to CPE versions (`old CPE versions`_ and `current CPE version`_)

TODO: Explain the CPE dictionary name changes
(CPE description format in version 1.1, CPE dictionary version 2.0 or higher).


Features
--------

- Django models associated with CPE dictionary elements.
- Import of CPE dictionaries with XML format.
(TODO: explain the implementation with SAX)
- LGPL Licensed.
- Semantic versioning.
- Tests.


Installation |Package_version| |TravisCI| |Coveralls| |Requires|
----------------------------------------------------------------

To install `Django-CPE` execute:

.. code-block:: bash

    $ pip install django-cpe

The latest stable version is always in `PyPI`_.


Documentation
-------------

Documentation is available at `ReadTheDocs`_.


Compatibility |Supported_Python_version|
----------------------------------------

- Python: 2.7-3.4 => TODO: check all versions
- CPE versions: 1.1, 2.0, 2.1, 2.2, 2.3 => TODO: check all versions


Contribute |Waffle_ready| |Download_format| |Downloads_day| |Downloads_week| |Downloads_month|
----------------------------------------------------------------------------------------------

Follow the steps on the `how to contribute`_ document.


License |License|
-----------------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.


.. _PyPI: https://pypi.python.org/pypi/django-cpe/
.. _MITRE: http://cpe.mitre.org/
.. _NIST: hhttp://nvd.nist.gov/cpe.cfm
.. _ReadTheDocs: https://django-cpe.readthedocs.org/en/latest/
.. _GitHub: https://github.com/galindale/django-cpe
.. _How to contribute: https://github.com/galindale/django-cpe/blob/develop/CONTRIBUTING.md
.. _Old CPE versions: http://cpe.mitre.org/cpe/archive/
.. _Current CPE version: http://cpe.mitre.org/specification/


.. |TravisCI| image:: https://travis-ci.org/galindale/django-cpe.svg?branch=master
   :target: https://travis-ci.org/galindale/django-cpe
   :alt: Build Status (master)

.. |TravisCI_develop| image:: https://travis-ci.org/galindale/django-cpe.svg?branch=develop
   :target: https://travis-ci.org/galindale/django-cpe
   :alt: Build Status (develop)

.. |Waffle_ready| image:: https://badge.waffle.io/galindale/django-cpe.png?label=ready&title=Ready
   :target: https://waffle.io/galindale/django-cpe
   :alt: Stories in Ready

.. |Coveralls| image:: https://coveralls.io/repos/galindale/django-cpe/badge.png?branch=master
   :target: https://coveralls.io/r/galindale/django-cpe?branch=master
   :alt: Coverage Status (master)

.. |Coverage_develop| image:: https://coveralls.io/repos/galindale/django-cpe/badge.png?branch=develop
   :target: https://coveralls.io/r/galindale/django-cpe?branch=develop
   :alt: Coverage Status (develop)

.. |Downloads_day| image:: https://pypip.in/download/django-cpe/badge.svg?period=day
   :target: https://crate.io/packages/django-cpe
   :alt: Downloads by day

.. |Downloads_week| image:: https://pypip.in/download/django-cpe/badge.svg?period=week
   :target: https://crate.io/packages/django-cpe
   :alt: Downloads by week

.. |Downloads_month| image:: https://pypip.in/download/django-cpe/badge.svg?period=month
   :target: https://crate.io/packages/django-cpe
   :alt: Downloads by month

.. |Requires| image:: https://requires.io/github/galindale/django-cpe/requirements.png?branch=master
   :target: https://requires.io/github/galindale/django-cpe/requirements/?branch=master
   :alt: Requirements Status (master)

.. |Requires_develop| image:: https://requires.io/github/galindale/django-cpe/requirements.png?branch=develop
   :target: https://requires.io/github/galindale/django-cpe/requirements/?branch=develop
   :alt: Requirements Status (develop)

.. |Package_version| image:: https://badge.fury.io/py/cpe.svg
    :target: http://badge.fury.io/py/cpe
    :alt: Latest Version

.. |Supported_Python_version| image:: https://pypip.in/py_versions/django-cpe/badge.svg
   :target: https://pypi.python.org/pypi/django-cpe/
   :alt: Supported Python versions

.. |Download_format_wheel| image:: https://pypip.in/wheel/django-cpe/badge.svg
   :target: https://pypi.python.org/pypi/django-cpe/
   :alt: Wheel Status

.. |Download_format_egg| image:: https://pypip.in/egg/django-cpe/badge.svg
   :target: https://pypi.python.org/pypi/django-cpe/
   :alt: Egg Status

.. |Download_format| image:: https://pypip.in/format/django-cpe/badge.svg
    :target: https://pypi.python.org/pypi/django-cpe/
    :alt: Download format

.. |License| image:: https://pypip.in/license/django-cpe/badge.svg
    :target: https://pypi.python.org/pypi/django-cpe/
    :alt: License
