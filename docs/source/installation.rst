Installing trytond-sugarcrm module
==================================

The steps below below describe the process of installing the module on
a tryton instance.

.. _install-module-source:

Installation from source code
-----------------------------

**Installing dependency**

1. The module depends on a python module which can be downloaded from
   `here <https://github.com/sugarcrm/python_webservices_library>`_.

2. The module can be downloaded as a `zip` or can be `cloned` by running

   .. code-block:: sh 

        git clone https://github.com/sugarcrm/python_webservices_library.git

3. If the module is downloaded as a zip, extract the module which will
   give a directory.

4. From the module directory, use the setup.py script with the command:

   .. code-block:: sh

        python setup.py install

**Installing tryton module**

1. The module source is available online and can be downloaded from
   `here <https://github.com/openlabs/trytond-sugarcrm>`_.

2. The module can be downloaded as a `zip` or can be `cloned` by running

   .. code-block:: sh 

        git clone https://github.com/openlabs/trytond-sugarcrm.git

3. If the module is downloaded as a zip, extract the module which will
   give a directory.

4. From the module directory, use the setup.py script with the command:

   .. code-block:: sh

        python setup.py install

5. The command above makes the module available for use by tryton server
   instance in a database.

6. The module can be installed in a tryton database by following to menu:

   | ``Administration > Modules > Modules``

7. This should show the modules list screen as below:

   .. image:: images/modules.png
      :width: 900

8. Install the module as shown below:

   | ``Step 1``

    .. image:: images/install.png
       :width: 900

   | ``Step 2``

    .. image:: images/perform.png
       :width: 900

   | ``Step 3``

    .. image:: images/popup.png
       :width: 900


.. _install-module-pypi:

Installation from PYPI
----------------------

TODO
   

:ref:`configure-sugarcrm-account`
