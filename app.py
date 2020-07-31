import requests


def api_data():
    url = "https://randomuser.me/api/?results=1000"

    response = requests.get(url)
    data = response.json()
    x = data["results"][0]
    gender = x["gender"]
    name = x["name"]
    print(type(x))
    print(name)
    print(gender)


if __name__ == "__main__":
    api_data()
