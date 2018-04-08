FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /librarycode
WORKDIR /librarycode
ADD requirements.txt /librarycode/
RUN pip install -r requirements.txt
ADD . /librarycode/