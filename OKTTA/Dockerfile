FROM python:3.10.5

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libc6-dev \
    libffi-dev \
    libpq-dev \
    postgresql-client

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . .

COPY init_db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init_db.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]