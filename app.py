from sqlalchemy import func, desc
from models import Person
from session import session_creator
import argparse
from datetime import datetime


def percentage(number, total):
    """
    Calculates and returns percentage value from given number and total amount.
    :param number: int
    :param total: int
    :return: percentage: int
    """
    return (number * 100) / total


def gender_proportions():
    """
    Prints gender proportions of db population.
    :return:
    """
    total_rows = sql_session.query(Person) \
        .count()

    men = sql_session.query(Person) \
        .filter(Person.gender == "male") \
        .count()

    women = sql_session.query(Person) \
        .filter(Person.gender == "female") \
        .count()

    men_percent = percentage(men, total_rows)
    women_percent = percentage(women, total_rows)
    print(f"Gender proportions are: \n\t-{men_percent}% men({men} total)\n\t-{women_percent}% women({women} total).")


def average_age(option="total"):
    """
    Prints average age depending on option chosen from {'total', 'male', 'female'}. Default 'total'.
    Raises Value Error if option other then allowed.
    :param option: str, default 'total'
    :return:
    """
    populations = {"total", "male", "female"}
    if option not in populations:
        raise ValueError("Used unsupported population")

    if option == "total":
        age_avg = sql_session.query(func.avg(Person.age))\
            .scalar()
    else:
        age_avg = sql_session.query(func.avg(Person.age))\
            .filter(Person.gender == option)\
            .scalar()

    if age_avg.is_integer():
        age_avg = int(age_avg)
    else:
        age_avg = round(age_avg, 2)
    print(f"Average age for the selected population({option}) is {age_avg} years.")


def sqlalch_count_grouped(attribute, amount):
    """
    Counts grouped rows from db by given attribute.
    :param attribute: class: sqlalchemy.orm.attributes.InstrumentedAttribute
    :param amount: int
    :return: result: list
    """
    result = sql_session.query(attribute, func.count(attribute).label("quantity")) \
        .group_by(attribute) \
        .order_by(desc("quantity")) \
        .limit(amount) \
        .all()
    return result


def most_common_cities(amount):
    """
    Prints number of most common cities from db with number they appear. Used sqlalch_count_grouped().
    :param amount: int
    :return:
    """
    print(type(Person.city))
    popular_cities = sqlalch_count_grouped(Person.city, amount)

    print(f"Lista {amount} najczęściej występujących miast:")
    for city, count in popular_cities:
        print(f"\tMiasto: {city} - wystąpiło {count} razy")


def most_common_pw(amount):
    """
    Prints number of most common passwords from db with number they appear. Used sqlalch_count_grouped().
    :param amount: int
    :return:
    """
    common_pw = sqlalch_count_grouped(Person.password, amount)

    print(f"Lista {amount} najczęściej występujących haseł:")
    for pw, count in common_pw:
        print(f"\tHasło: '{pw}' - użyto {count} razy")


def str_to_datetime(date_str):
    """
    Converts date string to datetime object.
    :param date_str: str
    :return: datetime object
    """
    return datetime.strptime(date_str, "%Y-%m-%d")


def born_between(str_start, str_end):
    """
    Prints all people (firstnames, lastnames and d.o.b.) from db that were born between given dates.
    Dates are given as string and converted to datetime with str_to_datetime(). Raises ValueError if start date is
    bigger then end date.
    :param str_start: str
    :param str_end: str
    :return:
    """
    date_start = str_to_datetime(str_start)
    date_end = str_to_datetime(str_end)

    if date_start > date_end:
        raise ValueError("Wprowadzono niepoprawne daty")

    results = sql_session.query(Person) \
        .filter(Person.dob >= date_start) \
        .filter(Person.dob <= date_end) \
        .order_by(Person.dob) \
        .all()
    print(f"Liczba {len(results)} osób urodzonych pomiędzy {str_start} a {str_end}:")
    for person in results:
        print(f"\t- {person.firstname} {person.lastname}, date of birth: {datetime.strftime(person.dob, '%Y-%m-%d')}")


def password_safety_score(password):
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


def safest_password():
    """
    Uses password_safety_score() to print the most secure password from db and it's score.
    :return:
    """
    result = sql_session.query(Person.password).all()
    best_result = max((password_safety_score(row.password), row.password)for row in result)
    best_score = best_result[0]
    best_password = best_result[1]
    print(f"Najbezpieczniejsze hasło zdobyło {best_score} punktów i brzmi: '{best_password}'.")


def main():
    """
    Creates parser, collects arguments and runs appropriate functions.
    :return:
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="born_between")

    dates_parser = subparsers.add_parser("born_between", help="Return all people born between given dates")

    dates_parser.add_argument("-s", "--start_date", action="store", metavar="", required=True,
                              help="Start date in format YYYY-MM-DD for born_between")
    dates_parser.add_argument("-e", "--end_date", action="store", metavar="", required=True,
                              help="End date in format YYYY-MM-DD for born_between")

    parser.add_argument("-g", "--gender_proportion", action="store_true",
                        help="Returns gender proportions of the population")
    parser.add_argument("-a", "--average_age", choices=["total", "male", "female"], const="total", nargs="?",
                        help="Returns average age of the selected population from [male, female, total]. Default total")
    parser.add_argument("-c", "--common_cities", metavar="",
                        help="Returns number of most common cities")
    parser.add_argument("-p", "--common_password", metavar="",
                        help="Returns number of most common password")
    parser.add_argument("-s", "--safest_password", action="store_true",
                        help="Returns the safest password")

    args = parser.parse_args()

    if args.gender_proportion:
        gender_proportions()
    if args.average_age:
        average_age(args.average_age)
    if args.common_cities:
        most_common_cities(args.common_cities)
    if args.common_password:
        most_common_pw(args.common_password)
    if args.safest_password:
        safest_password()
    if args.born_between:
        if args.start_date and args.end_date:
            born_between(args.start_date, args.end_date)


if __name__ == "__main__":
    sql_session = session_creator()
    main()

# TODO: README
