FROM python:3.7

EXPOSE 8501

WORKDIR /app

COPY requirements.txt ./

RUN python3.7 -m venv ~/.virt_env01

RUN source ~/.virt_env01/bin/activate

RUN pip install -U pip

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]
