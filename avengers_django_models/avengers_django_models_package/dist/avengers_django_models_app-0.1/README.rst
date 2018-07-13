=====
Avengers_django_models_app
=====

avengers_django_models_app is a Django app containing all the model definitions to be used by other avengers apps.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "avengers_django_models_app" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'avengers_django_models_app',
    ]

2. Include the avengers_django_models_app URLconf in your project urls.py like this::

    path('avengers_django_models_app/', include('avengers_django_models_app.urls')),

3. Run `./manage.py migrate` to create the avengers_django_models_app models.