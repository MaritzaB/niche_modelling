FROM ubuntu:latest

ENV TZ=US/Pacific

RUN ln --symbolic --no-dereference --force /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install --yes --no-install-recommends apt-utils

RUN apt-get update && \
    apt upgrade --yes && \
    apt-get install make --yes

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
    libpq-dev gcc \
    gettext-base \
    git \
    make \
    pandoc \
    python3 \
    python3-dev \
    python3-pip


RUN pip install --upgrade \
    black -U \
    ipykernel \
    matplotlib \
    numpy \
    pandas \
    pytest \
    -U scikit-learn \
    seaborn \
    imblearn \
    openpyxl \
    xarray \
    psycopg2 \
    sqlalchemy \
    cdsapi \
    netcdf4
