from pydantic import BaseModel

class Product(BaseModel):
    code: int
    name: str
    price: float
    stock: int

class User(BaseModel):
    username: str
    password: str

class Employee(BaseModel):
    document: int
    name: str
    position: str
    salary: float