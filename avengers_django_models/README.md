# avengers_django_models

## 1 How To Run

### 1.1 Project info & directory structure

This contains the app, that defines all the models for the whole project. This is done so that in the scenario that a model is required in more than one project, the model definition(and hence the ORMs) can be imported into the apps/projects without code duplication.

The ```avengers_django_models_app``` is the app that contains the model definitions and is to be packaged and imported across all the projects. ```avengers_django_models_package``` contains the scripts and files required for packaging. For more on packaging and use see the packaging section below. 

### 1.2 Prerequisites & environment setup


As metioned in top-level README use the following to install dependencies
    ```
    # When running for the first time
    $ virtualenv [-p path to conda's python binary] venv # Only for the first time
    $ source ./venv/bin/activate
    $ pip install -r requirements.txt
    # Everytime before running the project
    $ source ./env/bin/activate # While the avengers env is active
    $ ./manage.py runserver [host:port] # and voila!
    ```
## 2 Tests

All tests, if any are in ```tests.py``` for each app and test data in ```test``` directory. To run tests:
    ```
    # ./manage.py test
    ```
## 4 Packaging ```avengers_django_models_app```

All the scripts for pacakaging resides in ```avengers_django_models_package``` directory. To package:
    ```
    $ chmod +x package_models_app.sh
    $ ./package_models_app.sh
    # The package is created in /avengers_django_models_package/dist/avengers_django_models_app-<version_number>.tar.gz
    ```
###### Note: After every iteration of the app, please bump the version(in /avengers_django_models_package/setup.py) to keep track of changes in dependent apps.

## 5 Usage

For use of the packaged app. 
    ```
    $ pip install <path to the package tar>

    # In another project use it by adding it to INSTALLED_APPS
    INSTALLED_APPS = [
        ...
        'avengers_django_models_app',
    ]
    # Import the models like:
    from avengers_django_models_app.models import <model_name>
    ```
