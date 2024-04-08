# CITS3403 Agile Web Development Project

## Setting up the project development environment

-   Create the development environment using `python3 -m venv .venv`. This will create a virtual environment folder called _.venv_.
-   Activate the virtual environment folder using `source .venv/bin/activate`. You will know this has worked if a **(.venv)** prefix has appeared in your CLI.
-   Install project dependencies, as described below.

## Project dependencies

Python version: 3.12.2 (Latest)

Install dependencies using `pip install -r requirements.txt`.

Whenever a dependency has been added, it must be exported using `pip freeze > requirements.txt`.

## Running the project

After setting up the virtual environment and installing the dependencies, run `flask --app main run`

-   Alternatively, Visual Studio Code's launch.json the project can be run from the 'Run and Debug' tool (F5)

## Running tests

To run specified test files:

-   run `python -m unittest tests/<testName.py>` replacing testName.py with the file you want to run.

To run all test files in the tests directory:

-   run `python -m unittest`.

If you would like to see what tests are being run, use the `-v` flag with the commands above.

These commands should be run in the app's root directory since the main app file needs to be accessed.

There is no need to run the main app for testing.

## Our Team :)

| Student Number | Name              | Github User Name |
| -------------- | ----------------- | ---------------- |
| 23398223       | Jared Healy       | jh1236           |
| 23460936       | Brigitte Gredziuk | aeoniaa          |
| 23372032       | James Frayne      | Semuca           |
| 23643117       | Heidi Leow        | sellsol          |
