"""This Package specifies classes which implement the most common workflows.

following workflows are implemented:

    * Sign In
    * Sign Out
    * Token Request
    * Registration
    * User creation (by Administrators)
    * User deletion
    * Group creation (by Administrators)
    * Group deletion (by Administrators)
    * Adding User to a Group (by Administrators)
    * Removing User from a Group (by Administrators)

All Function should return Dictionaries which can be easily parsed to JSON

"""

from ._userworkflow import UserWorkflow
from ._sessionworkflow import SessionWorkflow
from ._groupworkflow import GroupWorkflow

__all__ = ["UserWorkflow", "SessionWorkflow","GroupWorkflow"]
