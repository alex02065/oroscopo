FROM python:3.10.4

RUN apt-get update

RUN apt-get install gettext -y

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["./fla.sh"]