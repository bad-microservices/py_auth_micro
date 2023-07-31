Changelog
=============

0.1.7
-------
* Removed :code:`LoginHandler.LoginKerberos` because it's not needed
* documentation:
   * switched theme to ``pydata``
   * added :code:`Exceptions` submodule documentation
* Code:
   * switched to absolute imports instead of relative imports 

0.1.6
-------
* BUGFIX: :code:`UserWorkflow.change_user` now only allows changing the :code:`activated` attribute if the calling user is an admin
* :code:`UserWorkflow.get_user` now includes a list of groups if the requesting user is an admin or the requested user himself

0.1.5
-------
* BUGFIX: :code:`UserWorkflow` returned wrong data format for :code:`get_user`
* BUGFIX: fixed typo in response message when deleting a group

0.1.4
-------
* BUGFIX: :code:`group_members` this time for real...

0.1.3
-------
* BUGFIX: :code:`group_members` had a bug which is now fixed....

0.1.2
-------
* new feature :code:`group_members` in :code:`GroupWorkflow` will return a list of all group Members.

0.1.1
-------
* BUGFIX: :code:`_perm_and_name_check` in :code:`GroupWorkflow` got called without kwargs... again

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