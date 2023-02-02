FROM python:3.10.9-alpine3.16

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy dependency files and code
COPY poetry.lock /temp/poetry.lock
COPY pyproject.toml /temp/pyproject.toml

WORKDIR /temp

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-client build-base postgresql-dev gcc python3-dev musl-dev

# Add locales in alpine image
ENV MUSL_LOCALE_DEPS cmake make musl-dev gcc gettext-dev libintl
ENV MUSL_LOCPATH /usr/share/i18n/locales/musl
RUN apk add --no-cache \
    $MUSL_LOCALE_DEPS \
    && unzip musl-locales-master.zip \
      && cd musl-locales-master \
      && cmake -DLOCALE_PROFILE=OFF -D CMAKE_INSTALL_PREFIX:PATH=/usr . && make && make install \
      && cd .. && rm -r musl-locales-master

RUN apk add make

# Install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install


COPY city-poster /web-app/city-poster
COPY .env /web-app
COPY Makefile /web-app
COPY poetry.lock /web-app
COPY pyproject.toml /web-app
WORKDIR /web-app/city-poster

#EXPOSE 8000

RUN adduser --disabled-password service-user

USER service-user