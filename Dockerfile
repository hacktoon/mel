FROM python:3.6

WORKDIR  /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/app/bin/dale"]
