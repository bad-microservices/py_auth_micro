Getting started
=================

Requirements
--------------

* python3.6+
* python modules
    * jwt_helper
    * tortoise-orm[asyncmy]
    * bcrypt
* Optional
    * python-ldap

The Optional python-ldap Dependency is only needed if you want to use an LDAP/AD-Server as upstream Identity Provider.

Installation
--------------

via PyPi
~~~~~~~~

py_auth_micro is available from PyPi and can be installed with `pip` from there. Just run the following command.

.. code-block:: bash

    python3 -m pip install py_auth_micro


with python-ldap

.. code-block:: bash

    python3 -m pip install py_auth_micro python-ldap


From Source
~~~~~~~~~~~~~

#. Clone the repository

.. code-block:: bash

    git clone https://github.com/bad-microservices/py_auth_micro.git

#. navigate into the cloned folder

.. code-block:: bash

    cd py_auth_micro

#. install via pip

.. code-block:: bash

    python3 -m pip install .

(OPTIONAL) install python-ldap

.. code-block:: bash

    python3 -m pip install python-ldap
