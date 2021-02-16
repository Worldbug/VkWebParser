FROM python:latest
LABEL maintainer="Kirill T."
LABEL version="0.1"
LABEL description="Web VK parser"

RUN pip install --upgrade pip
RUN pip install flask

WORKDIR /usr/src/app
COPY ./ .
ENV FLASK_RUN_HOST 0.0.0.0
ENTRYPOINT ["python", "./run.py"]

#EXPOSE 5000

#VOLUME /Logs
