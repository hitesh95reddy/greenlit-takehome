from fastapi import FastAPI,Depends
from sqlalchemy import func, or_
from database import SessionLocal
from schemas import AddUserReq,AddCompanyReq,AddFilmReq,UpdateFilmDetailsReq
from schemas import AddUserRoleToCompanyReq,AddUserRoleToFilmReq
from models import User,Film,Company,UserFilm,UserCompany

from models import Base
from database import engine
Base.metadata.create_all(bind=engine)
app=FastAPI()

@app.get("/")
def root():
    return {"msg":"greenlit services"}

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/addUser')
def addUser(addUserReq:AddUserReq,db=Depends(get_db)):
    new_user=User(first_name=addUserReq.first_name,
                  last_name=addUserReq.last_name,
                  email=addUserReq.email,
                  minimum_fee=addUserReq.minimum_fee)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        return {"err":f"User Not Added: {e}"}
    return {"msg":"user added successfully",
            "user_id":new_user.user_id
            }

@app.get('/getUser/{user_id}')
def getUserDetails(user_id:int,db=Depends(get_db)):
    user=db.query(User).filter(User.user_id==user_id).first()
    if user:
        return user
    return {"err":"User Not Found"}

@app.get('/allUsers')
def getAllUsers(db=Depends(get_db)):
    return db.query(User).all()

@app.get('/getUserbyName/{name}')
def getUsersbyName(name:str,db=Depends(get_db)):
    users = db.query(User).filter(or_(func.lower(User.first_name).contains(name.lower()), 
                                        func.lower(User.last_name).contains(name.lower()))).all()
    return users

@app.put('/updateUserDetails/{user_id}')
def updateUser(user_id:int,addUserReq:AddUserReq,db=Depends(get_db)):
    user=db.query(User).filter(User.user_id==user_id).first()
    if user:
        user.first_name=addUserReq.first_name
        user.last_name=addUserReq.last_name
        user.email=addUserReq.email
        user.minimum_fee=addUserReq.minimum_fee
        db.commit()
        return {"msg":"User Updated Successfully"}
    return {"err":"User Not Found"}

@app.delete('/deleteUser/{user_id}')
def deleteUser(user_id:int,db=Depends(get_db)):
    user=db.query(User).filter(User.user_id==user_id).first()

    if user:
        
        user_films=db.query(UserFilm).filter(UserFilm.user_id==user_id).all()
        for user_film in user_films:
            db.delete(user_film)
        
        user_companies=db.query(UserCompany).filter(UserCompany.user_id==user_id).all()
        for user_company in user_companies:
            db.delete(user_company)
        db.delete(user)

        db.commit()
        return {"msg":"User Deleted Successfully"}
    return {"err":"User Not Found"}

@app.post('/addCompany')
def addCompany(addCompanyReq:AddCompanyReq,db=Depends(get_db)):
    new_company=Company(name=addCompanyReq.name,
                        contact_email_address=addCompanyReq.contact_email_address,
                        phone_number=addCompanyReq.phone_number)
    try:
        db.add(new_company)
        db.commit()
        db.refresh(new_company)
    except Exception as e:
        return {"err":f"Company Not Added: {e}"}
    return {"msg":"Company added successfully",
            "company_id":new_company.company_id
            }

@app.get('/getCompany/{company_id}')
def getCompanyDetails(company_id:int,db=Depends(get_db)):
    company=db.query(Company).filter(Company.company_id==company_id).first()
    if company:
        return company
    return {"err":"Company Not Found"}

@app.get('/allCompanies')
def getAllCompanies(db=Depends(get_db)):
    return db.query(Company).all()

@app.get('/getCompanybyName/{name}')
def getCompanybyName(name:str,db=Depends(get_db)):
    companies = db.query(Company).filter(func.lower(Company.name).contains(name.lower())).all()
    return companies

@app.put('/updateCompanyDetails/{company_id}')
def updateCompany(company_id:int,addCompanyReq:AddCompanyReq,db=Depends(get_db)):
    company=db.query(Company).filter(Company.company_id==company_id).first()
    if company:
        company.name=addCompanyReq.name
        company.contact_email_address=addCompanyReq.contact_email_address
        company.phone_number=addCompanyReq.phone_number
        db.commit()
        return {"msg":"Company Updated Successfully"}
    return {"err":"Company Not Found"}

@app.delete('/deleteCompany/{company_id}')
def deleteCompany(company_id:int,db=Depends(get_db)):
    company=db.query(Company).filter(Company.company_id==company_id).first()
    if company:
        films=db.query(Film).filter(Film.company_id==company_id).all()
        for film in films:
            db.delete(film)
        db.delete(company)
        db.commit()
        return {"msg":"Company Deleted Successfully"}
    return {"err":"Company Not Found"}

