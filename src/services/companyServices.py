from db import db
from flask import abort, render_template, session
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
    def __init__(self, id=None, firstName: str = "", lastName: str = "", email: str = "", phone: str = "", companyName: str = "", companyId: str = ""):
            self.id = id
            self.firstName = firstName
            self.lastName = lastName
            self.email = email
            self.phone = phone
            self.companyName = companyName
            self.companyId = companyId

    id: int
    firstName: str
    lastName: str
    email: str
    phone: str
    companyName: str
    companyId: str

def renderUpsertCompanyTemplate(id, errorMessage=""):
    company = CompanyData()
    if id:
        company = getCompany(id)
    return render_template("upsertcompany.html", 
                           id=id, 
                           company=company,
                           errorMessage=errorMessage)

def renderCompanyContactTemplate(companyId, contactId, errorMessage=""):
    contact = CompanyContactData()
    if companyId and contactId:
        contact = getCompanyContact(companyId, contactId)
        if not contact:
            return render_template("404.html")
    return render_template("upsertcontact.html", 
                           companyId=companyId,
                           contactId=contactId,
                           contact=contact,
                           errorMessage=errorMessage)

def upsertCompany(company: CompanyData, companyId=None):
    try:
        if not companyId:
            createCompanySql = text(
                "INSERT INTO companies (companyName, businessId, notes, websiteUrl, email, phone, address, groupId) "
                "VALUES (:companyName, :businessId, :notes, :websiteUrl, :email, :phone, :address, :groupId) RETURNING id")
            createCompanyResult = db.session.execute(createCompanySql, {
                "companyName": company.companyName, 
                "businessId": company.businessId, 
                "notes": company.notes, 
                "websiteUrl": company.websiteUrl, 
                "email": company.email, 
                "phone": company.phone, 
                "address": company.address, 
                "groupId": session["groupId"]
            })
            companyId = createCompanyResult.fetchone()[0]
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
                "id": companyId
            })
        
        db.session.commit()
        return companyId
    except:
        return None
    
def getCompany(id):
    getCompanySql = text("SELECT * FROM companies WHERE id=:id")
    getCompanyResult = db.session.execute(getCompanySql, {"id": id})
    company = getCompanyResult.fetchone()
    if not company:
        abort(404)
        return None
    return CompanyData(
        company[0], 
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
                "VALUES (:firstName, :lastName, :email, :phone, :companyId) RETURNING id")
            createContactResult = db.session.execute(createContactSql, {
                "firstName": contact.firstName, 
                "lastName": contact.lastName, 
                "email": contact.email, 
                "phone": contact.phone,
                "companyId": companyId
            })
            contactId = createContactResult.fetchone()[0]
        else:
            updateContactSql = text(
                "UPDATE contacts SET firstName = :firstName, lastName = :lastName, email = :email, phone = :phone "
                "WHERE companyId = :companyId AND id = :contactId"
            )
            db.session.execute(updateContactSql, {
                "firstName": contact.firstName,
                "lastName": contact.lastName,
                "email": contact.email,
                "phone": contact.phone,
                "companyId": companyId,
                "contactId": contactId
            })

        db.session.commit()
        return contactId
    except:
        return None

def getCompanyContact(companyId, contactId):
    getContactSql = text("SELECT * FROM contacts WHERE companyId=:companyId AND id=:contactId")
    getContactResult = db.session.execute(getContactSql, {"companyId": companyId, "contactId": contactId})
    contact = getContactResult.fetchone()
    if not contact:
        abort(404)
        return None
    return CompanyContactData(
        contact[0], 
        contact[1], 
        contact[2],
        contact[3],
        contact[4],
        "",
        companyId
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

def getAllGroupContacts(groupId):
    getContactsSql = text("""
        SELECT contacts.*, companies.companyName, companies.id
        FROM contacts
        JOIN companies ON contacts.companyId = companies.id
        JOIN groups ON companies.groupId = groups.id
        WHERE groups.id = :groupId
    """)
    getContactsResult = db.session.execute(getContactsSql, {"groupId": groupId})
    
    return [
        CompanyContactData(
            contact[0],  # id
            contact[1],  # firstName
            contact[2],  # lastName
            contact[3],  # email
            contact[4],  # phone
            contact[-2], # companyName
            contact[-1]  # companyId
        )
        for contact in getContactsResult.fetchall()
    ]