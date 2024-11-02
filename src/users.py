from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from flask import session
from sqlalchemy.sql import text

from enum import IntEnum

class UserRoles(IntEnum):
    OWNER = 1
    ADMIN = 2
    VIEWER = 3

def login(username, password):
    getUserSql = text("SELECT id, password FROM users WHERE username=:username")
    getUserResult = db.session.execute(getUserSql, {"username":username})
    user = getUserResult.fetchone()

    if not user:
        return False
    
    if check_password_hash(user.password, password):
        getUserGroupIdSql = text("SELECT groupId, role FROM userGroups WHERE userId=:userId")
        getUserGroupIdResult = db.session.execute(getUserGroupIdSql, {"userId":user.id})
        group = getUserGroupIdResult.fetchone()
        
        session["username"] = username
        session["groupId"] = group[0]
        session["role"] = group[1]
        return True
    
    return False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        createUserSql = text("INSERT INTO users (username, password) VALUES (:username, :password) RETURNING id")
        createUserResult = db.session.execute(createUserSql, {"username":username, "password":hash_value})
        userId = createUserResult.fetchone()[0]

        createGroupSql = text("INSERT INTO groups DEFAULT VALUES RETURNING id")
        createGroupResult = db.session.execute(createGroupSql)
        groupId = createGroupResult.fetchone()[0]
        
        insertUserGroupSql = text("INSERT INTO userGroups (userId, groupId, role) VALUES (:userId, :groupId, :role)")
        db.session.execute(insertUserGroupSql, {"userId": userId, "groupId": groupId, "role": UserRoles.OWNER})

        db.session.commit()
    except:
        return False
    return login(username, password)

