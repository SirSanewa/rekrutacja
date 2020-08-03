from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    gender = Column(String(100))
    title = Column(String(100))
    firstname = Column(String(100))
    lastname = Column(String(100))
    street_nr = Column(String(100))
    street_name = Column(String(100))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postcode = Column(String(100))
    location_lat = Column(String(100))
    location_lon = Column(String(100))
    time_offser = Column(String(100))
    time_description = Column(String(100))
    email = Column(String(100))
    uuid = Column(String(100))
    username = Column(String(100))
    password = Column(String(100))
    salt = Column(String(100))
    md5 = Column(String(100))
    sha1 = Column(String(100))
    sha256 = Column(String(100))
    dob = Column(DateTime)
    days_to_bd = Column(Integer)
    age = Column(Integer)
    registered_date = Column(DateTime)
    registered_age = Column(Integer)
    phone = Column(String(100))
    cell = Column(String(100))
    id_name = Column(String(100))
    id_value = Column(String(100))
    nationality = Column(String(100))


if __name__ == '__main__':
    engine = create_engine('sqlite:///database.db')
    Base.metadata.create_all(engine)