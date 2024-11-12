"""
Functions for user authentication and management.
Includes login, registration, and user creation,
with role-based access control.
"""

from enum import IntEnum

from flask import abort, session
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


class UserData:
    """
    A class representing user data.
    """

    def __init__(
            self,
            userId=None,
            groupId=None,
            username="",
            role=-1):
        self.userId = userId
        self.groupId = groupId
        self.username = username
        self.role = role

    userId: int
    groupId: int
    username: str
    role: int


def login(username, password):
    """
    Authenticates a user by verifying the provided username and password.

    If the credentials are correct, it sets the session variables `username`, `groupId`,
    and `role` to manage user state for the session.
    """

    getUserSql = text(
        "SELECT id, password FROM users WHERE username=:username")
    getUserResult = db.session.execute(getUserSql, {"username": username})
    user = getUserResult.fetchone()

    if not user:
        return False

    if check_password_hash(user.password, password):
        getUserGroupIdSql = text(
            "SELECT groupId, role, userId FROM userGroups WHERE userId=:userId")
        getUserGroupIdResult = db.session.execute(
            getUserGroupIdSql, {"userId": user.id})
        group = getUserGroupIdResult.fetchone()

        session["username"] = username
        session["groupId"] = group[0]
        session["role"] = group[1]
        session["userId"] = group[2]
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
            createGroupSql = text(
                "INSERT INTO groups DEFAULT VALUES RETURNING id")
            createGroupResult = db.session.execute(createGroupSql)
            groupId = createGroupResult.fetchone()[0]

        if role is None:
            role = UserRoles.OWNER

        insertUserGroupSql = text(
            "INSERT INTO userGroups (userId, groupId, role) VALUES (:userId, :groupId, :role)")
        db.session.execute(insertUserGroupSql, {
                           "userId": userId, "groupId": groupId, "role": role})

        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def editUserRole(role, userId, groupId):
    """
    Edits a users role in a certain group.
    """

    try:
        updateRoleSql = text(
            "UPDATE userGroups SET role = :role WHERE userId = :userId AND groupId = :groupId"
        )
        db.session.execute(
            updateRoleSql, {"role": role, "userId": userId, "groupId": groupId})

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


def getAllGroupUsers(groupId):
    """
     Retrieve all users associated with a specific group.
    """

    getUsersByGroupIdSql = text("""
        SELECT u.id, ug.groupId, u.username, ug.role
        FROM users u
        JOIN userGroups ug ON u.id = ug.userId
        WHERE ug.groupId = :groupId
    """)
    getUsersByGroupIdResult = db.session.execute(
        getUsersByGroupIdSql, {"groupId": groupId})
    return [
        UserData(
            user[0],
            user[1],
            user[2],
            user[3]
        )
        for user in getUsersByGroupIdResult.fetchall()
    ]


def getUser(userId):
    """
    Retrieve a user by its unique identifier.
    """

    getUserSql = text("SELECT id, username FROM users WHERE id=:id")
    getUserResult = db.session.execute(getUserSql, {"id": userId})
    user = getUserResult.fetchone()
    if not user:
        abort(404)
        return None
    return UserData(
        userId=user[0],
        username=user[1]
    )

def deleteUser(userId):
    """
    Delete a user by its unique identifier
    """
    try:
        #@todo ALSO DELETE USER FROM USERGROUPS!!!
        deleteUserSql = text("DELETE FROM users WHERE id = :id")
        deleteResult = db.session.execute(deleteUserSql, {"id": userId})

        if deleteResult.rowcount == 0:
            abort(404)

        db.session.commit()
        return True

    except SQLAlchemyError:
        db.session.rollback()
        return False
    
def getUserRole(userId, groupId):
    """
    Retrieve the role of a user in a specified group.
    """
    try:
        getUserRoleSql = text("SELECT role FROM userGroups WHERE userId = :userId AND groupId = :groupId")
        result = db.session.execute(getUserRoleSql, {"userId": userId, "groupId": groupId})
        role = result.fetchone()
        
        if not role:
            abort(403)
            return None

        return role[0]

    except SQLAlchemyError:
        db.session.rollback()
        return None