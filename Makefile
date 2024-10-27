# Makefile for Razigma project

# Variables
PYTHON = python3
PIP = pip3
FLASK = flask
VENV = venv
VENV_ACTIVATE = . $(VENV)/bin/activate

# Default target
all: setup run

# Setup virtual environment and install dependencies
setup: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VENV_ACTIVATE) && $(PIP) install -r requirements.txt

# Run the Flask application
run:
	$(VENV_ACTIVATE) && $(FLASK) --app server run

# Initialize the database
init_db:
	$(VENV_ACTIVATE) && $(PYTHON) database.py

# Flask database commands
db_init:
	$(VENV_ACTIVATE) && $(FLASK) --app server db init

db_migrate:
	$(VENV_ACTIVATE) && $(FLASK) --app server db migrate

db_upgrade:
	$(VENV_ACTIVATE) && $(FLASK) --app server db upgrade

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf $(VENV)

# Phony targets
.PHONY: all setup run init_db db_init db_migrate db_upgrade delete_db clean
