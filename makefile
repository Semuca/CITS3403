# Makefile with some common commands for development

help:		## Show this help display
	@echo 'The following commands can be used with make:'
	@echo ''
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)
	@echo ''

run: 		## Runs the main app
	flask --app main run

debug: 		## Runs the main app in debug mode
	flask --app main run --debug

test: 		## Runs all unit tests
	python3 -m unittest -v

coverage: 	## Generates code coverage from unit tests
	coverage run -m unittest
	coverage report -m

lint:		## Runs pylint recursively for the app directory
	pylint --rcfile=.pylintrc app

setup: 		## Installs packages from requirements.txt
	pip install -r requirements.txt

new_setup:	## Exports new packages to requirements.txt
	pip freeze > requirements.txt

clean_cache: 	## Clean pycaches
	rm -rf __pycache__

clean_dbs: 	## Removes database files
	rm app/databases/*.db

create_admin_user: 	## Creates admin user
	python3 script_runner.py create_admin_user