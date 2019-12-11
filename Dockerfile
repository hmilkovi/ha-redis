FROM python:3.8.0-alpine3.10
ENV LOG_LEVEL info
RUN mkdir /app
COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

COPY cli.py /app/
WORKDIR /app

CMD ["python", "./cli.py"]

ENTRYPOINT ["python", "./cli.py"]