''' payload
{
  "person": {
    "cpf": "09762022637",
    "name": "Carlos Roberto",
    "email": "carlosjr.if@gmail.com",
    "birth_date": "1995-04-03"
  },
  "user": {
    "name": "carlos.roberto",
    "password": "Carlos@123"
  }
}
'''
from pydantic import BaseModel


class PersonDTO(BaseModel):
    cpf: str
    name: str
    email: str
    birth_date: str


class UserDTO(BaseModel):
    name: str
    password: str


class SignUpDTO(BaseModel):
    person: PersonDTO
    user: UserDTO


__all__ = ["SignUpDTO"]

