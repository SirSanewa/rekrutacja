from datetime import datetime

import requests
from models import Person
from session import session_creator


def days_till_bd(dob):
    now = datetime.now()
    month = dob.month
    day = dob.day
    bd_date = datetime(year=now.year, month=month, day=day)
    if bd_date < now:
        bd_date = datetime(year=now.year + 1, month=10, day=29)
    days_diff = bd_date - now
    return days_diff.days + 1


def clear_phone_nr(phone_nr):
    only_digits_nr = "".join([char for char in phone_nr if char.isdigit()])
    return only_digits_nr


def populate_db():
    people = []
    url = "https://randomuser.me/api/?results=1000"

    response = requests.get(url)
    data = response.json()

    for person in data["results"]:


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
            password=person["login"]["password"],
            salt=person["login"]["salt"],
            md5=person["login"]["md5"],
            sha1=person["login"]["sha1"],
            sha256=person["login"]["sha256"],
            dob=person["dob"]["date"],
            days_to_bd=days_till_bd(person["dob"]["date"]),
            age=person["dob"]["age"],
            registered_date=person["registered"]["date"],
            registered_age=person["registered"]["age"],
            phone=clear_phone_nr(person["phone"]),
            cell=clear_phone_nr(person["cell"]),
            id_name=person["id"]["name"],
            id_value=person["id"]["value"],
            nationality=person["nat"]
        ))
    session_sql.bulk_save_objects(people)


if __name__ == "__main__":
    session_sql = session_creator()
    populate_db()
    session_sql.commit()
