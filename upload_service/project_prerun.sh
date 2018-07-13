# This is to keep track of env variables and to export them in test environment.
# In productionn kubernetes and the container config sould handle this.

export MEDIA_ROOT="/fractal/home/gyan/api_service/avengers/media/car_damage/data"
export LOGS_ROOT="/fractal/home/gyan/api_service/avengers/logs"

export TEST_ENV=true
export PROD_ENV=false
export MONGODB_TEST_HOST="127.0.0.1"
export MONGODB_TEST_PORT=27017
export MONGODB_PROD_HOST="127.0.0.1"
export MONGODB_PROD_PORT=27017
