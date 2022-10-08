FROM python:3.7-slim-buster

ADD . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]