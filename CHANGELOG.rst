Changelog
=============


0.1.0
-------
* Formating Fixes
* BUGFIX: :code:`_perm_and_name_check` in :code:`GroupWorkflow` got called without kwargs

0.0.9
-------
* BUGFIX: :code:`_create_user` only takes KW arguments which i forgot...

0.0.8
-------
* All Workflow Functions now accept arbitary number of kwargs
* App Config got extended by a :code:`default_vhost` Setting which will get used in the :code:`SessionWorkflow`

0.0.7
-------
* changed workflows to return data which fits to my idea of usefull response data

0.0.6
-------
* ldap import now optional

0.0.3
-------
* SSL Context is automatically created if DBConfig recieves the :code:`ca_file` parameter

0.0.2
-------
Initial Version