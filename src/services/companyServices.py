from db import db
from flask import session
from sqlalchemy.sql import text

class CompanyData:
    def __init__(self, id = None, companyName: str = "", businessId: str = "", notes: str = "", websiteUrl : str="", email: str="", phone: str="", address: str=""):
        self.companyName = companyName
        self.businessId = businessId
        self.notes = notes
        self.websiteUrl = websiteUrl
        self.email = email
        self.phone = phone
        self.address = address
        self.id = id

    id: int
    companyName: str
    businessId: str
    notes: str
    websiteUrl: str
    email: str
    phone: str
    address: str

class CompanyContactData:
    def __init__(self, id=None, firstName: str = "", lastName: str = "", email: str = "", phone: str = ""):
            self.id = id
            self.firstName = firstName
            self.lastName = lastName
            self.email = email
            self.phone = phone

    id: int
    firstName: str
    lastName: str
    email: str
    phone: str

def upsertCompany(company: CompanyData, updateId=None):
    try:
        if not updateId:
            createCompanySql = text(
                "INSERT INTO companies (companyName, businessId, notes, websiteUrl, email, phone, address, groupId) "
                "VALUES (:companyName, :businessId, :notes, :websiteUrl, :email, :phone, :address, :groupId)")
            db.session.execute(createCompanySql, {
                "companyName": company.companyName, 
                "businessId": company.businessId, 
                "notes": company.notes, 
                "websiteUrl": company.websiteUrl, 
                "email": company.email, 
                "phone": company.phone, 
                "address": company.address, 
                "groupId": session["groupId"]
            })
        else:
            updateCompanySql = text(
                "UPDATE companies SET companyName = :companyName, businessId = :businessId, notes = :notes, "
                "websiteUrl = :websiteUrl, email = :email, phone = :phone, address = :address, groupId = :groupId "
                "WHERE id = :id"
            )
            db.session.execute(updateCompanySql, {
                "companyName": company.companyName,
                "businessId": company.businessId,
                "notes": company.notes,
                "websiteUrl": company.websiteUrl,
                "email": company.email,
                "phone": company.phone,
                "address": company.address,
                "groupId": session["groupId"],
                "id": updateId
            })
        
        db.session.commit()
        return True
    except:
        return False
    
def getCompany(id):
    getCompanySql = text("SELECT * FROM companies WHERE id=:id")
    getCompanyResult = db.session.execute(getCompanySql, {"id": id})
    company = getCompanyResult.fetchone()
    if not company:
        return None
    return CompanyData(
        None, 
        company[1], 
        company[2],
        company[3],
        company[4],
        company[5],
        company[6],
        company[7]
    )

def getAllGroupCompanies(groupId):
    getCompaniesSql = text("SELECT * FROM companies WHERE groupId=:groupId")
    getCompaniesResult = db.session.execute(getCompaniesSql, {"groupId": groupId})
    return [
        CompanyData(
            company[0],
            company[1],
            company[2],
            company[3],
            company[4],
            company[5],
            company[6],
            company[7]
        )
        for company in getCompaniesResult.fetchall()
    ]

def upsertCompanyContact(contact: CompanyContactData, companyId, contactId):
    try:
        if not contactId:
            createContactSql = text(
                "INSERT INTO contacts (firstName, lastName, email, phone, companyId) "
                "VALUES (:firstName, :lastName, :email, :phone, :companyId)")
            db.session.execute(createContactSql, {
                "firstName": contact.firstName, 
                "lastName": contact.lastName, 
                "email": contact.email, 
                "phone": contact.phone,
                "companyId": companyId
            })
        else:
            updateContactSql = text(
                "UPDATE contacts SET firstName = :firstName, lastName = :lastName, email = :email, "
                "phone = :phone"
                "WHERE companyId = :companyId AND contactId = :contactId"
            )
            db.session.execute(updateContactSql, {
                "firstName": contact.firstName,
                "lastName": contact.lastName,
                "email": contact.email,
                "phone": contact.phone,
                "contactId": contactId,
                "companyId": companyId
            })
    
        db.session.commit()
        return True
    except:
        return False

def getCompanyContact(companyId, contactId):
    getContactSql = text("SELECT * FROM contacts WHERE companyId=:companyId AND id=:contactId")
    getContactResult = db.session.execute(getContactSql, {"companyId": companyId, "contactId": contactId})
    contact = getContactResult.fetchone()
    if not contact:
        return None
    return CompanyData(
        None, 
        contact[1], 
        contact[2],
        contact[3],
        contact[4]
    )

def getAllCompanyContacts(companyId):
    getContactsSql = text("SELECT * FROM contacts WHERE companyId=:companyId")
    getContactsResult = db.session.execute(getContactsSql, {"companyId": companyId})
    return [
        CompanyContactData(
            contact[0],
            contact[1],
            contact[2],
            contact[3],
            contact[4]
        )
        for contact in getContactsResult.fetchall()
    ]