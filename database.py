from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DB_URL="postgresql://postgres:postgres@localhost:5432/greenlit"
DB_URL='postgresql://ujwxfyrh:IHsQGSgsAEYjeFLfgyVJ_08kInRWRU17@abul.db.elephantsql.com/ujwxfyrh'
engine=create_engine(DB_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()
