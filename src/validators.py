import sys
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field, StringConstraints, field_validator
import re

def formatErrors(error_list):
    return ''.join(f'<li>{error["loc"][-1]}: {error["msg"]}</li>' for error in error_list)

class LoginForm(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, max_length=30)]
    password: Annotated[str, StringConstraints(max_length=30)]

class RegisterForm(BaseModel):
    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=30)]
    password: Annotated[str, StringConstraints(min_length=8, max_length=30)]

    @field_validator('password')
    def validate_password(cls, password):
        if not re.search(r'[A-Z]', password):
            raise ValueError('password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password):
            raise ValueError('password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', password):
            raise ValueError('password must contain at least one digit.')
        return password
    
class CompanyForm(BaseModel):
    id: Annotated[int, Field(ge=0, le=sys.maxsize)]
    companyName: Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=30)]
    businessId: Optional[Annotated[str, StringConstraints(min_length=8, max_length=9)]]
    notes: Optional[Annotated[str, StringConstraints(max_length=500)]]
    websiteUrl: Optional[Annotated[str, StringConstraints(max_length=75)]]
    email: Optional[Annotated[str, StringConstraints(max_length=75)]]
    phone: Optional[Annotated[str, StringConstraints(max_length=20)]]
    address: Optional[Annotated[str, StringConstraints(max_length=75)]]