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


if __name__ == "__main__":
    sql_session = session_creator()
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gender_proportions", action="store_true",
                        help="Returns gender proportions of the population")

    args = parser.parse_args()
    if args.gender_proportions:
        gender_proportions()
