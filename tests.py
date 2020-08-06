import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_populate import days_till_bd, str_to_dt, clear_phone_nr
from models import Person, Base


class TestDB(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        DBSession = sessionmaker(bind=engine)
        self.sql_session = DBSession()
        Base.metadata.create_all(engine)
        new_person = Person(
            gender="male",
            title="MR",
            firstname="Lukasz",
            lastname="San",
            street_nr="10",
            street_name="Main",
            city="Gdańsk",
            state="Pomorskie",
            country="Poland",
            postcode="83-000",
            location_lat="50,03",
            location_lon="-20,12",
            time_offser="-",
            time_description="-",
            email="example@example.com",
            uuid="-",
            username="example",
            password="pw",
            salt="-",
            md5="-",
            sha1="-",
            sha256="-",
            dob=datetime(1991, 10, 29),
            days_to_bd=days_till_bd(datetime(1991, 10, 29)),
            age=29,
            registered_date=datetime(1995, 10, 29),
            registered_age=15,
            phone=clear_phone_nr("+123dad45-6==7da8/*-9."),
            cell=clear_phone_nr("+123dad45-6==7da8/*-9."),
            id_name="PLN",
            id_value="123",
            nationality="PL"
        )
        self.sql_session.add(new_person)

    def test_db_insert_data(self):
        """
        Testes if item is successfully added to in memory db
        :return:
        """
        result = self.sql_session.query(Person).all()
        self.assertEqual(len(result), 1)

    def test_db_data(self):
        result = self.sql_session.query(Person).one()
        self.assertEqual(result.gender, "male")
        self.assertEqual(result.city, "Gdańsk")
        self.assertEqual(result.phone, "123456789")
        self.assertEqual(type(result.dob), datetime)

    def tearDown(self):
        pass


class TestDBPopulate(unittest.TestCase):
    def setUp(self):
        self.dob1 = datetime(1991, 10, 29, 0, 0, 0)
        self.dob2 = datetime(2020, 11, 30, 0, 0, 0)

        self.str_dob1 = "1991-10-29T00:00:00.000Z"
        self.str_dob2 = "2020-11-30T00:00:00.000Z"
        self.str_dob3 = "2021-14-60T00:00:00.000Z"

        self.nr1 = "+42 -- 3213 -3123dasd f vcvxfafa [];';]p21a"
        self.nr2 = "54-89-2-985()da"

    def test_days_till_bd(self):
        self.assertEqual(days_till_bd(self.dob1), 84)
        self.assertEqual(days_till_bd(self.dob2), 116)
        self.assertEqual(type(days_till_bd(self.dob1)), int)

    def test_str_to_dt(self):
        self.assertEqual(str_to_dt(self.str_dob1), self.dob1)
        self.assertEqual(str_to_dt(self.str_dob2), self.dob2)
        self.assertEqual(type(str_to_dt(self.str_dob1)), datetime)
        self.assertRaises(ValueError, str_to_dt, self.str_dob3)

    def test_clear_phone_nr(self):
        self.assertEqual(clear_phone_nr(self.nr1), "423213312321")
        self.assertEqual(clear_phone_nr(self.nr2), "54892985")

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
