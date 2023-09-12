FROM python:3.8

WORKDIR /src

COPY . /src

RUN pip install --no-cache-dir -r requirements_test.txt
RUN pip install --no-cache-dir -r requirements_dev.txt

RUN pytest --cov
