FROM python:3.7-slim

WORKDIR /app


RUN pip install --upgrade pip

COPY ./setup.cfg .
COPY ./setup.py .
COPY ./dist ./dist

WORKDIR ./dist

RUN pip install *tar.gz

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -e '.[dev]'

COPY ./entrypoint_*.sh /usr/bin/

RUN chmod +x /usr/bin/entrypoint_*.sh

COPY . ./user_service

CMD [ "python", "user_service/run.py" ]