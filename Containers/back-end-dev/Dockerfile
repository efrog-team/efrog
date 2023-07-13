FROM ubuntu:22.04

RUN apt-get update
RUN apt-get -y install curl

RUN apt-get -y install gcc-11
RUN apt-get -y install g++-11

RUN apt-get -y install python3
RUN apt-get -y install python3-pip

COPY Connector/__MAIN__/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY Connector/__MAIN__ Connector/__MAIN__

COPY Checker Checker

WORKDIR /Connector/__MAIN__

EXPOSE 8000
EXPOSE 3306

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]