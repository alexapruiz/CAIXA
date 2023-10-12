FROM python:3.10

COPY BancodeDados.py /app/BancodeDados.py
COPY Clearcase.db /app/Clearcase.db
COPY servidor.py /app/servidor.py
COPY requirements.txt /app/requirements.txt
COPY templates/index.html /app/templates/index.html

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python","servidor.py"]
