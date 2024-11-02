from db import db
from flask import session
from sqlalchemy.sql import text

class CompanyData:
    def __init__(self, companyName: str = "", businessId: str = ""):
        self.companyName = companyName
        self.businessId = businessId

    companyName: str
    businessId: str

def upsertCompany(company: CompanyData, updateId=None):
    try:
        if not updateId:
            createCompanySql = text("INSERT INTO companies (companyName, businessId, groupId) VALUES (:companyName, :businessId, :groupId)")
            db.session.execute(createCompanySql, {"companyName": company.companyName, "businessId": company.businessId, "groupId": session["groupId"]})
        else:
            updateCompanySql = text("UPDATE companies SET companyName = :companyName, businessId = :businessId WHERE id = :id")
            db.session.execute(updateCompanySql, {"companyName": company.companyName, "businessId": company.businessId, "groupId": session["groupId"], "id": updateId})
        
        db.session.commit()
        return True
    except:
        return False
    
def getCompany(id):
    getCompanySql = text("SELECT companyName, businessId FROM companies WHERE id=:id")
    getCompanyResult = db.session.execute(getCompanySql, {"id": id})
    company = getCompanyResult.fetchone()
    if not company:
        return None
    return CompanyData(companyName=company[0], businessId=company[1])