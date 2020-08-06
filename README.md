# Recruitment task for Profile Software
## 1. Running script
### Step 1
Run file `models.py`, which will create SQLite database.
### Step 2
Run file `db_populate.py`, which will fill database with data collected from API.
### Step 3
Run file `app.py` in terminal to execute selected commands.
## 2. Available commands
Use `/app.py` with available commands:
- `-h, --help` - help menu,
- `-g, --gender_proportion` - Gender proportions in given population,
- `-a POPULATION, --average_age POPULATION` - Average age of given population. `POPULATION` to be chosen from `["total", "male", "female"]`. If none selected, default value is `total`,
- `-c N, --common_cities N` - `N`-long list of most common cities, with number of appearances,
- `-p N, --common_password N` - `N`-long list of most commonly used passwords, with number of appearances,
- `born_between` - List of people born between `START_DAT` and `END_DATE`. Both dates are required. 
    Example use: `app.py born_between -s 2000-10-10 -e 2000-11-11`:
    - `-s START_DATE, --start_date START_DATE` - Start date(YYYY-MM-DD),
    - `-e END_DATE, --end_date END_DATE` - End date(YYYY-MM-DD),
- `-s, --safest_password` - Safest password in database and it's score.
## 3. Additional information
- Correctly created database will include 1000 randomly generated persons,
- Passwords will include from 1 to 16 characters(small and large letters, digits and special characters),
- List of all required plug-ins is available in `requirement.txt` file.
## 4. Author data and contact
Łukasz Sanewski 
email: lukaszsanewski@gmail.com