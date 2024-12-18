"""
Pydantic models for form validation.
"""

import re
from typing import Dict, List, Optional
from flask import abort, session
from pydantic_core import ErrorDetails, PydanticCustomError
from typing_extensions import Annotated
from pydantic import BaseModel, Field, StringConstraints, ValidationError, field_validator

CUSTOM_MESSAGES = {
    'string_too_long': 'Syöttämäsi merkkijono on liian pitkä.',
    'string_too_short': 'Syöttämäsi merkkijono on liian lyhyt.',
    'less_than_equal': 'Syöttämäsi numero on liian suuri.',
    'greater_than_equal': 'Syöttämäsi numero on liian pieni.'
}

LOC_TRANSLATIONS = {
    'username': 'Käyttäjätunnus',
    'password': 'Salasana',
    'businessId': 'Y-tunnus',
    'companyName': 'Yrityksen nimi',
    'role': 'Rooli'
}


def convertErrors(
    e: ValidationError, customMessages: Dict[str, str], locTranslations: Dict[str, str]
) -> List[ErrorDetails]:
    """
    Converts error details into a user-friendly format with custom messages and translations.
    """
    newErrors: List[ErrorDetails] = []
    for error in e:
        print(error)
        customMessage = customMessages.get(error['type'])
        if customMessage:
            ctx = error.get('ctx')
            error['msg'] = (
                customMessage.format(**ctx) if ctx else customMessage
            )

        loc = list(error['loc'])

        if loc and loc[-1]:
            translatedLoc = locTranslations.get(loc[-1], loc[-1])
            loc[-1] = translatedLoc

        error['loc'] = loc

        newErrors.append(error)
    return newErrors


def formatErrors(errorListUnformatted):
    """
    Formats a list of errors into an HTML unordered list.
    """
    errorList = convertErrors(errorListUnformatted,
                              CUSTOM_MESSAGES, LOC_TRANSLATIONS)
    errorItems = ''.join(
        f'<li class="list-group-item">{error["loc"][-1]}: {error["msg"]}</li>' for error in errorList)
    return f'<ul class="list-group">{errorItems}</ul>'


class CSRFProtectedForm(BaseModel):
    """
    Pydantic model for handling forms with CSRF protection.
    """
    csrfToken: Annotated[str, Field]

    @field_validator("csrfToken")
    # pylint: disable=no-self-argument
    def validateCsrfToken(cls, token):
        """
        Validates that the CSRF token matches the session's stored token.
        """

        # replace this with actual session token
        sessionCsrfToken = session.get("csrfToken")
        if token != sessionCsrfToken:
            abort(403)
            raise PydanticCustomError(
                'csrfToken',
                'csrfToken on väärä')
        return token


class LoginForm(BaseModel):
    """
    Pydantic model for handling the login form validation.
    """
    username: Annotated[str, StringConstraints(
        strip_whitespace=True, max_length=30)]
    password: Annotated[str, StringConstraints(max_length=30)]


class RegisterForm(BaseModel):
    """
    Pydantic model for handling the registration form validation.
    """
    username: Annotated[str, StringConstraints(
        strip_whitespace=True, min_length=3, max_length=30)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=30)]

    @field_validator('password')
    # pylint: disable=no-self-argument
    def validatePassword(cls, password):
        """
        Validates the password to ensure it meets the required complexity.
        """
        if not re.search(r'[A-Z]', password):
            raise PydanticCustomError(
                'Salasana',
                'Salasanan tulee sisältää ainakin yksi iso kirjain.')
        if not re.search(r'[a-z]', password):
            raise PydanticCustomError(
                'Salasana',
                'Salasanan tulee sisältää ainakin yksi pieni kirjain.')
        if not re.search(r'[0-9]', password):
            raise PydanticCustomError(
                'Salasana',
                'Salasanan tulee sisältää ainakin yksi numero.')
        return password


class UserEditForm(CSRFProtectedForm):
    """
    Pydantic model for handling the edit user form validation.
    """
    role: Annotated[int, Field(ge=2, le=3)]


class UserCreateForm(UserEditForm, RegisterForm):
    """
    Combines UserEditForm and RegisterForm
    """


class CompanyForm(CSRFProtectedForm):
    """
    Pydantic model for handling the company form validation.
    """

    companyName: Annotated[str, StringConstraints(
        strip_whitespace=True, min_length=3, max_length=30)]
    businessId: Annotated[str, StringConstraints(min_length=8, max_length=9)]
    notes: Optional[Annotated[str, StringConstraints(max_length=500)]]
    websiteUrl: Optional[Annotated[str, StringConstraints(max_length=75)]]
    email: Optional[Annotated[str, StringConstraints(max_length=75)]]
    phone: Optional[Annotated[str, StringConstraints(max_length=20)]]
    address: Optional[Annotated[str, StringConstraints(max_length=75)]]


class CompanyContactForm(CSRFProtectedForm):
    """
    Pydantic model for handling the company contact form validation.
    """
    firstName: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    lastName: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    email: Optional[Annotated[str, StringConstraints(max_length=50)]]
    phone: Optional[Annotated[str, StringConstraints(max_length=20)]]
