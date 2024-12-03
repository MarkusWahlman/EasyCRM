"""
Jinja utility processor for adding utility functions to Flask templates.
"""

from flask import request, url_for, session
from services.userServices import UserRoles

def utilityProcessor():
    """
    Utility functions for the Jinja context.
    """

    def isActive(endpoint):
        return 'active' if request.path == url_for(endpoint) else ''

    def hasEditAccess():
        role = session.get('role')
        if not role or UserRoles(role) is not UserRoles.OWNER and UserRoles(
                    role) is not UserRoles.ADMIN:
                return False
        return True

    def hasOwnerAccess():
        role = session.get('role')
        if not role or UserRoles(role) is not UserRoles.OWNER:
                return False
        return True

    return {
        "isActive": isActive,
        "hasEditAccess": hasEditAccess,
        "hasOwnerAccess": hasOwnerAccess
    }

        
