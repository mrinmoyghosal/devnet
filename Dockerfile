FROM python:3.9

RUN pip install pipenv

# set the working directory in the container
WORKDIR /src

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system

# copy the dependencies file to the working directory
COPY . .

# install dependencies

RUN ["pipenv", "run", "flake8", "app"]

RUN ["pipenv", "run", "pylint", "--fail-under", "10", "--load-plugins", "pylint_flask", "pylint_flask_sqlalchemy", "app"]
RUN ["pipenv", "run", "pytest", "--ignore", "src", "--rootdir",  "app", "--disable-warnings"]
# command to run on container start
RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 5000