@app.post('/addFilm')
def addFilm(addFilmReq:AddFilmReq,db=Depends(get_db)):
    new_film=None
    if addFilmReq.company_id:
        company=db.query(Company).filter(Company.company_id==addFilmReq.company_id).first()
        if not company:
            return {"err":"Company Not Found"}
        else:
            new_film=Film(title=addFilmReq.title,
                          description=addFilmReq.description,
                          budget=addFilmReq.budget,
                          release_year=addFilmReq.release_year,
                          genres=",".join(addFilmReq.genres),
                          company_id=addFilmReq.company_id)
    elif addFilmReq.company_name:
        company=db.query(Company).filter(func.lower(Company.name)==addFilmReq.company_name.lower()).first()
        if not company:
            return {"err":"Company Not Found"}
        else:
            new_film=Film(title=addFilmReq.title,
                          description=addFilmReq.description,
                          budget=addFilmReq.budget,
                          release_year=addFilmReq.release_year,
                          genres=",".join(addFilmReq.genres),
                          company_id=company.company_id)
    elif not addFilmReq.company_id and not addFilmReq.company_name:
        new_film=Film(title=addFilmReq.title,
                      description=addFilmReq.description,
                      budget=addFilmReq.budget,
                      release_year=addFilmReq.release_year,
                      genres=",".join(addFilmReq.genres))
    if new_film:
        try:
            db.add(new_film)
            db.commit()
            db.refresh(new_film)
        except Exception as e:
            return {"err":f"Film Not Added: {e}"}
        return {"msg":"Film added successfully",
                "film_id":new_film.film_id
                }

@app.get('/getFilm/{film_id}')
def getFilmDetails(film_id:int,db=Depends(get_db)):
    film=db.query(Film).filter(Film.film_id==film_id).first()
    if film:
        return film
    return {"err":"Film Not Found"}

@app.get('/getAllFilms')
def getAllFilms(db=Depends(get_db)):
    return db.query(Film).all()    

@app.get('/getFilmbyTitle/{title}')
def getFilmbyTitle(title:str,db=Depends(get_db)):
    films = db.query(Film).filter(func.lower(Film.title).contains(title.lower())).all()
    return films

@app.put('/updateFilmDetails/{film_id}')
def updateFilmDetails(updateFilmDetailsReq:UpdateFilmDetailsReq,db=Depends(get_db)):
    film=db.query(Film).filter(Film.film_id==updateFilmDetailsReq.film_id).first()
    if film:
        if updateFilmDetailsReq.title:
            film.title=updateFilmDetailsReq.title
        if updateFilmDetailsReq.description:
            film.description=updateFilmDetailsReq.description
        if updateFilmDetailsReq.budget:
            film.budget=updateFilmDetailsReq.budget
        if updateFilmDetailsReq.release_year:
            film.release_year=updateFilmDetailsReq.release_year
        if updateFilmDetailsReq.genres:
            film.genres=",".join(updateFilmDetailsReq.genres)
        if updateFilmDetailsReq.company_id:
            company=db.query(Company).filter(Company.company_id==updateFilmDetailsReq.company_id).first()
            if company:
                film.company_id=updateFilmDetailsReq.company_id
            else:
                return {"err":"Invalid Company Details Provided"}
        db.commit()
        return {"msg":"Film Updated Successfully"}
    return {"err":"Film Not Found"}

@app.delete('/deleteFilm/{film_id}')
def deleteFilm(film_id:int,db=Depends(get_db)):
    film=db.query(Film).filter(Film.film_id==film_id).first()
    if film:
        user_films=db.query(UserFilm).filter(UserFilm.film_id==film_id).all()
        for user_film in user_films:
            db.delete(user_film)
        db.delete(film)
        db.commit()
        return {"msg":"Film Deleted Successfully"}
    return {"err":"Film Not Found"}

@app.post('/addUserRoleToFilm')
def addUserRoleToFilm(addUserRoleToFilmReq:AddUserRoleToFilmReq,db=Depends(get_db)):
    user=db.query(User).filter(User.user_id==addUserRoleToFilmReq.user_id).first()
    film=db.query(Film).filter(Film.film_id==addUserRoleToFilmReq.film_id).first()
    if user and film:
        user_role_film=db.query(UserFilm).filter(UserFilm.user_id==addUserRoleToFilmReq.user_id,
                                                UserFilm.film_id==addUserRoleToFilmReq.film_id,
                                                UserFilm.role==addUserRoleToFilmReq.role).first()
        if user_role_film:
            return {"err":"User Role Already Exists"}
        user_film=UserFilm(user_id=addUserRoleToFilmReq.user_id,
                           film_id=addUserRoleToFilmReq.film_id,
                           role=addUserRoleToFilmReq.role)
        try:
            db.add(user_film)
            db.commit()
            db.refresh(user_film)
        except Exception as e:
            return {"err":f"User Role Not Added: {e}"}
        return {"msg":"User Role added successfully",
                "user_film_id":user_film.id
                }
    return {"err":"Invalid User or Film Details Provided"}

@app.post('/addUserRoleToCompany')
def addUserRoleToCompany(addUserRoleToCompanyReq:AddUserRoleToCompanyReq,db=Depends(get_db)):
    user=db.query(User).filter(User.user_id==addUserRoleToCompanyReq.user_id).first()
    company=db.query(Company).filter(Company.company_id==addUserRoleToCompanyReq.company_id).first()
    if user and company:
        user_role_company=db.query(UserCompany).filter(UserCompany.user_id==addUserRoleToCompanyReq.user_id,
                                                       UserCompany.company_id==addUserRoleToCompanyReq.company_id,
                                                       UserCompany.role==addUserRoleToCompanyReq.role).first()
        if user_role_company:
            return {"err":"User Role Already Exists"}
        user_company=UserCompany(user_id=addUserRoleToCompanyReq.user_id,
                                 company_id=addUserRoleToCompanyReq.company_id,
                                 role=addUserRoleToCompanyReq.role)
        try:
            db.add(user_company)
            db.commit()
            db.refresh(user_company)
        except Exception as e:
            return {"err":f"User Role Not Added: {e}"}
        return {"msg":"User Role added successfully",
                "user_company_id":user_company.id
                }
    return {"err":"Invalid User or Company Details Provided"}
