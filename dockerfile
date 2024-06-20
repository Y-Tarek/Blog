FROM python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install gunicorn

RUN pip install psycopg2-binary


COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /app/
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
RUN mkdir /app/static

ENTRYPOINT ["sh", "/app/entrypoint.sh"]