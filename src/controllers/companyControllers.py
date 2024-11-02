from flask import redirect, render_template, request, session
from pydantic import ValidationError
from services import companyServices
from validators import CompanyForm, formatErrors

def editCompanyController(id):
    if request.method == "GET":
        return render_template("editcompany.html", id=id)

    if request.method == "POST":
        try:
            formData = CompanyForm(**request.form.to_dict())
        except ValidationError as e:
            return render_template("editcompany.html", errorMessage=formatErrors(e.errors()))

        if companyServices.upsertCompany(formData, id):
            return redirect("/")
        return render_template("editcompany.html", errorMessage="Yrityksen luomisessa tapahtui virhe")