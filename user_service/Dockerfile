#FROM python:3.7-slim
#
#WORKDIR /app
#
#
#RUN pip install --upgrade pip
#
#COPY ./setup.cfg .
#COPY ./setup.py .
##COPY ./dist ./dist
##
##WORKDIR ./dist
##
##RUN pip install *tar.gz
#
##WORKDIR /app
#
#RUN pip install --no-cache-dir --upgrade -e ".[dev]"
#
#COPY ./entrypoint_*.sh /usr/bin/
#
#RUN chmod +x /usr/bin/entrypoint_*.sh
#
#COPY . ./user_service
#
#CMD [ "python", "user_service/run.py" ]
##



FROM python:3.7-slim

WORKDIR /app

ENV PATH=$PATH:/usr/bin

RUN pip install --upgrade pip
#COPY ./dist ./dist
#RUN pip install ./dist/*tar.gz

COPY ./setup.cfg .
COPY ./setup.py .

RUN pip install --no-cache-dir --upgrade -e ".[dev]"
COPY . ./user_service

COPY ./entrypoint_*.sh /usr/bin/

RUN chmod +x /usr/bin/entrypoint_*.sh

CMD [ "python", "user_service/run.py" ]