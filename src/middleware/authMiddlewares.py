"""
Decorators for controlling user access based on group, role, and resource ownership.
Ensures proper access to companies and contacts based on user session data.
"""

from functools import wraps
from flask import session, abort

from sqlalchemy.sql import text
from services import userServices
from services.userServices import UserRoles

from db import db


def checkBelongsToGroup():
    """
    Decorator that ensures the user belongs to a group, aborts with 403 if not.
    """
    def decorator(f):
        @wraps(f)
        def decoratedFunction(*args, **kwargs):
            groupId = session.get("groupId")
            if not groupId:
                abort(403)

            return f(*args, **kwargs)
        return decoratedFunction
    return decorator


def checkEditAccess():
    """
    Decorator that checks if the user has edit access (OWNER or ADMIN role).
    Ensures the user has the required access and aborts with 403 if access is denied.
    """
    def decorator(f):
        @wraps(f)
        @checkBelongsToGroup()
        def decoratedFunction(*args, **kwargs):
            userId = session.get("userId")
            groupId = session.get("groupId")

            role = userServices.getUserRole(userId, groupId)
            if not role or UserRoles(role) is not UserRoles.OWNER and UserRoles(
                    role) is not UserRoles.ADMIN:
                abort(403)
            return f(*args, **kwargs)
        return decoratedFunction
    return decorator


def checkOwnerAccess():
    """
    Decorator that checks if the user has OWNER access.
    Ensures the user has the required access and aborts with 403 if access is denied.
    """
    def decorator(f):
        @wraps(f)
        @checkBelongsToGroup()
        def decoratedFunction(*args, **kwargs):
            userId = session.get("userId")
            groupId = session.get("groupId")

            role = userServices.getUserRole(userId, groupId)
            if UserRoles(role) is not UserRoles.OWNER:
                abort(403)
            return f(*args, **kwargs)
        return decoratedFunction
    return decorator


def checkAccessToCompanyIdArg():
    """
    Decorator that checks if the user has access to the company specified by the companyId argument.
    Ensures the user belongs to the same group as the company.
    """
    def decorator(f):
        @wraps(f)
        @checkBelongsToGroup()
        def decoratedFunction(*args, **kwargs):
            companyId = kwargs.get('companyId')
            if not companyId:
                return f(*args, **kwargs)

            getCompanySql = text(
                "SELECT groupId FROM companies WHERE id=:companyId")
            getCompanyResult = db.session.execute(
                getCompanySql, {"companyId": companyId})
            companyGroupIdObject = getCompanyResult.fetchone()
            if not companyGroupIdObject:
                abort(404)
            companyGroupId = companyGroupIdObject[0]

            if session.get("groupId") is not companyGroupId:
                abort(403)

            return f(*args, **kwargs)
        return decoratedFunction
    return decorator


def checkAccessToCompanyAndContactIdArg():
    """
    Decorator that checks if the user has access to both the
    company and contact specified by the companyId and contactId arguments.
    Ensures the user has the necessary role and belongs to the same company as the contact.
    """
    def decorator(f):
        @wraps(f)
        @checkAccessToCompanyIdArg()
        def decoratedFunction(*args, **kwargs):
            companyId = kwargs.get('companyId')
            contactId = kwargs.get('contactId')
            if not contactId:
                return f(*args, **kwargs)

            userId = session.get("userId")
            groupId = session.get("groupId")

            role = userServices.getUserRole(userId, groupId)

            if not role or (UserRoles(role) is not UserRoles.OWNER and UserRoles(
                    role) is not UserRoles.ADMIN):
                abort(403)

            getContactSql = text(
                "SELECT companyId FROM contacts WHERE id=:contactId")
            getContactResult = db.session.execute(
                getContactSql, {"contactId": contactId})
            contactCompanyIdObject = getContactResult.fetchone()
            if not contactCompanyIdObject:
                abort(404)
            contactCompanyId = contactCompanyIdObject[0]

            if contactCompanyId is not companyId:
                abort(403)

            return f(*args, **kwargs)
        return decoratedFunction
    return decorator


def checkAccessToUserIdArg():
    """
    Decorator that checks if the user has access to the user specified by the userId argument.
    Ensures the session user belongs to the same group as the userId.
    """
    def decorator(f):
        @wraps(f)
        @checkBelongsToGroup()
        def decoratedFunction(*args, **kwargs):
            userId = kwargs.get('userId')
            if not userId:
                return f(*args, **kwargs)

            if userId == session.get('userId'):
                abort(403)

            getGroupSql = text(
                "SELECT groupId FROM userGroups WHERE userId = :userId")
            getGroupResult = db.session.execute(
                getGroupSql, {"userId": userId})
            userGroup = getGroupResult.fetchone()

            if not userGroup:
                abort(404)

            userGroupId = userGroup[0]

            if session.get("groupId") != userGroupId:
                abort(403)

            return f(*args, **kwargs)
        return decoratedFunction
    return decorator
