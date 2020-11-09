FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN mkdir app
WORKDIR /app

COPY ./app/* /app/
RUN /usr/local/bin/python -m pip install --upgrade pip

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

ENV TZ Asia/Almaty
