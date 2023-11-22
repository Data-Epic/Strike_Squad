#### Create dedicated database

- login to postgres local as root user: `sudo -u postgres psql` or `psql -U postgres` <br>  you will get this prompt: 

           
      psql (12.9 (Ubuntu 12.9-0ubuntu0.20.04.1))
      Type "help" for help.

      postgres=#
      
- create a new user: `CREATE USER <your user> WITH PASSWORD <'your_password'>;`

- create new database: `CREATE DATABASE <your_database_name>;`

- grant user priveleges on new database `GRANT ALL PRIVILEGES ON DATABASE <your_database_name> TO <your_username>;`
  

### The env variables in the `.env` file required
      SHEET_URL="https://docs.google.com/spreadsheets/d/1grKWiIQPgqg-KD2rJwRofl3odqsQc-GbLIed7KRPcb8/edit?usp=sharing"
      WORKSHEET_NAME="Sheet1"
      CREDENTIALS_PATH=<"your_credentials.json_path">
      DB_USER=<"your_db_username>
      DB_PASSWORD=<"your_db_password>
      DB_NAME=<"your_database_name">
      HOST="localhost"
      PORT="5432"

### Project Directory structure
      project-5
      .
      ├── credentials.json
      ├── exceptions.py
      ├── main.py
      ├── poetry.lock
      ├── __pycache__
      │   ├── exceptions.cpython-39.pyc
      │   └── utils.cpython-39.pyc
      ├── pyproject.toml
      ├── README.md
      └── utils.py

- `credentials.json`: Google cloud api keys
- `exceptions.py`: all error excention handling happens here
- `main.py`: our main script woud exist here
- `poetry.lock`: lock file for dependencies (recomended over toml file for installation)
- `pyproject.toml`: poetry project dependencies and meta-data
- `utils.py`: all helper funtions goes here


### for dev purpose only **⚠️**
- BBeaver console sample 
![BBeaver Table created](./static/dbeaver-dev.png)