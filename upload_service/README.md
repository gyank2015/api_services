# upload_service

## 1 How To Run

### 1.1 Project info & directory structure

This is a dango(DRF) implementation for the [testing upload service](). 

### 1.2 Prerequisites & environment setup

All dependencies are in ```dependency_install.sh``` and ```requirements.txt```

As metioned in top-level README use the following to install dependencies
    ```
    # When running for the first time
    $ virtualenv [-p path to conda's python binary] venv # Only for the first time
    $ source ./venv/bin/activate
    $ ./dependency_install.sh # Dependencies not available by pip.
    $ pip install -r requirements.txt
    # Everytime before running the project
    $ source ./env/bin/activate # While the avengers env is active
    $ source ./project_prerun.sh # Contains env varibles for this project/django app
    $ ./manage.py runserver [host:port] # and voila!
    ```
## 2 Tests

All tests, if any are in ```tests.py``` for each app and test data in ```test``` directory. To run tests:
    ```
    # ./manage.py test
    ```
## 3 API definition (Swagger etc.)

The swagger exposed API definitions are avaliable at ```host:port/swagger```. Currently ```django_rest_swagger``` doesn't support ```file``` type parameters hence file types may appear as ```string```. So for manual testing purposes we have a view exposed(only in Debug mode), at ```host:port/test/test/upload```.