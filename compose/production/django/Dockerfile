FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

# 替换为国内源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

WORKDIR /django_app

RUN pip install pipenv -i https://mirrors.aliyun.com/pypi/simple/

COPY Pipfile /django_app/Pipfile
COPY Pipfile.lock /django_app/Pipfile.lock
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /django_app

COPY ./compose/production/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh
