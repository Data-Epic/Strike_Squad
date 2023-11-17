install:
	# install dependencies
	pip install --upgrade pip &&\
		pip --default-timeout=1000 install -r project-3/requirements/base.txt 
format:
	# format python code with black
	black project-3/tests/unit/*.py project-3/cli.py project-3/exceptions.py project-3/main.py

lint:
	# check code syntaxes
	pylint --disable=R,C project-3/tests/unit/*.py project-3/cli.py project-3/exceptions.py project-3/main.py

# populate:
# 	# populate sheet1 with grocery_transactions data
# 	python3 cli.py --spread_sheet=ny_taxi_data \
# 		 --worksheet_name=taxi_2023_2 \
# 		 --email=bestnyah7@gmail.com \
# 		 --year=2023 \
# 		 --month=3 

# bash:
# 	# run extract bash script 
# 	chmod +x extract.sh &&\
# 		./extract.sh 2023 3

test:
	# run unit and integration tests
	pytest -s project-3/tests/unit/test_gspread_utility.py

poetry_test:
	# run unit test using poetry 
	poetry run pytest tests/unit/test_gspread_utility.py	

deploy:
	# deploy code to cloud


all: 
	# run in required order
	install format lint test populate 

