install: 
	pip install -e .        

config:
	export FLASK_APP=main.py

run:
	flask run
