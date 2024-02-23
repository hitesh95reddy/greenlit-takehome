from database import Base
from sqlalchemy import Column,Integer,String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"

    user_id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String)
    last_name=Column(String)
    email=Column(String,unique=True,index=True)
    minimum_fee = Column(Integer)

class Film(Base):
    __tablename__ = "films"

    film_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    budget = Column(Integer)
    release_year = Column(Integer)
    genres = Column(String)
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    company = relationship("Company", back_populates="films")


class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contact_email_address = Column(String)
    phone_number = Column(String)
    films = relationship("Film", back_populates="company")

class UserFilm(Base):
    __tablename__ = "user_films"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    film_id = Column(Integer, ForeignKey("films.film_id"))
    role = Column(String)

class UserCompany(Base):
    __tablename__ = "user_companies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    role = Column(String)
