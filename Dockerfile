FROM python:3.6

WORKDIR  /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

ENTRYPOINT ["python", "/app/cli.py"]

