================
py_auth_micro
================

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://pypi.org/project/black

.. image:: https://app.codacy.com/project/badge/Grade/199fd463ff1a487eb206a2afbfb25168
    :target: https://www.codacy.com/gh/bad-microservices/py_auth_micro/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=bad-microservices/py_auth_micro&amp;utm_campaign=Badge_Grade

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
