FROM python:3.10-slim

RUN \
    # Print executed commands to terminal.
    set -ex ; \
    savedAptMark="$(apt-mark showmanual)" ; \
    apt-get update ; \
    apt install -y build-essential ; \
    apt-mark auto '.*' > /dev/null; \
    apt-mark manual $savedAptMark

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
	rm -rf /var/lib/apt/lists/*

COPY . .

#WORKDIR /app
#
#COPY . /app
#
#RUN pip install -U pip
#
#RUN pip install --no-cache-dir -r requirements.txt

#EXPOSE 8080

RUN mkdir ~/.streamlit

RUN cp config.toml ~/.streamlit/config.toml

RUN cp credentials.toml ~/.streamlit/credentials.toml

#ENTRYPOINT ["streamlit", "run"]

CMD ["streamlit", "run", "app.py"]

#
#
#FROM python:3.7.11-slim
#
#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt
#
#COPY . .
#
#ENV GUNICORN_CMD_ARGS='--bind 0.0.0.0:8080 -w 4 --log-level warning -k uvicorn.workers.UvicornWorker'
#
#CMD ["gunicorn", "main:app"]
#
