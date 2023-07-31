.. py_auth_micro documentation master file, created by
   sphinx-quickstart on Wed Oct 19 23:01:41 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

General
=============================

`py_auth_micro` is a small identity provider library which can use an LDAP/AD as upstream Identity Provider and can also store Users Localy.

The Authentication and Authorization is done via `ID-Tokens` and `Access-Tokens`. The `ID-Tokens` are given out after a User successfully logged in.
With this `ID-Token` a User can request an `Access-Token` which he can send to other (Micro-)Services to gain access According to his Permissions.

The Tokens are `JWT` Tokens which can either be signed with an symetric `HMAC`-Secret or with an `RSA`-Key.

   
Content
-----------

.. toctree::
   :maxdepth: 5
   :includehidden:

   getting_started
   examples
   api_reference
   CHANGELOG

* :ref:`genindex`
   