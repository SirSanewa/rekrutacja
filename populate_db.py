from datetime import datetime
import requests
from models import Person
from session import session_creator


def days_till_bd(dob):
    """
    Calculates number of days till next birthday from given d.o.b. and return it as an int
    :param dob: datetime object of d.o.b.
    :return: number of days till next birthday(int)
    """
    now = datetime.now()
    month = dob.month
    day = dob.day
    bd_date = datetime(year=now.year, month=month, day=day)
    if bd_date < now:
        # to cover February 29th and change it to February 28th
        try:
            bd_date = datetime(year=now.year + 1, month=month, day=day)
        except ValueError:
            bd_date = datetime(year=now.year + 1, month=month, day=day - 1)
    diff = bd_date - now
    return diff.days + 1


def clear_phone_nr(phone_nr):
    """
    Clears phone number str from all characters that are not digits and returns it as a str.
    :param phone_nr: str
    :return: digits only phone number as str
    """
    only_digits_nr = "".join([char for char in phone_nr if char.isdigit()])
    return only_digits_nr


def str_to_dt(str_date):
    """
    Converts str representation of date in ISO8601 format to datetime object.
    :param str_date: str
    :return: datetime object
    """
    return datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%S.%fZ")


def password_safety(password):
    """
    Calculates password's safety and returns score as an int.
    :param password: str
    :return: score int
    """
    pts = 0
    str_func_list = [
        {"function": str.islower, "points": 1},
        {"function": str.isupper, "points": 2},
        {"function": str.isdigit, "points": 1},
    ]
    for element in str_func_list:
        if sum(map(element["function"], password)) >= 1:
            pts += element["points"]
    if len(password) >= 8:
        pts += 5
    if not str.isalnum(password):
        pts += 3
    return pts


def populate_db():
    """
    Connects to API to get required data and populates the db.
    :return:
    """
    people = []
    url = "https://randomuser.me/api/?results=1000&password=upper,lower,number,special,1-16&exc=picture&noinfo"

    response = requests.get(url)
    data = response.json()
    for person in data["results"]:
        dob = str_to_dt(person["dob"]["date"])
        password = person["login"]["password"]
        people.append(Person(
            gender=person["gender"],
            title=person["name"]["title"],
            firstname=person["name"]["first"],
            lastname=person["name"]["last"],
            street_nr=person["location"]["street"]["number"],
            street_name=person["location"]["street"]["name"],
            city=person["location"]["city"],
            state=person["location"]["state"],
            country=person["location"]["country"],
            postcode=person["location"]["postcode"],
            location_lat=person["location"]["coordinates"]["latitude"],
            location_lon=person["location"]["coordinates"]["longitude"],
            time_offser=person["location"]["timezone"]["offset"],
            time_description=person["location"]["timezone"]["description"],
            email=person["email"],
            uuid=person["login"]["uuid"],
            username=person["login"]["username"],
            password=password,
            password_strenght=password_safety(password),
            salt=person["login"]["salt"],
            md5=person["login"]["md5"],
            sha1=person["login"]["sha1"],
            sha256=person["login"]["sha256"],
            dob=dob,
            days_to_bd=days_till_bd(dob),
            age=person["dob"]["age"],
            registered_date=str_to_dt(person["registered"]["date"]),
            registered_age=person["registered"]["age"],
            phone=clear_phone_nr(person["phone"]),
            cell=clear_phone_nr(person["cell"]),
            id_name=person["id"]["name"],
            id_value=person["id"]["value"],
            nationality=person["nat"]
        ))
    session_sql.bulk_save_objects(people)

# TODO: __repr__


if __name__ == "__main__":
    session_sql = session_creator()
    populate_db()
    session_sql.commit()

# TODO: testy
