# rooftop_damage_analysis

## 1 How To Run

### 1.1 Project info & directory structure

This is a dango(DRF) implementation for the [rooftop_damage_analysis](). 

### 1.2 Prerequisites & environment setup

All dependencies are in ```requirements.txt```

As metioned in top-level README use the following to install dependencies
    ```
    # When running for the first time
    $ virtualenv [-p path to conda's python binary] venv # Only for the first time
    $ source ./venv/bin/activate
    $ pip install -r requirements.txt
    # Everytime before running the project
<<<<<<< HEAD
    $ source ../inter_project_env_setup.sh
=======
>>>>>>> rooftop-damage-analysis
    $ source ./env/bin/activate # While the avengers env is active
    $ source ./project_prerun.sh # Contains env varibles for this project/django app
    $ ./manage.py runserver [host:port] # and voila!
    ```
## 2 Tests

Currently there are no tests for this service.
All tests, if any will be in ```tests.py``` for each app and test data in ```test``` directory. To run tests:
    ```
    # ./manage.py test
    ```
## 3 API definition (Swagger etc.)

The swagger exposed API definitions are avaliable at ```host:port/swagger``` and can be tested from the same. 