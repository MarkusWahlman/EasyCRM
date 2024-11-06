import sys
from typing import Dict, List, Optional
from pydantic_core import ErrorDetails, PydanticCustomError
from typing_extensions import Annotated
from pydantic import BaseModel, Field, StringConstraints, ValidationError, field_validator
import re

CUSTOM_MESSAGES = {
    'string_too_long': 'Syöttämäsi merkkijono on liian pitkä.',
    'string_too_short': 'Syöttämäsi merkkijono on liian lyhyt.',
}

LOC_TRANSLATIONS = {
    'username': 'Käyttäjätunnus',
    'password': 'Salasana',
    'businessId': 'Y-tunnus',
    'companyName': 'Yrityksen nimi',
}

def convert_errors(
    e: ValidationError, custom_messages: Dict[str, str], loc_translations: Dict[str, str]
) -> List[ErrorDetails]:
    new_errors: List[ErrorDetails] = []
    for error in e:
        custom_message = custom_messages.get(error['type'])
        if custom_message:
            ctx = error.get('ctx')
            error['msg'] = (
                custom_message.format(**ctx) if ctx else custom_message
            )

        loc = list(error['loc'])

        if loc and loc[-1]:
            translated_loc = loc_translations.get(loc[-1], loc[-1])
            loc[-1] = translated_loc

        error['loc'] = loc

        new_errors.append(error)
    return new_errors

def formatErrors(errorListUnformatted):
    errorList = convert_errors(errorListUnformatted, CUSTOM_MESSAGES, LOC_TRANSLATIONS)
    error_items = ''.join(f'<li class="list-group-item">{error["loc"][-1]}: {error["msg"]}</li>' for error in errorList)
    return f'<ul class="list-group">{error_items}</ul>'

class LoginForm(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, max_length=30)]
    password: Annotated[str, StringConstraints(max_length=30)]

class RegisterForm(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=30)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=30)]

    @field_validator('password')
    def validate_password(cls, password):
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
    
class CompanyForm(BaseModel):
    companyName: Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=30)]
    businessId: Optional[Annotated[str, StringConstraints(min_length=8, max_length=9)]]
    notes: Optional[Annotated[str, StringConstraints(max_length=500)]]
    websiteUrl: Optional[Annotated[str, StringConstraints(max_length=75)]]
    email: Optional[Annotated[str, StringConstraints(max_length=75)]]
    phone: Optional[Annotated[str, StringConstraints(max_length=20)]]
    address: Optional[Annotated[str, StringConstraints(max_length=75)]]

class CompanyContactForm(BaseModel):
    firstName: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    lastName: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    email: Optional[Annotated[str, StringConstraints(max_length=50)]]
    phone: Optional[Annotated[str, StringConstraints(max_length=20)]]