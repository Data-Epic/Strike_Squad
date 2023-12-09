# Project 6 (SQLAlchemy Database Integration)

## Overview
Project 6 revolves entirely around transferring data from a csv to a database. The dataset comprises of data from the uni-variate and bi-variate task given in week 4 in the Data-Epic mentorship program

The provided script in `main.py` which defines two database class, `Arts`, this class is for creating the table using SQLAlchemy ORM and `Artdb`, for extracting data from the CSV file, processes and validates the data while interacting with a SQLAlchemy ORM for ingestion. 

The `Artsdb` class contains the following methods:

- `read_data`: Extracts data from a CSV file.
- `data_ingeation`: Inserts data into the `arts_db` table from the extracted DataFrame.
- `data_validation`: Applies CHECK to ensure specific data types are met.


### Data source:
[CSV file](data/cleaned_data.csv)

![google sheets data sample](./static/data_example.png)

## Technologies used
- Bash
- SQLAlchemy ORM
- Python  <br>
  *Dependencies used:*
  - pandas: `^2.1.3`
  - sqlalchemy: `^2.0.23`
  - python-dotenv: `^1.0.0`


## Prerequisites
- Data from the Univariate and Bivariate task
- SQLAlchemy ORM for Database on localhost 
- Python3.9+ Intepreter
- Poetry `^1.7.1`

## Project build & setup 
___
- **setup development environment:** 
  - `poetry env use python3.9` 
  - `poetry install` 
<br>

- **Create dedicated database**

  - login to postgres local as root user: `sudo -u postgres psql` or `psql -U postgres` <br>  you will get this prompt: 

             
        psql (12.9 (Ubuntu 12.9-0ubuntu0.20.04.1))
        Type "help" for help.

        postgres=#
        
  - create a new user: `CREATE USER <your user> WITH PASSWORD <'your_password'>;`

  - create new database: `CREATE DATABASE <your_database_name>;`

  - grant user priveleges on new database `GRANT ALL PRIVILEGES ON DATABASE <your_database_name> TO <your_username>;`

<br>

- **Create and define required env variables in the `.env` file**
  
      connction = <postgresql://username:password@localhost:5432/database_name>

- **run `main.py` script from entry point with `poetry`**: `poetry run python3.9 main.py` 

### Project Directory structure
      project-6
      .
      ├── data
      │   └──cleaned_data.csv
      ├── exceptions.py
      ├── main.py
      ├── poetry.lock
      ├── pyproject.toml
      ├── README.md
      ├── static
      │   └──data_example.png
      └── test_main.py

- `exceptions.py`: all error exception handling happens here
- `main.py`: main script exists here
- `poetry.lock`: lock file for dependencies (recomended over toml file for installation)
- `pyproject.toml`: poetry project dependencies and meta-data
- `test_main.py`: all pytest functions in this file

## Results
![Query to fetch all items from DB](static/query5.png)

![Query to fetch department in order of most occurring to least occurring from DB](static/query4.png)

![Query to fetch title, date_acquired, artist from DB](static/query3.png)

![Query to fetch height greater than 50cm from DB](static/query2.png)

![Query to fetch artist in order of most occurring to least occurring from DB](static/query1.png)
<!-- ### for dev purpose only **⚠️**
- BBeaver console sample 
![BBeaver Table created](./static/dbeaver-dev.png) -->