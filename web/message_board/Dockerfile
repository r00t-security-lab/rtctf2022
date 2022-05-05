FROM python:3.8
RUN mkdir /fastapi
WORKDIR /fastapi
ADD . /fastapi/
RUN chmod u+x /fastapi/run.sh
RUN /fastapi/run.sh
EXPOSE 8080
