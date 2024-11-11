"""
Functions for user authentication and management.
Includes login, registration, and user creation,
with role-based access control.
"""

from enum import IntEnum

from flask import session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

class UserRoles(IntEnum):
    """
    Enum representing the different roles a user can have within the system.
    """

    OWNER = 1
    ADMIN = 2
    VIEWER = 3


def login(username, password):
    """
    Authenticates a user by verifying the provided username and password.

    If the credentials are correct, it sets the session variables `username`, `groupId`,
    and `role` to manage user state for the session.
    """
    getUserSql = text("SELECT id, password FROM users WHERE username=:username")
    getUserResult = db.session.execute(getUserSql, {"username": username})
    user = getUserResult.fetchone()

    if not user:
        return False

    if check_password_hash(user.password, password):
        getUserGroupIdSql = text("SELECT groupId, role FROM userGroups WHERE userId=:userId")
        getUserGroupIdResult = db.session.execute(getUserGroupIdSql, {"userId": user.id})
        group = getUserGroupIdResult.fetchone()

        session["username"] = username
        session["groupId"] = group[0]
        session["role"] = group[1]
        return True

    return False


def createUser(username, password, role: UserRoles = None, groupId=None):
    """
    Creates a new user, hashes their password, and assigns them a role and group.
    """

    hashValue = generate_password_hash(password)
    try:
        createUserSql = text(
            "INSERT INTO users (username, password) VALUES (:username, :password) RETURNING id")
        createUserResult = db.session.execute(
            createUserSql, {"username": username, "password": hashValue})
        userId = createUserResult.fetchone()[0]

        if not groupId:
            createGroupSql = text("INSERT INTO groups DEFAULT VALUES RETURNING id")
            createGroupResult = db.session.execute(createGroupSql)
            groupId = createGroupResult.fetchone()[0]

        if role is None:
            role = UserRoles.OWNER

        insertUserGroupSql = text(
            "INSERT INTO userGroups (userId, groupId, role) VALUES (:userId, :groupId, :role)")
        db.session.execute(insertUserGroupSql, {"userId": userId, "groupId": groupId, "role": role})

        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def register(username, password):
    """
    Registers a new user by creating their account and logging them in.
    """

    userCreated = createUser(username, password)
    if userCreated:
        return login(username, password)
    return False
