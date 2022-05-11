FROM python:3.7-slim

WORKDIR /app

ENV PATH=$PATH:/usr/bin

RUN pip install --upgrade pip
#COPY ./dist ./dist
#RUN pip install ./dist/*tar.gz

COPY ./setup.cfg .
COPY ./setup.py .

RUN pip install --no-cache-dir --upgrade -e '.[dev]'
COPY . ./book_service

COPY ./entrypoint_*.sh /usr/bin/

RUN chmod +x /usr/bin/entrypoint_*.sh

CMD [ "python", "book_service/run.py" ]