# Phase I - Builder source
FROM python:latest as builder
WORKDIR /usr/src/app
COPY app.py ./app.py
COPY .env ./.env
COPY pylint.cfg ./pylint.cfg
WORKDIR /wheels
COPY requirements.txt ./requirements.txt
# PIP Will create an archive of our libraries so we don't need to download them again
# argument - wheel
RUN pip wheel -r ./requirements.txt 

# Lints Code
# Phase II
FROM eeacms/pylint:latest as linting
WORKDIR /code
COPY --from=builder /usr/src/app/pylint.cfg /etc/pylint.cfg
COPY --from=builder /usr/src/app/app.py ./app.py
RUN ["/docker-entrypoint.sh", "pylint","--disable c0303,c0301,c0326"]

# Phase III Running Sonarqube scanner (Sonarqube server also required)
# FROM newtmitch/sonar-scanner as sonarqube
# WORKDIR /usr/src
# COPY --from=builder /usr/src/app/*.py ./
# RUN sonar-scanner -Dsonar.projectBaseDir=/usr/src

# Runs Unit Tests
# Phase IV
# FROM python:latest as unit-tests
# WORKDIR /usr/src/app
# # Copy all packages instead of rerunning pip install
# COPY --from=builder /wheels /wheels
# RUN     pip install -r /wheels/requirements.txt \
#                       -f /wheels \
#        && rm -rf /wheels \
#        && rm -rf /root/.cache/pip/* 

# COPY --from=builder /usr/src/app/ ./
# RUN ["make", "test"]

# Starts and Serves Web Page
# Phase VI
FROM python:3.7-slim as serve
# PYTHONUNBUFFERED Force logging to stdout / stderr not to be buffered into ram  
ENV PYTHONUNBUFFERED=1 
RUN mkdir root/.aws
COPY config root/.aws/
COPY credentials  root/.aws/
RUN apt-get -qq update && apt-get install -y build-essential \
    libssl-dev groff \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /usr/src/app
# Copy all packages instead of rerunning pip install
COPY --from=builder /wheels /wheels
RUN     pip install -r /wheels/requirements.txt \
                      -f /wheels \
       && rm -rf /wheels \
       && rm -rf /root/.cache/pip/* 

COPY --from=builder /usr/src/app/app.py ./app.py
COPY --from=builder /usr/src/app/.env ./.env
CMD ["python3", "app.py"]
