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

