from db import db
from flask import session
from sqlalchemy.sql import text

class CompanyData:
    companyName: str
    businessId: str

def upsertCompany(company: CompanyData, updateId=None):
    try:
        if not updateId:
            createCompanySql = text("INSERT INTO companies (companyName, businessId, groupId) VALUES (:companyName, :businessId, :groupId)")
            db.session.execute(createCompanySql, {"companyName": company.companyName, "businessId": company.businessId, "groupId": session["groupId"]})
        else:
            updateCompanySql = text("UPDATE companies SET companyName = :companyName, businessId = :password, groupId = :groupId WHERE id = :id")
            db.session.execute(updateCompanySql, {"companyName": company.companyName, "businessId": company.businessId, "groupId": session["groupId"], "id": updateId})
        return True
    except:
        return False