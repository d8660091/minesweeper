FROM python:3.6.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements /code/requirements
RUN ["ls"]
RUN pip install -r ./requirements/prod.txt
ADD . /code/
