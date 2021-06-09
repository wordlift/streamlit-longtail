FROM python:3.7-slim

WORKDIR /app

COPY . /app

RUN pip install -U pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

RUN mkdir ~/.streamlit

RUN cp config.toml ~/.streamlit/config.toml

RUN cp credentials.toml ~/.streamlit/credentials.toml

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]
