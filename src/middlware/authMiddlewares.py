from functools import wraps
from flask import session, abort

from sqlalchemy.sql import text
from services.userServices import UserRoles

from db import db

def checkSessionBelongsToGroup():
    def decorator(f):
        @wraps(f)
        def decoratedFunction(*args, **kwargs):
            groupId = session.get("groupId")
            if not groupId:
                abort(403)

            return f(*args, **kwargs)
        return decoratedFunction
    return decorator

def checkSessionAccessToCompanyIdArg():
    def decorator(f):
        @wraps(f)
        @checkSessionBelongsToGroup()
        def decoratedFunction(*args, **kwargs):
            companyId = kwargs.get('id')
            if not companyId:
                return f(*args, **kwargs)

            role = session.get("role")
            if not role or UserRoles(role) is not UserRoles.OWNER and UserRoles(role) is not UserRoles.ADMIN:
                abort(403)

            getCompanySql = text("SELECT groupId FROM companies WHERE id=:companyId")
            getCompanyResult = db.session.execute(getCompanySql, {"companyId":companyId})
            companyGroupIdObject = getCompanyResult.fetchone()
            if not companyGroupIdObject:
                abort(404)
            companyGroupId = companyGroupIdObject[0]

            if session.get("groupId") is not companyGroupId:
                abort(403)

            return f(*args, **kwargs)
        return decoratedFunction
    return decorator