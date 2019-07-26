#Champions league test project
Flask API which allows basic management of scores and ranking.

###Prerequisites
In order to run this code, you will need to have Python 3.7 and PostgreSQL database up and running.

###Installation (Windows dev environment)
* Install PostgreSQL with PgAdmin from this link: https://www.postgresql.org/download/windows/
* Create database with title of your choosing and change DB connection details in: config/dev.py config file.
* Install packages needed for running this code by PIP installing requirements.txt file.
* Run the app from root folder: python application.py
* Run the unit test by executing tests.py script in test directory.

```
Code is written by following PEP-8 standard, this is standard for pure Python and sometimes has conflicts
with how Flask is designed. Feel free to Pylint the code to check its quality but please note that __init__py in
championship module must have the import of routes at the end of the file.
```

###Routes
* url/api/fixture/result/publish, method: POST
```
Json data:
[
    {
        "leagueTitle": "Champions league 2018/19",
        "matchday": 1,
        "group": "B",
        "homeTeam": "Partizan",
        "awayTeam": "Zvezda",
        "kickoffAt": "2018-12-07T20:45:00",
        "score": "2:2"
    },
    {
        "leagueTitle": "Champions league 2018/19",
        "matchday": 2,
        "group": "B",
        "homeTeam": "Dinamo",
        "awayTeam": "Alanja",
        "kickoffAt": "2018-11-07T20:45:00",
        "score": "3:2"
    }
]
```

* url/api/table/<string:mode>, method: GET
```
mode: all|specific
if mode specific, json data:
[{
    "leagueName": "Champions league 2018/19",
    "group": "B"
},
{
    "leagueName": "Champions league 2016/17",
    "group": "A"
}]

```

* url/api/fixture/result/filter, methods: GET|POST
```
If you want to exclude a filter, just exclude it from json.
{
    "team": "Bagdad",
    "group": "B",
    "date_from": "2018-11-08T20:45:00",
    "date_to": "2019-11-08T20:45:00"
}
```

* url/api/result/update, methods: PUT
```
Json to send:
{
    "id": 553,
    "score": "2:2"
}
```
