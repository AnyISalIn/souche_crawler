from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime

from souche_crawler import constants as C

Base = declarative_base()
engine = create_engine(C.DB_URL)
Session = sessionmaker(bind=engine)
session = Session()


class Car(Base):

    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    price = Column(String(200))
    first_register = Column(DateTime)
    driver_mile = Column(String(200))
    location = Column(String(200))
    emission_standard = Column(String(200))
    car_id = Column(String(200), unique=True)
    contact = Column(String(100))

    def __repr__(self):
        return '<Car {}>'.format(self.name)
