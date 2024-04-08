# Makefile with some common commands for development

help:		## Show this help
	@echo 'The following commands can be used with make:'
	@echo ''
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)
	@echo ''

run: 		## Runs the main app
	flask --app main run

test: 		## Runs all unit tests
	python3 -m unittest -v

setup: 		## Installs packages from requirements.txt
	pip install -r requirements.txt

new_setup:	## Exports new packages to requirements.txt
	pip freeze > requirements.txt

clean_cache: 	## Clean pycaches
	rm -rf __pycache__

clean_dbs: 	## Removes database files
	rm app/databases/test.db
	rm app/databases/dev.db
