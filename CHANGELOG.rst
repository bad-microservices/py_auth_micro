Changelog
=============

0.2.4
------
* BUGFIX: removed unneeded :code:`print` statement which raised :code:`KeyError` on a missing :code:`mail` attribute

0.2.3
------
* Autogenerate Email for LDAP Users without an :code:`mail` attribute


0.2.2
------
* Token to User Relation is a 1 to 1 relation and not 1 to n.
   * Workflows got some fixes
* Changed alot of logging.info to logging.debug for clarity

0.2.1
------
* Removed Typehint which is not supported by python3.9
* added Test for the LDAP group sync with non existing groups
* Fixed a bug where non existing groups caused problems for LDAP Login the first time

0.2.0
-------
* Alot of type hint cleanup
* fixed a bug where non existing groups in active directory sync interfiered with login.
   * missing groups now get created and saved!
* updated tests for more moden pytest versions

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