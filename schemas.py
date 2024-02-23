from typing import Optional
from pydantic import BaseModel
from typing import List

class AddUserReq(BaseModel):
    first_name:str
    last_name:str
    email:str
    minimum_fee:int

class AddCompanyReq(BaseModel):
    name:str
    contact_email_address:str
    phone_number:str

class AddFilmReq(BaseModel):
    title:str
    description:str
    budget:int
    release_year:int
    genres:List[str]
    company_id:Optional[str]
    company_name:Optional[str]

class UpdateFilmDetailsReq(BaseModel):
    film_id:int
    title:Optional[str]=None
    description:Optional[str]=None
    budget:Optional[int]=None
    release_year:Optional[int]=None
    genres:Optional[List[str]]=None
    company_id:Optional[int]=None

class AddUserRoleToFilmReq(BaseModel):
    user_id:int
    film_id:int
    role:str

class AddUserRoleToCompanyReq(BaseModel):
    user_id:int
    company_id:int
    role:str
