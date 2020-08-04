from models import Person
from session import session_creator
from sqlalchemy.sql import func


def gender_proportions():
    # men = sql_session.query_with_entities(func.count(Person.gender)).scalar()
    # print(men)

    women = sql_session.query(Person)\
        .filter(Person.gender == "female")\
        .all()

    print(len(women))


if __name__ == "__main__":
    sql_session = session_creator()
    gender_proportions()
