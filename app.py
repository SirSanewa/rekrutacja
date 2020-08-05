from sqlalchemy import func

from models import Person
from session import session_creator
import argparse


def percentage(number, total):
    return (number * 100)/total


def gender_proportions():
    total_rows = sql_session.query(Person)\
        .count()

    men = sql_session.query(Person)\
        .filter(Person.gender == "male")\
        .count()

    women = sql_session.query(Person)\
        .filter(Person.gender == "female")\
        .count()

    men_percent = percentage(men, total_rows)
    women_percent = percentage(women, total_rows)
    print(f"Gender proportions are: \n\t-{men_percent}% men({men} total)\n\t-{women_percent}% women({women} total).")


def average_age(option="total"):
    populations = {"total", "male", "female"}
    if option not in populations:
        raise ValueError("Used unsupported population")

    if option == "total":
        age_avg = sql_session.query(func.avg(Person.age)).scalar()
    else:
        age_avg = sql_session.query(func.avg(Person.age)).filter(Person.gender == option).scalar()

    if age_avg.is_integer():
        age_avg = int(age_avg)
    else:
        age_avg = round(age_avg, 2)
    print(f"Average age for the selected population({option}) is {age_avg} years.")


if __name__ == "__main__":
    sql_session = session_creator()

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gender_proportion", action="store_true",
                        help="Returns gender proportions of the population")
    parser.add_argument("-a", "--average_age", choices=["total", "male", "female"], const="total", nargs="?",
                        help="Returns average age of the selected population from [male, female, total]. Default total")

    args = parser.parse_args()

    if args.sex_proportion:
        gender_proportions()
    if args.average_age:
        average_age(args.average_age)
