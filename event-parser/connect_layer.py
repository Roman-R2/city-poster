import settings
from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.orm import Session, registry
from sqlalchemy.sql import Select

mapper_registry = registry()
Base = mapper_registry.generate_base()

engine = create_engine(settings.DATABASE_CONNECTION, future=True)

connection = engine.connect()

session: Session = Session(engine)


class CompanyProfile(Base):
    __tablename__ = 'mainapp_companyprofile'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(512), nullable=False, unique=True)
    type = Column('type', String(512), nullable=False)
    address = Column('address', String(512), nullable=False)
    company_url = Column('company_url', String(256), nullable=False, unique=True)


print('Hello')
stmt: Select = select(CompanyProfile)

for user in session.scalars(stmt):
    print(user, user.name)

some_new = CompanyProfile(
    name='Some new',
    type='Some type',
    address='fsdgdfgfdgfdg',
    company_url='http://dddd.ru'
)

session.add(some_new)
session.commit()
