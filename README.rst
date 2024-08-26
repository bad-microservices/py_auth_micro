================
py_auth_micro
================

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://pypi.org/project/black

.. image:: https://app.codacy.com/project/badge/Grade/199fd463ff1a487eb206a2afbfb25168
    :target: https://app.codacy.com/gh/bad-microservices/py_auth_micro/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade

.. image:: https://badge.fury.io/py/py-auth-micro.svg
    :target: https://badge.fury.io/py/py-auth-micro

.. image:: https://github.com/bad-microservices/py_auth_micro/actions/workflows/documentation.yaml/badge.svg
   :target: https://github.com/bad-microservices/py_auth_micro/actions?query=workflow:Docs

.. image:: https://github.com/bad-microservices/py_auth_micro/actions/workflows/pypi_upload.yaml/badge.svg
    :target: https://github.com/bad-microservices/py_auth_micro/actions?query=workflow:pypi

Introduction
=============

`py_auth_micro` is a small identity provider library which can use an LDAP/AD as upstream Identity Provider and can also store Users Localy.

The Authentication and Authorization is done via `ID-Tokens` and `Access-Tokens`. The `ID-Tokens` are given out after a User successfully logged in.
With this `ID-Token` a User can request an `Access-Token` which he can send to other (Micro-)Services to gain access According to his Permissions.

The Tokens are `JWT` Tokens which can either be signed with an symetric `HMAC`-Secret or with an `RSA`-Key.

Documentation
==============

You can find the documentation `here <https://bad-microservices.github.io/py_auth_micro/>`_

Alternatively you can build it yourself by running :code:`make doc`

TODO
=====

There is still alot todo for the :code:`1.0.0` Release. The following list contains the most important stuff

- ☐ Reset-Password functionality
- ☐ Unit Tests
   - ☐ WorkFlows
      - ☑ :code:`GroupWorkflow`
      - ☐ :code:`SessionWorkflow`
      - ☐ :code:`UserWorkflow` 
   - ☐ Models
      - ☐ :code:`Group`
      - ☐ :code:`Token` 
      - ☐ :code:`User`
   - ☐ LoginHandler
      - ☐ :code:`LoginLDAP`
      - ☐ :code:`LoginLocal`
   - ☐ Core
      - ☐ :code:`LDAPHelper`
      - ☐ :code:`_ConnectionHandler`
- ☐ Documentation 
   - ☑ Api Reference
   - ☑ Installation
   - ☐ Example Code 


Contributing
=============

Missing a Feature or found a bug? Create an Issue or make a Pull-Request ;)

If you have any Question regarding this library feel free to create an issue.
