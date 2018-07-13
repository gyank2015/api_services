# Avengers

## 1 How To Run

### 1.1 Project info & directory structure

The top-level directories are themselves independent projects.
###### Note: For project level information refer project README, inside the project directory.

### 1.2 Prerequisites & environment setup

To manage project wide dependency we're using conda environment specified in ```environment.yml```. Install [conda](https://conda.io/docs/user-guide/install/linux.html) from here if you don't already have it installed. To setup the environment run the following commands:

    ```
    $ conda env create -f environment.yml
    $ source activate avengers
    ```
To manage each sub-project's dependency we're using virtualenv, just because this is what'll be used to mange dependencies inside docker. So, when using a particular project use the porject's ```requirements.txt``` in the sub-project's root directory. For example: for upload_service
    ```
    $ cd ./upload_service
    $ virtualenv [-p path to conda's python binary] venv # Only for the first time
    # For more info check specific project README
    ```