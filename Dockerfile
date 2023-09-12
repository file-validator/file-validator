FROM python:3.8

WORKDIR /src

COPY . /src

RUN pip install -r requirements_test.txt
RUN pip install -r requirements_dev.txt

RUN pytest --cov
