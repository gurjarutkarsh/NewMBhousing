FROM python:3.9

ENV DB_USER="postgres"

WORKDIR /firstdocker

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["python", "manage.py", "runserver"]