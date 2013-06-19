trytond-sugarcrm
================

Tryton integration with sugarcrm

This module imports Opportunities, Accounts and Contacts from SugarCRM.
This data is stored in following format in Tryton.

* **Opportunities in `Closed Won` state** are imported as **Parties**

* **Accounts related to Opportunity** are imported as **addresses**.

* **Billing and Shipping addresses on each account** are imported as
  **addresses**.

* **Contacts related to the Opportunity** are also imported as **addresses**.

* **Any phone, fax, email or website linked to Account or Contact** are
  imported as **contact mechanisms**.

* **Any documents attached to Opportunity, Account or Contact** are
  imported as **attachments**.

Build Status (Master)
---------------------

.. image:: https://travis-ci.org/openlabs/trytond-sugarcrm.png?branch=master


Build Status (Develop)
---------------------

.. image:: https://travis-ci.org/openlabs/trytond-sugarcrm.png?branch=develop


Useful Links
------------

* `Python Package Index PyPI <https://pypi.python.org/pypi/trytond_sugarcrm>`_
* `Documentation <http://openlabs.github.io/trytond-sugarcrm/>`_
