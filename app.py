from sqlalchemy import func, desc
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


def sqlalch_count_grouped(row, amount):
    result = sql_session.query(row, func.count(row).label("quantity"))\
        .group_by(row)\
        .order_by(desc("quantity"))\
        .limit(amount)\
        .all()
    return result


def most_common_cities(amount):
    popular_cities = sqlalch_count_grouped(Person.city, amount)

    print(f"Lista {amount} najczęściej występujących miast:")
    for city, count in popular_cities:
        print(f"\tMiasto: {city} - wystąpiło {count} razy")


def most_common_pw(amount):
    common_pw = sqlalch_count_grouped(Person.password, amount)

    print(f"Lista {amount} najczęściej występujących haseł:")
    for pw, count in common_pw:
        print(f"\tHasło: {pw} - użyto {count} razy")


if __name__ == "__main__":
    sql_session = session_creator()

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gender_proportion", action="store_true",
                        help="Returns gender proportions of the population")
    parser.add_argument("-a", "--average_age", choices=["total", "male", "female"], const="total", nargs="?",
                        help="Returns average age of the selected population from [male, female, total]. Default total")
    parser.add_argument("-c", "--common_cities", metavar="",
                        help="Returns number of most common cities")
    parser.add_argument("-p", "--common_password", metavar="",
                        help="Returns number of most common password")
    args = parser.parse_args()

    if args.gender_proportion:
        gender_proportions()
    if args.average_age:
        average_age(args.average_age)
    if args.common_cities:
        most_common_cities(args.common_cities)
    if args.common_password:
        most_common_pw(args.common_password)
