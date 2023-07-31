"""This Package specifies classes which implement the most common workflows.

following workflows are implemented:

    * SessionWorkflow
       * Sign In
       * Sign Out
       * Token Request
    * UserWorkFlow
       * Registration
       * User creation (by Administrators)
       * User deletion
    * GroupWorkfFlow
       * Group creation (by Administrators)
       * Group deletion (by Administrators)
       * Adding User to a Group (by Administrators)
       * Removing User from a Group (by Administrators)

All Function should return Dictionaries which can be easily parsed to JSON

"""

from py_auth_micro.WorkFlows._userworkflow import UserWorkflow
from py_auth_micro.WorkFlows._sessionworkflow import SessionWorkflow
from py_auth_micro.WorkFlows._groupworkflow import GroupWorkflow
from py_auth_micro.WorkFlows import _misc as misc

__all__ = ["UserWorkflow", "SessionWorkflow", "GroupWorkflow", "misc"]
